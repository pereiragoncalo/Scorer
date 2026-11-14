"""Show all consented seasons on the existing division boards; preserve database."""
import argparse,base64,hashlib,json,os,shutil,subprocess,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=('server/division_records.py',)
PAYLOAD='eyJzZXJ2ZXIvZGl2aXNpb25fcmVjb3Jkcy5weSI6eyJkYXRhIjoiSWlJaVJYaHdiR2xqYVhSc2VTQnpkV0p0YVhSMFpXUWdZMjl0Y0d4bGRHVmtJSE5sWVhOdmJuTXNJSEJ2YjJ4bFpDQmhZM0p2YzNNZ1kyOTFiblJ5YVdWeklHSjVJR1JwZG1semFXOXVMaUlpSWdwcGJYQnZjblFnYUdGemFHeHBZZ3BtY205dElHUmhkR1YwYVcxbElHbHRjRzl5ZENCa1lYUmxkR2x0WlN4MGFXMWxlbTl1WlFwbWNtOXRJR1JwZG1semFXOXVYM0psWTI5eVpITWdhVzF3YjNKMElIWmhiR2xrWDNKbFkyOXlaQXBtY205dElITmxjblpsY2k1elpXRnpiMjVmY21WamIzSmtjeUJwYlhCdmNuUWdhV1JsYm5ScGRIa0tDbVJsWmlCcGJtbDBhV0ZzYVhwbEtHUmlLVG9LSUNBZ0lHUmlMbVY0WldOMWRHVW9KeWNuUTFKRlFWUkZJRlJCUWt4RklFbEdJRTVQVkNCRldFbFRWRk1nWkdsMmFYTnBiMjVmY21WamIzSmtjeWh2ZDI1bGNpQlVSVmhVTEdScGRtbHphVzl1SUVsT1ZFVkhSVklzYzJWaGMyOXVJRWxPVkVWSFJWSXNjR3hoZVdWeUlGUkZXRlFzWjI5aGJITWdTVTVVUlVkRlVpeHpkR0YwWlNCVVJWaFVJRTVQVkNCT1ZVeE1MR052Ym5ObGJuUWdTVTVVUlVkRlVpQk9UMVFnVGxWTVRDeDFjR1JoZEdWa0lGUkZXRlFnVGs5VUlFNVZURXdzVUZKSlRVRlNXU0JMUlZrb2IzZHVaWElzWkdsMmFYTnBiMjRzYzJWaGMyOXVLU2tuSnljcENpQWdJQ0FqSUVWNGFYTjBhVzVuSUdWNGNHeHBZMmwwSUhObFlYTnZiaUJqYUc5cFkyVnpJR0psWTI5dFpTQjJhWE5wWW14bE95QnlaV3BsWTNSbFpDQnlaV052Y21SeklITjBZWGtnY21WdGIzWmxaQzRLSUNBZ0lHUmlMbVY0WldOMWRHVW9JbFZRUkVGVVJTQmthWFpwYzJsdmJsOXlaV052Y21SeklGTkZWQ0J6ZEdGMFpUMG5ZWEJ3Y205MlpXUW5JRmRJUlZKRklITjBZWFJsUFNkd1pXNWthVzVuSnlCQlRrUWdZMjl1YzJWdWREMHhJaWtLQ21SbFppQnpkV0p0YVhRb1pHSXNjR0Y1Ykc5aFpDazZDaUFnSUNCcFppQnViM1FnYVhOcGJuTjBZVzVqWlNod1lYbHNiMkZrTEdScFkzUXBJRzl5SUhObGRDaHdZWGxzYjJGa0tTRTlleWQwYjJ0bGJpY3NKM0psWTI5eVpDY3NKMk52Ym5ObGJuUmZkbVZ5YzJsdmJpZDlJRzl5SUhSNWNHVW9jR0Y1Ykc5aFpGc25ZMjl1YzJWdWRGOTJaWEp6YVc5dUoxMHBhWE1nYm05MElHbHVkQ0J2Y2lCd1lYbHNiMkZrV3lkamIyNXpaVzUwWDNabGNuTnBiMjRuWFNFOU1TQnZjaUJ1YjNRZ2RtRnNhV1JmY21WamIzSmtLSEJoZVd4dllXUmJKM0psWTI5eVpDZGRLVHB5WVdselpTQldZV3gxWlVWeWNtOXlLQ2RKYm5aaGJHbGtJSE5sWVhOdmJpQmpiMjV6Wlc1MEp5a0tJQ0FnSUdaeWIyMGdjMlZ5ZG1WeUxtMXZaR1Z5WVhScGIyNGdhVzF3YjNKMElIQjFZbXhwWTE5cFpBb2dJQ0FnYjNkdVpYSTlhV1JsYm5ScGRIa29jR0Y1Ykc5aFpGc25kRzlyWlc0blhTazdjajF3WVhsc2IyRmtXeWR5WldOdmNtUW5YVHR3ZFdKc2FYTm9aWEk5Y0hWaWJHbGpYMmxrS0c5M2JtVnlLUW9nSUNBZ2FXWWdaR0l1WlhobFkzVjBaU2duVTBWTVJVTlVJREVnUmxKUFRTQmlZVzV1WldSZmNIVmliR2x6YUdWeWN5QlhTRVZTUlNCd2RXSnNhWE5vWlhJOVB5Y3NLSEIxWW14cGMyaGxjaXdwS1M1bVpYUmphRzl1WlNncE9uSmhhWE5sSUZCbGNtMXBjM05wYjI1RmNuSnZjaWduVTNWemNHVnVaR1ZrSnlrS0lDQWdJRzlzWkQxa1lpNWxlR1ZqZFhSbEtDZFRSVXhGUTFRZ2NHeGhlV1Z5TEdkdllXeHpMSE4wWVhSbElFWlNUMDBnWkdsMmFYTnBiMjVmY21WamIzSmtjeUJYU0VWU1JTQnZkMjVsY2owL0lFRk9SQ0JrYVhacGMybHZiajAvSUVGT1JDQnpaV0Z6YjI0OVB5Y3NLRzkzYm1WeUxISmJKMlJwZG1semFXOXVKMTBzY2xzbmMyVmhjMjl1SjEwcEtTNW1aWFJqYUc5dVpTZ3BDaUFnSUNCcFppQnZiR1FnWVc1a0lHOXNaRnM2TWwwOVBTaHlXeWR3YkdGNVpYSW5YU3h5V3lkbmIyRnNjeWRkS1RvS0lDQWdJQ0FnSUNCcFppQnZiR1JiTWwwOVBTZHlaV3BsWTNSbFpDYzZjbUZwYzJVZ1VHVnliV2x6YzJsdmJrVnljbTl5S0NkU1pXTnZjbVFnY21WdGIzWmxaQ2NwQ2lBZ0lDQWdJQ0FnY21WMGRYSnVDaUFnSUNCa1lpNWxlR1ZqZFhSbEtDSkpUbE5GVWxRZ1NVNVVUeUJrYVhacGMybHZibDl5WldOdmNtUnpJRlpCVEZWRlV5Zy9MRDhzUHl3L0xEOHNKMkZ3Y0hKdmRtVmtKeXd4TEQ4cElFOU9JRU5QVGtaTVNVTlVLRzkzYm1WeUxHUnBkbWx6YVc5dUxITmxZWE52YmlrZ1JFOGdWVkJFUVZSRklGTkZWQ0J3YkdGNVpYSTlaWGhqYkhWa1pXUXVjR3hoZVdWeUxHZHZZV3h6UFdWNFkyeDFaR1ZrTG1kdllXeHpMSE4wWVhSbFBTZGhjSEJ5YjNabFpDY3NZMjl1YzJWdWREMHhMSFZ3WkdGMFpXUTlaWGhqYkhWa1pXUXVkWEJrWVhSbFpDSXNLRzkzYm1WeUxISmJKMlJwZG1semFXOXVKMTBzY2xzbmMyVmhjMjl1SjEwc2Nsc25jR3hoZVdWeUoxMHNjbHNuWjI5aGJITW5YU3hrWVhSbGRHbHRaUzV1YjNjb2RHbHRaWHB2Ym1VdWRYUmpLUzVwYzI5bWIzSnRZWFFvS1NrcENncGtaV1lnYkdWaFpHVnljeWhrWWl4a2FYWnBjMmx2YmlrNkNpQWdJQ0JwWmlCMGVYQmxLR1JwZG1semFXOXVLV2x6SUc1dmRDQnBiblFnYjNJZ1pHbDJhWE5wYjI0Z2JtOTBJR2x1SUNneExESXBPbkpoYVhObElGWmhiSFZsUlhKeWIzSW9KMGx1ZG1Gc2FXUWdaR2wyYVhOcGIyNG5LUW9nSUNBZ1puSnZiU0J6WlhKMlpYSXViVzlrWlhKaGRHbHZiaUJwYlhCdmNuUWdjSFZpYkdsalgybGtDaUFnSUNCeWIzZHpQV1JpTG1WNFpXTjFkR1VvSWxORlRFVkRWQ0J2ZDI1bGNpeHdiR0Y1WlhJc1oyOWhiSE1zYzJWaGMyOXVJRVpTVDAwZ1pHbDJhWE5wYjI1ZmNtVmpiM0prY3lCWFNFVlNSU0JrYVhacGMybHZiajAvSUVGT1JDQnpkR0YwWlQwbllYQndjbTkyWldRbklFRk9SQ0JqYjI1elpXNTBQVEVnVDFKRVJWSWdRbGtnWjI5aGJITWdSRVZUUXl4elpXRnpiMjRnUVZORExIQnNZWGxsY2lCQlUwTXNiM2R1WlhJZ1FWTkRJaXdvWkdsMmFYTnBiMjRzS1NrdVptVjBZMmhoYkd3b0tRb2dJQ0FnWlc1MGNtbGxjejFiWFFvZ0lDQWdabTl5SUc5M2JtVnlMSEJzWVhsbGNpeG5iMkZzY3l4elpXRnpiMjRnYVc0Z2NtOTNjem9LSUNBZ0lDQWdJQ0J3ZFdKc2FYTm9aWEk5Y0hWaWJHbGpYMmxrS0c5M2JtVnlLUW9nSUNBZ0lDQWdJR2xtSUdSaUxtVjRaV04xZEdVb0oxTkZURVZEVkNBeElFWlNUMDBnWW1GdWJtVmtYM0IxWW14cGMyaGxjbk1nVjBoRlVrVWdjSFZpYkdsemFHVnlQVDhuTENod2RXSnNhWE5vWlhJc0tTa3VabVYwWTJodmJtVW9LVHBqYjI1MGFXNTFaUW9nSUNBZ0lDQWdJR1Z1ZEhKcFpYTXVZWEJ3Wlc1a0tHUnBZM1FvY0d4aGVXVnlQWEJzWVhsbGNpeG5iMkZzY3oxbmIyRnNjeXh3ZFdKc2FYTm9aWEk5Y0hWaWJHbHphR1Z5S1NrS0lDQWdJQ0FnSUNCcFppQnNaVzRvWlc1MGNtbGxjeWsrUFRFd01EcGljbVZoYXdvZ0lDQWdjbVYwZFhKdUlHUnBZM1FvYzJOb1pXMWhQVFVzWkdsMmFYTnBiMjQ5WkdsMmFYTnBiMjRzZG1WeWFXWnBaV1E5Um1Gc2MyVXNaVzUwY21sbGN6MWxiblJ5YVdWektRbz0iLCJzaGEyNTYiOiI2NTlkMTQ0MjZmZWFmMDM3NDEwNGZjYmViMzVkMGUwODVjOGFiNDU4MDQ4NmNkZGFjYTFhZWExMWIxNzJiZDA1In19'
BASELINE={'server/division_records.py': ['d7905867c7f7517329456c2c08e98afe73bc3a46c3c9feff2a0e26f70b7d3888', 'c1b926cee69422242d06b363fc363ca0cd5c776af90e552281a567b850940986']}

