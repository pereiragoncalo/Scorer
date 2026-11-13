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
        self.division=1;self.approved_seasons=[];self.next_retry=0;self._pending_lock=threading.RLock()
        try:
            d=json.loads(self.path.read_text());self.token=d['token'];self.alias=d['alias']
            self.enabled=d['enabled'] is True and d.get('origin')==origin and d.get('consent_version')==3
            self.career_enabled=d.get('career_enabled') is True and self.enabled
            self.sent=d.get('sent',{}) if isinstance(d.get('sent'),dict) else {}
            self.pending_withdrawal=d.get('pending_withdrawal') is True
            self.terms_version=1 if d.get('terms_version')==1 else 0
            self.blocked={x for x in d.get('blocked',[]) if isinstance(x,str) and len(x)==32}
            from division_records import valid_record
            self.approved_seasons=[j for j in (d.get('approved_seasons',[])[:1024] if d.get('origin')==origin else []) if isinstance(j,dict) and j.get('consent_version')==1 and isinstance(j.get('key'),str) and len(j['key'])==64 and valid_record(j.get('record'))]
        except (OSError,ValueError,KeyError,TypeError):pass
        # Legacy global opt-in never authorizes publishing another season.
        self.enabled=False;self.career_enabled=False
        if not isinstance(self.token,str) or len(self.token)!=64:self.token=secrets.token_hex(32)
        if not isinstance(self.alias,str) or not self.alias:self.alias='Striker-'+secrets.token_hex(3)

    def save(self):
        with self._pending_lock:self._save_state()

    def _save_state(self):
        import os,tempfile
        self.path.parent.mkdir(parents=True,exist_ok=True)
        fd,name=tempfile.mkstemp(dir=self.path.parent)
        try:
            with os.fdopen(fd,'w') as f:json.dump(dict(approved_seasons=self.approved_seasons,career_enabled=self.career_enabled,token=self.token,alias=self.alias,enabled=self.enabled,origin=self.origin,pending_withdrawal=self.pending_withdrawal,consent_version=3,sent=self.sent,terms_version=self.terms_version,blocked=sorted(self.blocked)),f)
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
        if withdraw:return self.withdraw_all(callback)
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
        publish=False  # v3/v4 automatic bulk publication has been retired.
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

    def enqueue_season(self,records,name):
        from division_records import valid_record
        import hashlib
        name=name.strip() if isinstance(name,str) else ''
        jobs=[]
        for record in records:
            row=dict(record,player=name)
            if not valid_record(row):raise ValueError('Enter a valid public name.')
            key=hashlib.sha256(('v5:'+json.dumps(row,sort_keys=True)).encode()).hexdigest()
            if key not in self.sent and not any(j['key']==key for j in self.approved_seasons):jobs.append(dict(key=key,record=row,consent_version=1))
        if not records:raise ValueError('No completed league season to publish.')
        with self._pending_lock:
            old=list(self.approved_seasons);self.approved_seasons+=jobs
            try:self.save()
            except OSError:self.approved_seasons=old;raise
        return [j['key']for j in jobs]

    def cancel_jobs(self,keys):
        self.approved_seasons=[j for j in self.approved_seasons if j['key']not in keys];self.save()

    def refresh_division(self,division,callback=None):
        if type(division)is not int or division not in (1,2):raise ValueError('Invalid division')
        if self.busy:return False
        self.division=division;self.busy=True
        def work():
            try:
                result=self.request('/v5/records?division='+str(division));entries=result.get('entries')
                if result.get('schema')!=5 or result.get('division')!=division or not isinstance(entries,list) or len(entries)>100 or any(not valid_division_entry(e)for e in entries):raise ValueError('Invalid classification')
                self.entries=[e for e in entries if e['publisher']not in self.blocked]
                self.status='' if self.entries else 'No published records yet.'
            except HTTPError as error:self.status='Server update required.' if error.code in (404,426) else 'Service unavailable. Refresh to retry.'
            except Exception:self.status='Offline. Try again when connected.'
            finally:
                self.busy=False
                if callback:callback()
        threading.Thread(target=work,daemon=True).start();return True

    def flush_approved(self,callback=None):
        import time
        if self.busy or time.monotonic()<self.next_retry or not (self.approved_seasons or self.pending_withdrawal):return False
        self.busy=True
        def work():
            try:
                if self.pending_withdrawal:
                    self.request('/v5/records/withdraw',{'token':self.token});self.pending_withdrawal=False;self.save()
                for job in list(self.approved_seasons)[:8]:
                    self.request('/v5/records',dict(token=self.token,record=job['record'],consent_version=job['consent_version']))
                    with self._pending_lock:
                        self.sent[job['key']]=True
                        if job in self.approved_seasons:self.approved_seasons.remove(job)
                        self.save()
                self.status='Submitted for moderator review.'
            except HTTPError as error:
                self.next_retry=time.monotonic()+60
                self.status='Server update required.' if error.code in (404,426) else 'Saved to send when connected.'
            except Exception:self.next_retry=time.monotonic()+60;self.status='Saved to send when connected.'
            finally:
                self.busy=False
                if callback:callback()
        threading.Thread(target=work,daemon=True).start();return True

    def withdraw_all(self,callback=None):
        self.approved_seasons=[];self.pending_withdrawal=True;self.enabled=False;self.career_enabled=False;self.save();self.next_retry=0
        return self.flush_approved(callback)

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


def valid_division_entry(e):
    import re
    from season_records import safe_text
    return (isinstance(e,dict) and set(e)=={'player','goals','publisher'} and safe_text(e['player'],60)
            and type(e['goals'])is int and 0<=e['goals']<=4000 and isinstance(e['publisher'],str)
            and re.fullmatch('[0-9a-f]{32}',e['publisher']) is not None)
