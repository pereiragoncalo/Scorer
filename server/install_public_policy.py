"""Install reviewed public-page files/config only; do not touch secrets or SQLite.
The bundled World policy is final English text; Play approval is a separate process.
"""
import argparse,json,os,stat,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from server.public_pages import load_config,page

FILES=('server/public_pages.py','server/configure_public.py','public.json')

def _write(path,data,mode=0o644):
    fd,name=tempfile.mkstemp(prefix='.scorer-policy-',dir=path.parent)
    temporary=Path(name)
    try:
        with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        temporary.chmod(mode);os.replace(temporary,path)
    finally:temporary.unlink(missing_ok=True)

def check(source,config):
    source=Path(source);config=Path(config)
    if config.is_symlink():raise ValueError('Refusing a symlink configuration')
    for name in FILES[:-1]:
        p=source/name
        if not p.is_file() or p.is_symlink():raise ValueError('Public page source is missing or a symlink: '+name)
    d=load_config(config)
    for path in ('/privacy','/terms','/delete'):
        status,body=page(path,config)
        if status!=200:raise ValueError('Public document validation failed: '+path)
        if path=='/privacy' and ('data-publication-status="'+d['publication_status']+'"').encode() not in body:raise ValueError('Declared policy status is missing')
    return d

def apply(source,config,target,stop,start,verify):
    """Transactional update; callbacks make stop/start/rollback testable locally."""
    source=Path(source);target=Path(target);d=check(source,config)
    if not (target/'server/usage_collector.py').is_file():raise ValueError('Install the Scorer server before this public-page update')
    active=target/'public.json'
    if active.is_symlink():raise ValueError('Refusing a symlink public configuration')
    if active.exists():
        try:existing=load_config(active)
        except (OSError,ValueError,TypeError):existing=None
        if existing:
            raw=json.loads(active.read_text(encoding='utf8'))
            if d['publication_status']=='draft' and (existing['publication_status']=='published' or 'publication_status' not in raw):raise ValueError('An existing completed or legacy policy is installed; refusing to replace it with a draft')
    originals={}
    for name in FILES:
        p=target/name
        if p.is_symlink():raise ValueError('Refusing a symlink target: '+name)
        originals[name]=(p.read_bytes(),stat.S_IMODE(p.stat().st_mode)) if p.exists() else None
    replacement={name:(source/name).read_bytes() for name in FILES[:-1]}
    replacement['public.json']=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8')
    stop()
    try:
        for name in FILES:_write(target/name,replacement[name])
        start();verify()
    except BaseException:
        # Stop a partially started service before restoring its previous renderer/config.
        try:stop()
        finally:
            for name,previous in originals.items():
                p=target/name
                if previous is None:p.unlink(missing_ok=True)
                else:_write(p,*previous)
            start()
        raise

def verify_local(expected_status="published"):
    from urllib.request import build_opener,ProxyHandler
    # Loopback service checks must stay on the laptop, not go through any proxy.
    client=build_opener(ProxyHandler({}));last=None
    for _ in range(8):
        try:
            for path in ('/privacy','/terms','/delete'):
                with client.open('http://127.0.0.1:8787'+path,timeout=2) as response:
                    body=response.read(131073)
                    if response.status!=200 or len(body)>131072:raise ValueError('Invalid local document response')
                    if path=='/privacy' and ('data-publication-status="'+expected_status+'"').encode() not in body:raise ValueError('Running service did not load the expected renderer')
            return
        except Exception as error:last=error;time.sleep(.25)
    raise RuntimeError('Local public-page checks failed; the previous files will be restored') from last

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    config=ROOT/'server/public.world.policy.json';check(ROOT,config)
    if args.check:print('Final English World policy validated; /privacy, /terms and /delete render locally. No files or services changed.');return
    if os.geteuid()!=0:raise SystemExit('Run as root on the laptop, or use --check for validation only')
    target=Path('/opt/scorer')
    def control(action):subprocess.run(['systemctl',action,'scorer-online'],check=True)
    apply(ROOT,config,target,lambda:control('stop'),lambda:control('start'),verify_local)
    print('Public-page update complete: local /privacy, /terms and /delete return HTTP200.')
    print('Final English World policy installed. This does not certify Google Play approval or change Console review flags.')
    print('No administrator token, tunnel, maintenance timer, game save or database was read or changed by this installer.')
    print('Check externally: https://stats.clemir.com/privacy · /terms · /delete')

if __name__=='__main__':main()
