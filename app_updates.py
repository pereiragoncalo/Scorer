"""No-ID compatibility check. Offline allowed unless a valid cached minimum blocks."""
import json,os,tempfile,threading
from pathlib import Path
from urllib.request import Request,build_opener,HTTPRedirectHandler,HTTPSHandler
from version_policy import validate,read,blocked,PACKAGE

ENDPOINT='https://stats.clemir.com/v1/app-version'
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def installed_version():
    import release_settings
    fallback=getattr(release_settings,'VERSION_CODE',0)
    try:
        from kivy.utils import platform
        if platform=='android':
            from jnius import autoclass
            activity=autoclass('org.kivy.android.PythonActivity').mActivity
            info=activity.getPackageManager().getPackageInfo(activity.getPackageName(),0)
            if str(activity.getPackageName())!=PACKAGE:return 0
            try:return int(info.getLongVersionCode())
            except Exception:return int(info.versionCode)
    except Exception:pass
    return fallback if type(fallback)is int else 0

def fetch():
    request=Request(ENDPOINT,headers={'User-Agent':'ScorerWorld-VersionCheck/1','Accept':'application/json'})
    from network_tls import verified_context
    with build_opener(NoRedirect(),HTTPSHandler(context=verified_context())).open(request,timeout=4) as response:
        raw=response.read(4097)
    if len(raw)>4096:raise ValueError('Version policy too large')
    return validate(json.loads(raw))

class UpdateState:
    def __init__(self,installed,path):
        self.installed=installed;self.path=Path(path);self.policy=None;self.checking=False;self._lock=threading.Lock();self._generation=0
        try:self.policy=read(self.path)
        except (OSError,ValueError,TypeError):pass
    @property
    def required(self):return blocked(self.policy,self.installed)
    @property
    def locked(self):return self.checking or self.required
    def apply(self,data):
        policy=validate(data)
        # A valid server response can also revoke an accidental mandatory update.
        self.policy=policy
        try:
            self.path.parent.mkdir(parents=True,exist_ok=True)
            fd,name=tempfile.mkstemp(prefix='.version-',dir=self.path.parent)
            try:
                with os.fdopen(fd,'w',encoding='utf8') as stream:json.dump(policy,stream);stream.flush();os.fsync(stream.fileno())
                os.replace(name,self.path)
            finally:
                if os.path.exists(name):os.unlink(name)
        except OSError:pass  # A full disk never clears the current in-memory block.
    def check_async(self,callback,dispatch,fetcher=fetch,timeout=5):
        with self._lock:
            if self.checking:return False
            self.checking=True;self._generation+=1;generation=self._generation
        callback()
        def deliver(result):
            def complete():
                with self._lock:
                    if generation!=self._generation or not self.checking:return
                    self.checking=False;self._generation+=1
                if result is not None:
                    try:self.apply(result)
                    except (ValueError,TypeError):pass
                callback()
            dispatch(complete)
        # Socket timeout alone does not bound a slow DNS resolver. A UI deadline
        # allows offline play and ignores late responses from abandoned checks.
        watchdog=threading.Timer(timeout,lambda:deliver(None));watchdog.daemon=True;watchdog.start()
        def worker():
            try:result=fetcher()
            except Exception:result=None
            watchdog.cancel();deliver(result)
        threading.Thread(target=worker,name='ScorerVersionCheck',daemon=True).start()
        return True
