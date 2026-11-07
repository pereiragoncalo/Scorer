"""Transactional additive v4 career-board update; existing v3 seasons stay intact."""
import argparse,base64,gzip,hashlib,json,os,subprocess,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=('server/usage_collector.py','server/moderation.py','server/career_records.py','career_records.py','season_records.py')
PAYLOAD=None

def sources():
 if PAYLOAD is None:return {name:(ROOT/name).read_bytes() for name in FILES}
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
   return
  except Exception as e:last=e;time.sleep(.25)
 raise RuntimeError('Local v3/v4 validation failed') from last

def apply(target,payload,stop,start,check):
 target=Path(target).resolve();previous={}
 for name,raw in payload.items():
  compile(raw,name,'exec');p=target/name
  if p.is_symlink() or p.parent.resolve() not in (target,target/'server'):raise ValueError('Unsafe target: '+name)
  previous[name]=p.read_bytes() if p.exists() else None
 if previous['server/usage_collector.py'] is None or previous['server/moderation.py'] is None:raise ValueError('Existing v3 Scorer service required')
 stop()
 try:
  for name,raw in payload.items():write(target/name,raw)
  start();check()
 except Exception:
  stop()
  for name,raw in previous.items():
   p=target/name
   if raw is None:p.unlink(missing_ok=True)
   else:write(p,raw)
  start();raise

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');parser.add_argument('--target',type=Path,default=Path('/opt/scorer'));parser.add_argument('--port',type=int,default=8787);args=parser.parse_args();payload=sources()
 for name,raw in payload.items():compile(raw,name,'exec')
 if args.check:print('Career-board source hashes and Python syntax verified. No service or data changed.');return
 if os.geteuid()!=0:raise SystemExit('Run as root on bastion, or use --check.')
 def control(action):subprocess.run(['systemctl',action,'scorer-online'],check=True)
 apply(args.target,payload,lambda:control('stop'),lambda:control('start'),lambda:verify(args.port))
 print('Scorer career board installed: local v3 seasons and v4 career endpoint verified.')
 print('Adds one career-record table. Existing totals, seasonal records, tokens, Tunnel and maintenance settings are retained.')
if __name__=='__main__':main()