def sources():
 if PAYLOAD is None:return {name:(ROOT/name).read_bytes() for name in FILES}
 packed=json.loads(base64.b64decode(PAYLOAD));data={k:base64.b64decode(v['data']) for k,v in packed.items()}
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
 if set(payload)!=set(FILES):raise ValueError('Incomplete season-board patch')
 for name,raw in payload.items():compile(raw,name,'exec')

def apply(root,payload,stop,start,check,baseline=None):
 root=Path(root).resolve();preflight(payload);previous={};unknown=[]
 for name,raw in payload.items():
  path=root/name
  if path.is_symlink() or path.parent.resolve() not in (root,root/'server'):raise ValueError('Unsafe target')
  previous[name]=path.read_bytes() if path.exists() else None
  if baseline is not None and previous[name] is not None:
   digest=hashlib.sha256(previous[name]).hexdigest()
   if digest not in (*baseline.get(name,[]),hashlib.sha256(raw).hexdigest()):unknown.append(name+' (SHA256 '+digest+')')
 if unknown:raise ValueError('Installed files differ from known versions; nothing changed: '+'; '.join(unknown))
 if any(previous[n] is None for n in FILES[:2]):raise ValueError('Existing Scorer service required')
 if all(previous[n]==payload[n] for n in FILES):check();return None
 backup=Path(tempfile.mkdtemp(prefix='scorer-season-board-backup-',dir=root.parent));os.chmod(backup,0o700)
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
 client=build_opener(ProxyHandler({}));last=None
 for _ in range(20):
  try:
   with client.open(f'http://127.0.0.1:{port}/health',timeout=2) as r:
    if json.load(r).get('ok') is not True:raise ValueError('Health check failed')
   for division in (1,2):
    with client.open(f'http://127.0.0.1:{port}/v5/records?division={division}',timeout=2) as r:
     data=json.load(r)
     if data.get('schema')!=5 or data.get('division')!=division:raise ValueError('Invalid division response')
   for version in (3,4):
    with client.open(f'http://127.0.0.1:{port}/v{version}/records?edition=world&country=England&division=1',timeout=2) as r:
     if json.load(r).get('schema')!=version:raise ValueError('Legacy records unavailable')
   return
  except Exception as e:last=e;time.sleep(.25)
 raise RuntimeError('Season-board verification failed') from last

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args();payload=sources();preflight(payload)
 if a.check:print('Season-board payload verified; no service or data changed.');return
 if os.geteuid()!=0:raise SystemExit('Run on bastion as root')
 backup=apply('/opt/scorer',payload,lambda:control('stop'),lambda:control('start'),lambda:verify(8787),BASELINE)
 print('All published seasons are now listed; existing database records retained.')
 if backup:print('Previous files backed up:',backup)
 print('Existing database, token, game collection settings and update minimum retained.')
if __name__=='__main__':main()
