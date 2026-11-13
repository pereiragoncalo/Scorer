"""Transactional World policy and v4 board update; no Console declaration or rollout."""
import argparse,base64,gzip,hashlib,json,os,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=('server/__init__.py','server/usage_collector.py','server/leaderboard.py','server/season_records.py','server/moderation.py','server/career_records.py','server/privacy_cases.py','privacy_requests.py','anonymous_stats.py','career_records.py','season_records.py','server/public_pages.py','server/configure_public.py','server/dashboard.html','server/management.html','online_safety.py','public.json','version_policy.py','server/version_updates.py','version-policy.json')
PAYLOAD=None

def sources():
 if PAYLOAD is None:return {name:(ROOT/('server/public.world.policy.json' if name=='public.json' else 'server/version-policy.example.json' if name=='version-policy.json' else name)).read_bytes() for name in FILES}
 data=json.loads(gzip.decompress(base64.b64decode(PAYLOAD)))
 result={name:base64.b64decode(row['data']) for name,row in data.items()}
 if set(result)!=set(FILES):raise ValueError('Invalid bundled file list')
 for name,raw in result.items():
  if hashlib.sha256(raw).hexdigest()!=data[name]['sha256']:raise ValueError('Bundled source hash mismatch')
 return result

def write(path,data):
 previous=path.stat() if path.exists() else None
 fd,name=tempfile.mkstemp(prefix='.scorer-career-',dir=path.parent)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.chmod(name,previous.st_mode & 0o777 if previous else 0o644)
  if previous and os.geteuid()==0:os.chown(name,previous.st_uid,previous.st_gid)
  os.replace(name,path)
 finally:
  if os.path.exists(name):os.unlink(name)

def verify(port=8787):
 from urllib.request import build_opener,ProxyHandler
 client=build_opener(ProxyHandler({}));last=None
 for _ in range(12):
  try:
   for version in (3,4):
    with client.open(f'http://127.0.0.1:{port}/v{version}/records?edition=world&country=England&division=1',timeout=3) as r:
     d=json.loads(r.read(65537))
     if r.status!=200 or d.get('schema')!=version or not isinstance(d.get('entries'),list):raise ValueError('Unexpected record response')
   for path in ('privacy','terms','delete'):
    with client.open(f'http://127.0.0.1:{port}/'+path,timeout=3) as r:
     text=r.read(131073).decode('utf8')
     if r.status!=200 or len(text)>131072:raise ValueError('Invalid public page')
     if path=='privacy':
      required=('data-publication-status="published"','From version code 1030005, I AGREE on the startup notice enables aggregate usage statistics.','I DO NOT AGREE closes the game without sending statistics.','Career category')
      if not all(marker in text for marker in required):raise ValueError('Policy version mismatch')
   with client.open(f'http://127.0.0.1:{port}/v1/app-version',timeout=3) as r:
    d=json.loads(r.read(4097))
    if d.get('package')!='com.clemir.scorerworld' or type(d.get('minimum_version_code'))is not int:raise ValueError('Version endpoint failed')
   return
  except Exception as e:last=e;time.sleep(.25)
 raise RuntimeError('Local v3/v4 validation failed') from last

def preflight(payload):
 if set(payload)!=set(FILES):raise ValueError('Incomplete backend payload')
 for name,raw in payload.items():
  if name.endswith('.py'):compile(raw,name,'exec')
  elif name=='public.json':
   config=json.loads(raw)
   if config.get('publication_status')!='published' or config.get('support_email')!='goncalo@clemir.com':raise ValueError('Unexpected policy configuration')
  elif name=='version-policy.json':
   config=json.loads(raw)
   if config.get('schema')!=1 or config.get('package')!='com.clemir.scorerworld' or type(config.get('minimum_version_code'))is not int or not 0<=config['minimum_version_code']<=config.get('latest_version_code',-1):raise ValueError('Invalid minimum version policy')
  elif name in ('server/dashboard.html','server/management.html'):raw.decode('utf8')
  else:raise ValueError('Unexpected payload file')
 # A syntax check alone cannot detect a missing imported module. Use ONLY the
 # delivered files in a fresh isolated Python, without the source checkout.
 with tempfile.TemporaryDirectory(prefix='scorer-backend-preflight-') as directory:
  root=Path(directory)
  for name,raw in payload.items():
   path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
  code="import sys;sys.path.insert(0,sys.argv[1]);from server.usage_collector import Collector;s=Collector(('127.0.0.1',0),sys.argv[1]+'/preflight.sqlite');s.server_close();from version_policy import read;from server.version_updates import policy_path;read(sys.argv[1]+'/version-policy.json');from server.public_pages import page;assert page('/privacy',sys.argv[1]+'/public.json')[0]==200"
  result=subprocess.run([sys.executable,'-I','-B','-c',code,str(root)],capture_output=True,text=True)
  if result.returncode:raise RuntimeError('Backend dependency preflight failed:\n'+result.stderr)

def control_service(action):
 if action=='start':subprocess.run(['systemctl','reset-failed','scorer-online'],check=True)
 subprocess.run(['systemctl',action,'scorer-online'],check=True)

def apply(target,payload,stop,start,check):
 target=Path(target).resolve();previous={};payload=dict(payload)
 for name in ('public.json','version-policy.json'):
  path=target/name
  if path.is_symlink():raise ValueError('Unsafe existing configuration')
  if path.exists():payload[name]=path.read_bytes()
 # Preserve existing operator policy/minimum; only advance the disclosure date.
 config=json.loads(payload['public.json']);disclosure=json.loads(sources()['public.json']);config['legal_basis']=disclosure['legal_basis'];config['children_practices']=disclosure['children_practices'];config.pop('legal_basis_en',None);config.pop('children_practices_en',None);config['effective_date']=max(config.get('effective_date',''),'2026-11-12');payload['public.json']=json.dumps(config,ensure_ascii=False).encode()
 preflight(payload)
 for name,raw in payload.items():
  p=target/name
  if p.is_symlink() or p.parent.resolve() not in (target,target/'server'):raise ValueError('Unsafe target: '+name)
  previous[name]=p.read_bytes() if p.exists() else None
 if previous['server/usage_collector.py'] is None or previous['server/moderation.py'] is None:raise ValueError('Existing v3 Scorer service required')
 stop()
 try:
  for name,raw in payload.items():write(target/name,raw)
  start();check()
 except Exception as original:
  try:
   stop()
   for name,raw in previous.items():
    p=target/name
    if raw is None:p.unlink(missing_ok=True)
    else:write(p,raw)
   start()
  except Exception as rollback:
   raise RuntimeError('Update failed: '+str(original)+'; rollback/restart also failed: '+str(rollback)) from original
  raise

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');parser.add_argument('--target',type=Path,default=Path('/opt/scorer'));parser.add_argument('--port',type=int,default=8787);args=parser.parse_args();payload=sources()
 preflight(payload)
 if args.check:print('Complete backend dependency imports, source hashes, Python syntax and public policy verified. No service or data changed.');return
 if os.geteuid()!=0:raise SystemExit('Run as root on bastion, or use --check.')
 apply(args.target,payload,lambda:control_service('stop'),lambda:control_service('start'),lambda:verify(args.port))
 print('Version-check endpoint and disclosure installed; local v3/v4/public pages preserved and verified.')
 print('Existing minimum, records, tokens, Tunnel and maintenance retained. Check https://stats.clemir.com/v1/app-version externally. A higher minimum must only be activated after the new Play version is available to all intended players.')
if __name__=='__main__':main()
