"""Bundle the small dashboard-only patch, pinning known prior installed files."""
import argparse,base64,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def build(output):
 files=('server/usage_collector.py','server/dashboard.html','server/management.html')
 payload={name:{'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),'data':base64.b64encode((ROOT/name).read_bytes()).decode()} for name in files}
 baseline=json.loads((ROOT/'docs/data/activity_stats/baseline.json').read_text())['files']
 packed=base64.b64encode(json.dumps(payload,separators=(',',':'),sort_keys=True).encode()).decode()
 text=(ROOT/'server/install_activity_dashboard.py').read_text().replace('PAYLOAD=None','PAYLOAD='+repr(packed)).replace('BASELINE=None','BASELINE='+repr(dict(sorted(baseline.items()))))
 Path(output).write_text(text)
 print(hashlib.sha256(text.encode()).hexdigest(),output)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);build(p.parse_args().output)
