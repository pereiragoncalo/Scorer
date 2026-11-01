"""Optional legal-rights workflow, separate from ordinary automatic usage."""
import hashlib,json,secrets,threading,time,re
from pathlib import Path
from online_safety import atomic_json

def reference(token):return 'SCW-'+hashlib.sha256(('privacy:'+token).encode()).hexdigest()[:20].upper()

class PrivacyRequest:
    def __init__(self,directory,origin=''):
        self.path=Path(directory)/'scorer_privacy_request.json';self.origin=origin;self.token='';self.status='none';self.message='';self.busy=False;self.last_attempt=0
        if self.path.exists():
            self.status='needs_support'  # Corruption must not silently restart collection.
            try:
                if self.path.stat().st_size>8192:return
                d=json.loads(self.path.read_text())
                if set(d)!={'schema','token','status'} or type(d['schema']) is not int or d['schema']!=1 or not re.fullmatch('[0-9a-f]{64}',d['token']) or d['status'] not in ('pending','granted','closed'):return
                self.token=d['token'];self.status=d['status']
            except (OSError,ValueError,TypeError,KeyError):pass
    @property
    def active(self):return self.status in ('pending','granted','needs_support')
    @property
    def case_reference(self):return reference(self.token) if self.token else ''
    def save(self,status=None):atomic_json(self.path,dict(schema=1,token=self.token,status=self.status if status is None else status))
    def object(self):
        if not self.token:self.token=secrets.token_hex(32)
        self.status='pending'
        try:self.save();self.message='Request saved. Usage collection is suspended.'
        except OSError:self.message='Usage is paused for this session. Could not save the request; contact support and retry.'
    def sync(self,callback=None,withdraw=False,force=False):
        if self.busy or not self.token or (not force and time.monotonic()-self.last_attempt<60):return False
        from online_leaderboard import valid_origin,Leaderboard
        if not valid_origin(self.origin):return False
        self.busy=True;self.last_attempt=time.monotonic()
        def work():
            try:
                result=Leaderboard(self.path.parent,self.origin).request('/v1/privacy/request',{'token':self.token,'action':'withdraw' if withdraw else 'object'})
                if set(result)!={'schema','reference','status'} or type(result['schema']) is not int or result['schema']!=1 or result['reference']!=self.case_reference or result['status'] not in ('pending','granted','closed'):raise ValueError('Invalid rights response')
                new=result['status']
                # A granted request cannot be silently closed by a background lookup.
                if new=='closed' and not withdraw:raise ValueError('Unexpected rights resumption')
                # Publish the new in-memory state only after durable storage succeeds.
                self.save(status=new);self.status=new
                self.message='Request withdrawn. Automatic usage resumes on your next opening.' if new=='closed' else 'Privacy request received. Usage remains suspended.'
            except Exception:self.message='Offline or unavailable. Usage stays suspended; retry or contact support.'
            finally:
                self.busy=False
                if callback:callback()
        threading.Thread(target=work,daemon=True).start();return True
