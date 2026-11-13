"""Bundle the small dashboard-only patch, pinning known prior installed files."""
import argparse,base64,gzip,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def build(output):
 files=('server/usage_collector.py','server/dashboard.html','server/management.html')
 payload={name:{'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),'data':base64.b64encode((ROOT/name).read_bytes()).decode()} for name in files}
 baseline={name:hashlib.sha256(subprocess.check_output(['git','show','255d64a:'+name],cwd=ROOT)).hexdigest() for name in files[:2]}
 packed=base64.b64encode(gzip.compress(json.dumps(payload).encode(),mtime=0)).decode()
 text=(ROOT/'server/install_activity_dashboard.py').read_text().replace('PAYLOAD=None','PAYLOAD='+repr(packed)).replace('BASELINE=None','BASELINE='+repr(baseline))
 Path(output).write_text(text)
 print(hashlib.sha256(text.encode()).hexdigest(),output)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);build(p.parse_args().output)
