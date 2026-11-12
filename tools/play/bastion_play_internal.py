"""Owner-side, certificate/payload-pinned Scorer upload to Play INTERNAL only.

Python stdlib + OpenSSL + JDK. Credentials/private keys stay on owner bastion.
No production-track/listing/tester/financial APIs. No live credentials in tests.
"""
import argparse,base64,fcntl,hashlib,json,os,re,shutil,ssl,stat,subprocess,sys,tempfile,time,zipfile
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.parse import urlencode,urlsplit,quote
from urllib.request import Request,build_opener,HTTPRedirectHandler

PACKAGE='com.clemir.scorerworld'
VERSION=1030011
TRACK='internal'
BASE='https://androidpublisher.googleapis.com/androidpublisher/v3/applications/'+PACKAGE+'/edits'
TOKEN_URL='https://oauth2.googleapis.com/token'
SCOPE='https://www.googleapis.com/auth/androidpublisher'
CERT='2259de229b49bb40e158d3c015fe1e0d2426becb4e1a4f110dbcd183b51e59a0'
PAYLOAD='da17771e3c4ef5422c343f29e07728b5734f4871c2862f5c7af7c087ed340cf9'
SIGNED=Path('/home/clemir/Scorer-World-1.0-1030011.aab')
PRIVATE=Path('/root/scorer-signing')
CREDENTIALS=PRIVATE/'google-play-service-account.json'
BOOTSTRAP_URL='https://github.com/pereiragoncalo/Scorer/releases/download/world-1.0-1030011/bastion_bundle_1030011.py'
BOOTSTRAP_SHA='3da383dc3f56f8308d3bf0d652dd51f235dcf328671af34081cd0e00a9fc85e0'
CHUNK=8*1024*1024  # Multiple of256KiB; never send an entire117MiB request.

class Stop(RuntimeError):pass
class APIError(Stop):
    def __init__(self,status,message,retry_after=None):self.status=status;self.retry_after=retry_after;super().__init__('Google API HTTP '+str(status)+': '+message)
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def protected_file(path):
    path=Path(path);info=path.lstat()
    if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode)&0o077 or info.st_uid!=os.getuid():
        raise Stop('Credential must be an owned regular file with mode0600: '+str(path))
    return path


def private_directory(path):
    path=Path(path)
    if not path.exists():path.mkdir(mode=0o700,parents=True)
    info=path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid!=os.getuid() or stat.S_IMODE(info.st_mode)&0o077:
        raise Stop('Use an owned private directory with mode0700: '+str(path))
    return path


def load_account(path):
    path=protected_file(path)
    with path.open(encoding='utf8') as f:data=json.load(f)
    if data.get('type')!='service_account' or not re.fullmatch(r'[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.iam\.gserviceaccount\.com',data.get('client_email','')):
        raise Stop('Expected a Google service-account JSON key, not an upload keystore')
    if not isinstance(data.get('private_key'),str) or not data['private_key'].startswith('-----BEGIN PRIVATE KEY-----'):
        raise Stop('Service-account private key missing')
    if data.get('token_uri',TOKEN_URL)!=TOKEN_URL:raise Stop('Unexpected Google OAuth token endpoint')
    return data


def jwt(account,now=None):
    now=int(time.time() if now is None else now)
    encode=lambda raw:base64.urlsafe_b64encode(raw).rstrip(b'=')
    header={'alg':'RS256','typ':'JWT'}
    if account.get('private_key_id'):header['kid']=account['private_key_id']
    claims={'iss':account['client_email'],'scope':SCOPE,'aud':TOKEN_URL,'iat':now,'exp':now+3500}
    unsigned=encode(json.dumps(header,separators=(',',':')).encode())+b'.'+encode(json.dumps(claims,separators=(',',':')).encode())
    with tempfile.TemporaryDirectory(prefix='scorer-oauth-') as directory:
        key=Path(directory)/'key.pem';key.write_text(account['private_key']);key.chmod(0o600)
        result=subprocess.run(['openssl','dgst','-sha256','-sign',str(key)],input=unsigned,capture_output=True)
        if result.returncode:raise Stop('OpenSSL could not sign Google OAuth assertion')
    return (unsigned+b'.'+encode(result.stdout)).decode()


