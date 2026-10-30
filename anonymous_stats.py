"""Optional aggregate game usage counters. No accounts, names, device IDs or event logs."""
from datetime import datetime, timezone, date
import json
import os
from pathlib import Path
import ssl
import tempfile
import threading
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler, HTTPSHandler

EVENTS=frozenset(('sessions','sessions_ended','new_careers','careers_loaded','trainings_completed',
                 'matches_completed','goals_scored','load_failures','save_failures'))
MAX_COUNT=10000
MAX_FILE=16384


def valid_endpoint(value):
    if not isinstance(value,str) or len(value)>512 or any(c.isspace() for c in value):return False
    try:
        u=urlsplit(value)
        return u.scheme=='https' and bool(u.hostname) and not u.username and not u.password and not u.query and not u.fragment and u.port in (None,443) and u.path=='/v1/usage'
    except ValueError:return False


def valid_payload(data):
    return (isinstance(data,dict) and set(data)=={'schema','app','counts'}
            and type(data['schema']) is int and data['schema']==1 and data['app']=='scorer_free'
            and isinstance(data['counts'],dict) and bool(data['counts'])
            and set(data['counts'])<=EVENTS
            and all(type(n) is int and 0<n<=MAX_COUNT for n in data['counts'].values()))


class NoStatistics:
    enabled=False
    endpoint=''
    remote_available=False
    last_error=''
    def begin_session(self):pass
    def end_session(self):pass
    def record(self,*_,**__):return False
    def set_enabled(self,*_):return False
    def flush_async(self):return False


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*_,**__):return None


def send_counts(endpoint,payload):
    if not valid_endpoint(endpoint) or not valid_payload(payload):return False
    from network_tls import verified_context
    context=verified_context()
    body=json.dumps(payload,separators=(',',':')).encode('ascii')
    request=Request(endpoint,body,{'Content-Type':'application/json','User-Agent':'Scorer-Usage/1'},method='POST')
    try:
        with build_opener(_NoRedirect(),HTTPSHandler(context=context)).open(request,timeout=4) as response:
            response.read(256)
            return 200<=response.status<300
    except Exception:return False


class UsageStatistics(NoStatistics):
    def __init__(self,directory,endpoint='',sender=send_counts):
        self.path=Path(directory)/'scorer_usage.json'
        self.endpoint=endpoint if valid_endpoint(endpoint) else ''
        self.remote_available=bool(self.endpoint)
        self._scope=self.endpoint or 'local-v1'
        self._lock=threading.RLock();self._sender=sender;self._sending=False;self._generation=0
        self._session_seen=False;self._session_counted=False;self._session_ended=False;self._flush_requested=False
        self.enabled=False;self.counts={};self.day=self._today();self.last_error=''
        try:
            if self.path.stat().st_size>MAX_FILE:return
            data=json.loads(self.path.read_text(encoding='utf8'))
            if not isinstance(data,dict) or set(data)!={'schema','enabled','scope','day','counts'}:return
            if type(data['schema']) is not int or data['schema']!=1 or type(data['enabled']) is not bool or data['scope']!=self._scope:return
            if not isinstance(data['counts'],dict) or set(data['counts'])-EVENTS:return
            if any(type(n) is not int or not 0<n<=MAX_COUNT for n in data['counts'].values()):return
            day=date.fromisoformat(data['day'])
            age=(date.fromisoformat(self._today())-day).days
            self.enabled=data['enabled']
            if self.enabled and 0<=age<=7:self.counts=data['counts'];self.day=data['day']
        except (OSError,ValueError,TypeError):pass

    @staticmethod
    def _today():return datetime.now(timezone.utc).date().isoformat()

    def _save(self):
        temporary=None
        try:
            self.path.parent.mkdir(parents=True,exist_ok=True)
            data={'schema':1,'enabled':self.enabled,'scope':self._scope,'day':self.day,'counts':self.counts}
            with tempfile.NamedTemporaryFile(mode='w',dir=self.path.parent,prefix='.scorer-usage-',delete=False) as out:
                temporary=Path(out.name);json.dump(data,out,separators=(',',':'));out.flush();os.fsync(out.fileno())
            os.replace(temporary,self.path);self.last_error='';return True
        except OSError:
            self.last_error='Unable to save statistics settings. Please try again.';return False
        finally:
            if temporary:
                try:temporary.unlink(missing_ok=True)
                except OSError:pass

    def set_enabled(self,enabled):
        if type(enabled) is not bool:return False
        with self._lock:
            old=(self.enabled,self.counts,self.day)
            self.enabled=enabled;self.counts={} if not enabled else dict(self.counts);self.day=self._today()
            if not enabled:self._generation+=1
            if not self._save():
                if enabled:
                    self.enabled,self.counts,self.day=old;return False
                # Withdrawal stops collection now, even with full/read-only storage.
                # Removing the old opt-in file also makes the next launch fail closed.
                try:self.path.unlink(missing_ok=True);self.last_error='';return True
                except OSError:
                    self.last_error='Statistics stopped for this session. Unable to save the choice; please try again.'
                    return False
            if enabled:self._generation+=1
        if enabled and self._session_seen:self.begin_session()
        return True

    def begin_session(self):
        self._session_seen=True
        if self.enabled and not self._session_counted:
            if self.record('sessions'):self._session_counted=True

    def end_session(self):
        # Android can kill a process without on_stop: never invent a completion.
        with self._lock:
            if not self._session_counted or self._session_ended:return False
            if self.record('sessions_ended'):
                self._session_ended=True;return True
            return False

    def record(self,event,amount=1):
        if not isinstance(event,str) or event not in EVENTS or type(amount) is not int or not 0<amount<=MAX_COUNT:return False
        with self._lock:
            if not self.enabled:return False
            old=self.counts;old_day=self.day
            age=(date.fromisoformat(self._today())-date.fromisoformat(self.day)).days
            self.counts=dict(self.counts) if 0<=age<=7 else {};self.day=self._today() if age<0 or age>7 else self.day
            self.counts[event]=min(MAX_COUNT,self.counts.get(event,0)+amount)
            if not self._save():self.counts=old;self.day=old_day;return False
            return True

    def flush_async(self):
        with self._lock:
            if not self.enabled or not self.remote_available or not self.counts:return False
            if self._sending:
                self._flush_requested=True;return False
            age=(date.fromisoformat(self._today())-date.fromisoformat(self.day)).days
            if age<0 or age>7:
                self.counts={};self.day=self._today();self._save();return False
            counts=dict(self.counts);generation=self._generation;self._sending=True
        def upload():
            try:
                with self._lock:
                    if not self.enabled or generation!=self._generation:return
                payload={'schema':1,'app':'scorer_free','counts':counts}
                ok=self._sender(self.endpoint,payload)
                with self._lock:
                    if ok and self.enabled and generation==self._generation:
                        previous=self.counts
                        self.counts={key:value-counts.get(key,0) for key,value in self.counts.items() if value-counts.get(key,0)>0}
                        if not self._save():self.counts=previous
            except Exception:pass
            finally:
                with self._lock:
                    self._sending=False
                    again=self._flush_requested;self._flush_requested=False
                # At most the explicitly requested follow-up, not an offline retry loop.
                if again:self.flush_async()
        try:threading.Thread(target=upload,name='scorer-usage',daemon=True).start();return True
        except RuntimeError:
            with self._lock:self._sending=False
            return False


def create_statistics(world,directory,endpoint=None):
    if endpoint is None:
        from analytics_config import ENDPOINT
        endpoint=ENDPOINT
    return UsageStatistics(directory,endpoint)
