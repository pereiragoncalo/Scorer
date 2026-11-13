"""Bundle the per-season global leaderboard backend with known source baselines."""
import argparse,base64,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT))

def build(output):
 from server.install_season_board import FILES
 files=FILES
 payload={name:{'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),'data':base64.b64encode((ROOT/name).read_bytes()).decode()} for name in files}
 baseline=json.loads((ROOT/'docs/data/season_board_baseline.json').read_text())
 packed=base64.b64encode(json.dumps(payload,separators=(',',':'),sort_keys=True).encode()).decode()
 text=(ROOT/'server/install_season_board.py').read_text().replace('PAYLOAD=None','PAYLOAD='+repr(packed)).replace('BASELINE=None','BASELINE='+repr(dict(sorted(baseline.items()))))
 Path(output).write_text(text)
 print(hashlib.sha256(text.encode()).hexdigest(),output)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);build(p.parse_args().output)