class Client:
    def __init__(self,account):
        self.account=account;self.token='';self.expires=0;self.opener=build_opener(NoRedirect())
    def request(self,method,url,body=None,headers=None,accepted=(200,),auth=True):
        parsed=urlsplit(url)
        hosts=('androidpublisher.googleapis.com','www.googleapis.com') if auth else ('oauth2.googleapis.com',)
        if parsed.scheme!='https' or parsed.hostname not in hosts or parsed.port not in (None,443) or parsed.username or parsed.password or parsed.fragment:
            raise Stop('Refusing untrusted API/upload endpoint')
        headers=dict(headers or {})
        if auth:
            if self.expires<time.time()+90:self.refresh()
            headers['Authorization']='Bearer '+self.token
        request=Request(url,data=body,headers=headers,method=method)
        try:
            response=self.opener.open(request,timeout=120)
        except HTTPError as error:response=error
        with response:
            raw=response.read(1024*1024);status=response.code;reply_headers=response.headers
        if status not in accepted:
            message='Request rejected; check API enablement and app-specific Play permissions'
            try:
                data=json.loads(raw);error=data.get('error');message=error.get('message',message) if isinstance(error,dict) else data.get('error_description',message)
            except (ValueError,AttributeError):pass
            # Never expose bearer tokens, signed JWT assertions, or service-account keys.
            for secret in (self.token,self.account.get('private_key','')):
                if secret:message=message.replace(secret,'[redacted]')
            message=re.sub(r'eyJ[A-Za-z0-9_.-]{40,}','[redacted]',message)
            raise APIError(status,message[:500],reply_headers.get('Retry-After'))
        return status,reply_headers,json.loads(raw) if raw and status!=308 else {}
    def refresh(self):
        body=urlencode({'grant_type':'urn:ietf:params:oauth:grant-type:jwt-bearer','assertion':jwt(self.account)}).encode()
        _,_,data=self.request('POST',TOKEN_URL,body,{'Content-Type':'application/x-www-form-urlencoded'},auth=False)
        if not isinstance(data.get('access_token'),str) or not data['access_token']:raise Stop('Google returned no OAuth access token')
        self.token=data['access_token'];self.expires=time.time()+int(data.get('expires_in',3500))
    def api(self,method,url,body=None):
        encoded=json.dumps(body).encode() if body is not None else (b'' if method in ('POST','PUT') else None)
        return self.request(method,url,encoded,{'Content-Type':'application/json'},accepted=(200,201,204))[2]


def payload_digest(path):
    h=hashlib.sha256()
    with zipfile.ZipFile(path) as archive:
        infos=archive.infolist()
        if len({i.filename for i in infos})!=len(infos):raise Stop('Duplicate AAB ZIP entries')
        if not {'BundleConfig.pb','base/manifest/AndroidManifest.xml'}.issubset(archive.namelist()):raise Stop('Not an Android App Bundle')
        for info in sorted(infos,key=lambda i:i.filename):
            if info.is_dir():continue
            upper=info.filename.upper()
            if upper.startswith('META-INF/') and (upper=='META-INF/MANIFEST.MF' or upper.endswith(('.RSA','.SF','.EC','.DSA'))):continue
            digest=hashlib.sha256()
            with archive.open(info) as stream:
                for chunk in iter(lambda:stream.read(1024*1024),b''):digest.update(chunk)
            name=info.filename.encode();h.update(len(name).to_bytes(4,'big'));h.update(name);h.update(digest.digest())
    return h.hexdigest()


def verify_signed(path):
    path=Path(path)
    if not path.is_file() or path.is_symlink():raise Stop('Signed AAB not found: '+str(path))
    if payload_digest(path)!=PAYLOAD:raise Stop('AAB payload is not the approved1030011 build')
    for tool in ('jarsigner','keytool'):
        if not shutil.which(tool):raise Stop('Full JDK required: missing '+tool)
    result=subprocess.run(['jarsigner','-verify',str(path)],capture_output=True,text=True)
    if result.returncode:raise Stop('Signed AAB signature verification failed')
    result=subprocess.run(['keytool','-printcert','-rfc','-jarfile',str(path)],capture_output=True,text=True)
    certificates=re.findall(r'-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----',result.stdout,re.S)
    if result.returncode or not certificates:raise Stop('AAB upload certificate missing')
    actual={hashlib.sha256(ssl.PEM_cert_to_DER_cert(pem)).hexdigest() for pem in certificates}
    if CERT not in actual:raise Stop('AAB does not use the existing owner upload certificate')
    return sha(path)


def snapshot_signed(source,directory):
    """Verify/upload the same private snapshot, not a replaceable SFTP pathname."""
    target=Path(directory)/'bundle.aab'
    fd=os.open(source,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):raise Stop('AAB must be a regular file')
        output=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(output,'wb') as destination:shutil.copyfileobj(stream,destination)
    return target


