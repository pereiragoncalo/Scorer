"""Bundle the small dashboard-only patch, pinning known prior installed files."""
import argparse,base64,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

sys.path.insert(0,str(ROOT))

def build(output):
 from server.install_activity_dashboard import FILES
 files=FILES
 payload={name:{'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),'data':base64.b64encode((ROOT/name).read_bytes()).decode()} for name in files}
 baseline=json.loads((ROOT/'docs/data/activity_stats/baseline.json').read_text())['files']
 packed=base64.b64encode(json.dumps(payload,separators=(',',':'),sort_keys=True).encode()).decode()
 text=(ROOT/'server/install_activity_dashboard.py').read_text().replace('PAYLOAD=None','PAYLOAD='+repr(packed)).replace('BASELINE=None','BASELINE='+repr(dict(sorted(baseline.items()))))
 Path(output).write_text(text)
 print(hashlib.sha256(text.encode()).hexdigest(),output)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);build(p.parse_args().output)
