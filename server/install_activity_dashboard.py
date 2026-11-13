"""Install only the 30-day activity dashboard on the existing bastion service."""
import argparse,base64,gzip,hashlib,json,os,shutil,subprocess,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=('server/usage_collector.py','server/dashboard.html','server/management.html')
PAYLOAD=None
BASELINE=None

def sources():
 if PAYLOAD is None:return {name:(ROOT/name).read_bytes() for name in FILES}
 packed=json.loads(gzip.decompress(base64.b64decode(PAYLOAD)));data={k:base64.b64decode(v['data']) for k,v in packed.items()}
 if set(data)!=set(FILES):raise ValueError('Unexpected file list')
 for name,raw in data.items():
  if hashlib.sha256(raw).hexdigest()!=packed[name]['sha256']:raise ValueError('Payload mismatch')
 return data

def write(path,raw):
 previous=path.stat() if path.exists() else None
 fd,name=tempfile.mkstemp(prefix='.activity-',dir=path.parent)
 try:
  with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
  os.chmod(name,previous.st_mode&0o777 if previous else 0o644)
  if previous and os.geteuid()==0:os.chown(name,previous.st_uid,previous.st_gid)
  os.replace(name,path)
 finally:
  if os.path.exists(name):os.unlink(name)

def preflight(payload):
 if set(payload)!=set(FILES):raise ValueError('Incomplete dashboard patch')
 compile(payload['server/usage_collector.py'],'usage_collector.py','exec')
 for name in FILES[1:]:payload[name].decode('utf8')

def apply(root,payload,stop,start,check,baseline=None):
 root=Path(root).resolve();preflight(payload);previous={}
 for name,raw in payload.items():
  path=root/name
  if path.is_symlink() or path.parent.resolve()!=root/'server':raise ValueError('Unsafe target')
  previous[name]=path.read_bytes() if path.exists() else None
  if baseline is not None and previous[name] is not None:
   digest=hashlib.sha256(previous[name]).hexdigest()
   if digest not in (baseline.get(name),hashlib.sha256(raw).hexdigest()):raise ValueError('Installed file differs from known version; nothing changed: '+name)
 if any(previous[n] is None for n in FILES[:2]):raise ValueError('Existing Scorer service required')
 if all(previous[n]==payload[n] for n in FILES):check();return None
 backup=Path(tempfile.mkdtemp(prefix='scorer-activity-backup-',dir=root.parent));os.chmod(backup,0o700)
 for name,raw in previous.items():
  if raw is not None:
   path=backup/name;path.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/name,path)
 stop()
 try:
  for name,raw in payload.items():write(root/name,raw)
  start();check()
 except Exception:
  stop()
  for name,raw in previous.items():
   if raw is None:(root/name).unlink(missing_ok=True)
   else:write(root/name,raw)
  start();raise
 return backup

def control(action):subprocess.run(['systemctl',action,'scorer-online'],check=True)

def verify(port):
 from urllib.request import build_opener,ProxyHandler
 from urllib.error import HTTPError
 client=build_opener(ProxyHandler({}));last=None
 for _ in range(20):
  try:
   with client.open(f'http://127.0.0.1:{port}/health',timeout=2) as r:
    if json.load(r).get('ok') is not True:raise ValueError('Health check failed')
   with client.open(f'http://127.0.0.1:{port}/admin',timeout=2) as r:
    if b'/v1/activity' not in r.read():raise ValueError('Wrong dashboard')
   with client.open(f'http://127.0.0.1:{port}/admin/manage',timeout=2) as r:
    if b'Load moderation' not in r.read():raise ValueError('Missing management')
   try:client.open(f'http://127.0.0.1:{port}/v1/activity',timeout=2)
   except HTTPError as error:
    if error.code!=404:raise
   else:raise ValueError('Activity must require admin authentication')
   return
  except Exception as e:last=e;time.sleep(.25)
 raise RuntimeError('Dashboard verification failed') from last

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args();payload=sources();preflight(payload)
 if a.check:print('Dashboard payload verified; no service or data changed.');return
 if os.geteuid()!=0:raise SystemExit('Run on bastion as root')
 backup=apply('/opt/scorer',payload,lambda:control('stop'),lambda:control('start'),lambda:verify(8787),BASELINE)
 print('Activity dashboard installed: https://stats.clemir.com/admin')
 if backup:print('Previous files backed up:',backup)
 print('Existing database, token, game collection settings and update minimum retained.')
if __name__=='__main__':main()
