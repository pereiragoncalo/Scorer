"""Opt-in casual ranking; persistent random credential, never the career name."""
import json
import secrets
import ssl
import threading
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request,build_opener,HTTPSHandler
from urllib.request import HTTPRedirectHandler

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
        self.pending_withdrawal=False;self.enabled=False;self.alias='';self.token='';self.entries=[];self.status='';self.busy=False
        try:
            d=json.loads(self.path.read_text());self.token=d['token'];self.alias=d['alias']
            self.enabled=d['enabled'] is True and d.get('origin')==origin
            self.pending_withdrawal=d.get('pending_withdrawal') is True
        except (OSError,ValueError,KeyError,TypeError):pass
        if not isinstance(self.token,str) or len(self.token)!=64:self.token=secrets.token_hex(32)
        if not isinstance(self.alias,str) or not self.alias:self.alias='Striker-'+secrets.token_hex(3)

    def save(self):
        import os,tempfile
        self.path.parent.mkdir(parents=True,exist_ok=True)
        fd,name=tempfile.mkstemp(dir=self.path.parent)
        try:
            with os.fdopen(fd,'w') as f:json.dump(dict(token=self.token,alias=self.alias,enabled=self.enabled,origin=self.origin,pending_withdrawal=self.pending_withdrawal),f)
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
        req=Request(self.origin+path,data=data,headers={'Content-Type':'application/json','User-Agent':'Scorer/0.6.41','Accept':'application/json'})
        with opener.open(req,timeout=5) as response:
            body=response.read(65537)
            if len(body)>65536:raise ValueError('Response too large')
            return json.loads(body) if body else {}

    def sync(self,career,world,callback=None,withdraw=False):
        if self.busy:return
        # Snapshot on UI thread; worker never touches the live career/Kivy.
        payload=dict(token=self.token,alias=self.alias,edition='world' if world else 'free',season=career.season,matches=career.matches,goals=career.goals)
        self.busy=True
        def work():
            try:
                if withdraw:
                    self.request('/v1/leaderboard/withdraw',{'token':self.token})
                    self.pending_withdrawal=False;self.save()
                elif self.enabled and payload['matches']>0:self.request('/v1/leaderboard',payload)
                result=self.request('/v1/leaderboard');entries=result.get('entries')
                if not isinstance(entries,list) or len(entries)>100:raise ValueError('Invalid ranking')
                for e in entries:
                    if not isinstance(e,dict) or set(e)!={'edition','season','alias','matches','goals'}:raise ValueError('Invalid row')
                    import re
                    if e['edition'] not in ('free','world') or not isinstance(e['alias'],str) or not re.fullmatch(r'[A-Za-z0-9 _-]{3,20}',e['alias']):raise ValueError('Invalid alias')
                    if any(type(e[k]) is not int for k in ('season','matches','goals')):raise ValueError('Invalid score')
                self.entries=entries
                self.status='Updated. Scores are self-reported.'
            except Exception:self.status='Offline or service unavailable. Your career is safe.'
            finally:
                self.busy=False
                if callback:callback()
        threading.Thread(target=work,daemon=True).start()