def prepare_signed():
    if SIGNED.exists():return  # verify_signed validates before any API mutation.
    with tempfile.TemporaryDirectory(prefix='scorer-play-download-') as directory:
        helper=Path(directory)/'prepare.py'
        # GitHub release redirects are expected here, without any Google credentials.
        with build_opener().open(BOOTSTRAP_URL,timeout=90) as source,helper.open('xb') as target:
            shutil.copyfileobj(source,target)
        if sha(helper)!=BOOTSTRAP_SHA:raise Stop('Signing coordinator checksum mismatch')
        subprocess.run([sys.executable,str(helper)],check=True)


def upload(client,edit,path):
    total=path.stat().st_size
    endpoint='https://androidpublisher.googleapis.com/resumable/upload/androidpublisher/v3/applications/'+PACKAGE+'/edits/'+quote(edit,safe='')+'/bundles?uploadType=resumable'
    _,headers,_=client.request('POST',endpoint,b'',{'Content-Type':'application/json','X-Upload-Content-Type':'application/octet-stream','X-Upload-Content-Length':str(total)},accepted=(200,201))
    session=headers.get('Location')
    if not session:raise Stop('Google returned no resumable upload session')
    offset=0;failures=0
    with path.open('rb') as source:
        while True:
            source.seek(offset);chunk=source.read(CHUNK)
            try:
                status,headers,data=client.request('PUT',session,chunk,{'Content-Type':'application/octet-stream','Content-Range':f'bytes {offset}-{offset+len(chunk)-1}/{total}'},accepted=(200,201,308))
            except (URLError,TimeoutError,OSError,APIError) as error:
                if isinstance(error,APIError) and error.status not in (429,500,502,503,504):raise
                failures+=1
                if failures>3:raise Stop('Upload interrupted; no release committed. Rerun after checking connection') from None
                try:delay=int(getattr(error,'retry_after',None) or min(failures,3))
                except ValueError:delay=1
                if delay>30:raise Stop('Google rate limit: retry later. No release committed') from None
                time.sleep(max(0,delay))
                # Query server offset; never blindly resend a possibly accepted chunk.
                status,headers,data=client.request('PUT',session,b'',{'Content-Length':'0','Content-Range':f'bytes */{total}'},accepted=(200,201,308))
            if status in (200,201):return data
            matched=re.fullmatch(r'bytes=0-(\d+)',headers.get('Range',''))
            received=int(matched.group(1))+1 if matched else 0
            if not 0<=received<=min(total,offset+len(chunk)) or received==total:raise Stop('Invalid resumable upload offset')
            if received==offset:
                failures+=1
                if failures>3:raise Stop('Resumable upload made no progress; no release committed')
            else:failures=0
            offset=received
            print('Uploaded '+str(offset//(1024*1024))+' MiB',flush=True)


def version_codes(track):
    return [int(code) for release in track.get('releases',[]) for code in release.get('versionCodes',[])]


def internal_release():
    return {'track':TRACK,'releases':[{'name':'1.0 (1030011) - rebuild with installed version code','versionCodes':[str(VERSION)],'status':'completed','releaseNotes':[{'language':'en-US','text':'Rebuilt with visible installed version code. Retains home-colour chairs, seated fans and empty training seats.'}]}]}


def publish(client,path,signed_sha,check_only=False):
    edit=client.api('POST',BASE,{})['id'];edit_url=BASE+'/'+quote(edit,safe='');commit_attempted=False
    try:
        track=client.api('GET',edit_url+'/tracks/'+TRACK)
        codes=version_codes(track)
        if check_only:
            print('Play API connected: '+PACKAGE+'; internal versions: '+str(codes));return 'checked'
        if any(code>VERSION for code in codes):raise Stop('Internal track contains a newer version; refusing downgrade')
        bundles=client.api('GET',edit_url+'/bundles').get('bundles',[])
        existing=next((row for row in bundles if int(row['versionCode'])==VERSION),None)
        if existing:
            if existing.get('sha256','').lower()!=signed_sha:raise Stop('Version1030011 already exists with another SHA256; do not reuse a version code')
            if any(str(VERSION) in release.get('versionCodes',[]) and release.get('status')=='completed' for release in track.get('releases',[])):
                print('Version1030011 is already committed to internal; no change made');return 'unchanged'
            result=existing
        else:result=upload(client,edit,path)
        if int(result.get('versionCode',0))!=VERSION or result.get('sha256','').lower()!=signed_sha:
            raise Stop('Google bundle version/SHA256 differs; no release committed')
        updated=client.api('PUT',edit_url+'/tracks/'+TRACK,internal_release())
        if updated.get('track')!=TRACK or version_codes(updated)!=[VERSION]:raise Stop('Unexpected internal release response; no commit')
        client.api('POST',edit_url+':validate')
        print('Bundle and internal release validated; committing internal edit',flush=True)
        commit_attempted=True
        # Internal testing uses this app's automatic review mode. The owner-observed
        #400 explicitly forbids changesNotSentForReview; omit it, but NEVER cancel a review.
        query=urlencode({'changesInReviewBehavior':'ERROR_IF_IN_REVIEW'})
        try:client.api('POST',edit_url+':commit?'+query)
        except (URLError,TimeoutError,OSError,APIError) as error:
            if isinstance(error,APIError) and error.status<500:raise
            raise Stop('Commit response was lost: outcome uncertain. Check internal track in Console before retrying') from None
        print('Committed INTERNAL version1030011. Play availability/review timing is controlled by Google.')
        return 'committed'
    finally:
        if not commit_attempted:
            try:client.api('DELETE',edit_url)
            except (Stop,URLError,OSError):print('Temporary edit cleanup not confirmed; it expires without publishing',file=sys.stderr)


def install_credentials(source):
    private_directory(PRIVATE)
    source=Path(source)
    # Uploaded source must sit inside an owned private directory, not a public home folder.
    info=source.parent.stat()
    if stat.S_IMODE(info.st_mode)&0o077:raise Stop('Upload JSON into a private0700 folder first')
    if source.is_symlink() or not source.is_file():raise Stop('Credential source must be a regular JSON file')
    if source.stat().st_size>65536:raise Stop('Unexpected credential file size')
    raw=source.read_bytes()
    if os.path.lexists(CREDENTIALS):
        existing=load_account(CREDENTIALS)
        if CREDENTIALS.read_bytes()!=raw:raise Stop('Google credential already installed; refusing replacement')
        print('Identical Google credential already installed: '+existing['client_email']);return
    created=False
    try:
        with CREDENTIALS.open('xb') as target:
            created=True;CREDENTIALS.chmod(0o600);target.write(raw);target.flush();os.fsync(target.fileno())
        data=load_account(CREDENTIALS)
    except Exception:
        if created:CREDENTIALS.unlink(missing_ok=True)
        raise
    print('Private Google account installed: '+data['client_email'])
    print('Source remains in its private folder; remove the source copy after verifying setup.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check',action='store_true');mode.add_argument('--publish',action='store_true')
    mode.add_argument('--install-credentials',type=Path);mode.add_argument('--setup-folder',action='store_true')
    args=parser.parse_args();private_directory(PRIVATE)
    if args.setup_folder:
        import pwd
        owner=pwd.getpwnam('clemir');folder=Path(tempfile.mkdtemp(prefix='scorer-play-setup-',dir=owner.pw_dir));folder.chmod(0o700);os.chown(folder,owner.pw_uid,owner.pw_gid)
        print('SFTP upload destination (private): '+str(folder));return
    if args.install_credentials:install_credentials(args.install_credentials);return
    account=load_account(CREDENTIALS);client=Client(account)
    # The lock prevents concurrent owner commands from racing upload/commit.
    fd=os.open(PRIVATE/'play-internal.lock',os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'w') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise Stop('Another internal upload is running') from None
        if args.check:publish(client,None,'',check_only=True);return
        prepare_signed()
        with tempfile.TemporaryDirectory(prefix='play-upload-',dir=PRIVATE) as directory:
            bundle=snapshot_signed(SIGNED,directory);digest=verify_signed(bundle)
            print('Local signature, original upload certificate and approved payload verified',flush=True)
            publish(client,bundle,digest)
            print('After Play makes this build available to every intended player, activate the update policy on bastion:')
            print(f'python3 /opt/scorer/server/version_updates.py --minimum {VERSION} --latest {VERSION} --name 1.0')
            print('Verify: curl -f https://stats.clemir.com/v1/app-version')

if __name__=='__main__':
    try:main()
    except (Stop,OSError,ValueError,subprocess.CalledProcessError,zipfile.BadZipFile) as error:
        if isinstance(error,subprocess.CalledProcessError):message='Local preparation command failed; no Play release committed'
        elif isinstance(error,(URLError,TimeoutError)):message='Google connection failed; check connectivity and rerun --check'
        else:message=str(error)
        print('Stopped: '+message,file=sys.stderr);sys.exit(1)
