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
        self.pending_withdrawal=False;self.enabled=False;self.alias='';self.token='';self.entries=[];self.status='';self.busy=False;self.sent={}
        try:
            d=json.loads(self.path.read_text());self.token=d['token'];self.alias=d['alias']
            self.enabled=d['enabled'] is True and d.get('origin')==origin and d.get('consent_version')==2
            self.sent=d.get('sent',{}) if isinstance(d.get('sent'),dict) else {}
            self.pending_withdrawal=d.get('pending_withdrawal') is True
        except (OSError,ValueError,KeyError,TypeError):pass
        if not isinstance(self.token,str) or len(self.token)!=64:self.token=secrets.token_hex(32)
        if not isinstance(self.alias,str) or not self.alias:self.alias='Striker-'+secrets.token_hex(3)

    def save(self):
        import os,tempfile
        self.path.parent.mkdir(parents=True,exist_ok=True)
        fd,name=tempfile.mkstemp(dir=self.path.parent)
        try:
            with os.fdopen(fd,'w') as f:json.dump(dict(token=self.token,alias=self.alias,enabled=self.enabled,origin=self.origin,pending_withdrawal=self.pending_withdrawal,consent_version=2,sent=self.sent),f)
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
        query='/v2/records?'+urlencode(dict(edition=edition,country=country,division=division))
        snapshots=[dict(r) for r in getattr(career,'completed_records',[]) if valid_record(r)]
        publish=self.enabled and not withdraw
        self.busy=True
        def work():
            try:
                if withdraw:
                    self.request('/v2/records/withdraw',{'token':self.token})
                    self.pending_withdrawal=False;self.sent={};self.save()
                elif publish:
                    sent=0
                    for record in snapshots:
                        digest=hashlib.sha256(json.dumps(record,sort_keys=True).encode()).hexdigest()
                        if digest in self.sent:continue
                        self.request('/v2/records',dict(token=self.token,record=record))
                        self.sent[digest]=True;self.save();sent+=1
                        if sent>=8:break
                result=self.request(query);entries=result.get('entries')
                if result.get('schema')!=2 or not isinstance(entries,list) or len(entries)>100:raise ValueError('Invalid records')
                if any(not valid_record(e) or (e['edition'],e['country'],e['division'])!=(edition,country,division) for e in entries):raise ValueError('Wrong division')
                self.entries=entries
                self.status='Completed-season records updated.'
            except HTTPError as error:
                self.status='Server update required.' if error.code==404 else 'Service unavailable. Refresh to retry.'
            except Exception:self.status='Offline. Completed records are kept on this device.'
            finally:
                self.busy=False
                if callback:callback()
        threading.Thread(target=work,daemon=True).start()
