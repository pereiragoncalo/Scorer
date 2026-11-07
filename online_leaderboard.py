"""Opt-in completed-season records; explicit consent to share player and team."""
import json
import secrets
import ssl
import threading
from pathlib import Path
from urllib.parse import urlsplit,urlencode
from urllib.request import Request,build_opener,HTTPSHandler
from urllib.request import HTTPRedirectHandler
from urllib.error import HTTPError

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*a,**kw):return None

def valid_origin(origin):
    try:
        u=urlsplit(origin)
        return (isinstance(origin,str) and len(origin)<=512 and not any(c.isspace() for c in origin)
                and u.scheme=='https' and bool(u.hostname) and not u.username and not u.password
                and not u.query and not u.fragment and not u.path and u.port in (None,443))
    except (ValueError,TypeError):return False

class Leaderboard:
    def __init__(self,directory,origin=''):
        self.path=Path(directory)/'leaderboard.json';self.origin=origin
        self.pending_withdrawal=False;self.enabled=False;self.career_enabled=False;self.alias='';self.token='';self.entries=[];self.status='';self.busy=False;self.sent={};self.blocked=set();self.terms_version=0
        try:
            d=json.loads(self.path.read_text());self.token=d['token'];self.alias=d['alias']
            self.enabled=d['enabled'] is True and d.get('origin')==origin and d.get('consent_version')==3
            self.career_enabled=d.get('career_enabled') is True and self.enabled
            self.sent=d.get('sent',{}) if isinstance(d.get('sent'),dict) else {}
            self.pending_withdrawal=d.get('pending_withdrawal') is True
            self.terms_version=1 if d.get('terms_version')==1 else 0
            self.blocked={x for x in d.get('blocked',[]) if isinstance(x,str) and len(x)==32}
        except (OSError,ValueError,KeyError,TypeError):pass
        if not isinstance(self.token,str) or len(self.token)!=64:self.token=secrets.token_hex(32)
        if not isinstance(self.alias,str) or not self.alias:self.alias='Striker-'+secrets.token_hex(3)

    def save(self):
        import os,tempfile
        self.path.parent.mkdir(parents=True,exist_ok=True)
        fd,name=tempfile.mkstemp(dir=self.path.parent)
        try:
            with os.fdopen(fd,'w') as f:json.dump(dict(career_enabled=self.career_enabled,token=self.token,alias=self.alias,enabled=self.enabled,origin=self.origin,pending_withdrawal=self.pending_withdrawal,consent_version=3,sent=self.sent,terms_version=self.terms_version,blocked=sorted(self.blocked)),f)
            os.replace(name,self.path)
        finally:
            try:os.unlink(name)
            except FileNotFoundError:pass

    def request(self,path,payload=None):
        if not valid_origin(self.origin):raise ValueError('Service not configured')
        from network_tls import verified_context
        context=verified_context()
        opener=build_opener(NoRedirect(),HTTPSHandler(context=context))
        data=None if payload is None else json.dumps(payload).encode()
        req=Request(self.origin+path,data=data,headers={'Content-Type':'application/json','User-Agent':'Scorer/0.6.42','Accept':'application/json'})
        with opener.open(req,timeout=5) as response:
            body=response.read(65537)
            if len(body)>65536:raise ValueError('Response too large')
            return json.loads(body) if body else {}

    def sync(self,career,world,callback=None,withdraw=False):
        if self.busy:return
        from season_records import scope,valid_record
        import hashlib
        edition,country,division=scope(career,world)
        category=getattr(self,'category','season')
        query=('/v4/records?' if category=='career' else '/v3/records?')+urlencode(dict(edition=edition,country=country,division=division))
        snapshots=[dict(r) for r in getattr(career,'completed_records',[]) if valid_record(r)]
        if category=='career':
            from career_records import snapshot
            career_snapshot=snapshot(career,world);snapshots=[career_snapshot] if career_snapshot else []
        publish=self.enabled and (category!='career' or self.career_enabled) and self.terms_version==1 and not withdraw
        self.busy=True
        def work():
            try:
                sent=0
                if withdraw:
                    self.request('/v3/records/withdraw',{'token':self.token})
                    self.pending_withdrawal=False;self.sent={};self.save()
                elif publish:
                    sent=0
                    for record in snapshots:
                        digest=hashlib.sha256((category+json.dumps(record,sort_keys=True)).encode()).hexdigest()
                        if digest in self.sent:continue
                        self.request('/v4/records' if category=='career' else '/v3/records',dict(token=self.token,record=record,terms_version=self.terms_version))
                        self.sent[digest]=True;self.save();sent+=1
                        if sent>=8:break
                result=self.request(query);entries=result.get('entries')
                if result.get('schema')!=(4 if category=='career' else 3) or not isinstance(entries,list) or len(entries)>100:raise ValueError('Invalid records')
                if any(not valid_public_entry(e,category) or (e['edition'],e['country'],e['division'])!=(edition,country,division) for e in entries):raise ValueError('Wrong division')
                self.entries=[e for e in entries if e['publisher'] not in self.blocked]
                self.status='Submitted for moderator review.' if sent else 'Completed-season records updated.'
            except HTTPError as error:
                self.status='Server update required.' if error.code in (404,426) else 'Service unavailable. Refresh to retry.'
            except Exception:self.status='Offline. Completed records are kept on this device.'
            finally:
                self.busy=False
                if callback:callback()
        threading.Thread(target=work,daemon=True).start()

    def block(self,publisher):
        import re
        if not isinstance(publisher,str) or not re.fullmatch('[0-9a-f]{32}',publisher):return False
        self.blocked.add(publisher);self.entries=[e for e in self.entries if e.get('publisher')!=publisher];self.save();return True

    def report(self,publisher,reason,callback=None):
        if self.busy:return False
        import re
        if not isinstance(publisher,str) or not re.fullmatch('[0-9a-f]{32}',publisher) or reason not in ('personal_info','abuse','spam','other'):return False
        self.busy=True
        def work():
            try:
                self.request('/v3/reports',{'token':self.token,'publisher':publisher,'reason':reason});self.status='Report sent for review.'
            except Exception:self.status='Report not sent. Check connection and retry.'
            finally:
                self.busy=False
                if callback:callback()
        threading.Thread(target=work,daemon=True).start();return True

def valid_public_entry(entry,category='season'):
    import re
    from season_records import FIELDS,valid_record
    if category=='career':
        from career_records import valid_record
    return (isinstance(entry,dict) and set(entry)==FIELDS|{'publisher','record_id'}
            and valid_record({k:entry[k] for k in FIELDS})
            and all(isinstance(entry[k],str) and re.fullmatch('[0-9a-f]{32}',entry[k]) for k in ('publisher','record_id')))
