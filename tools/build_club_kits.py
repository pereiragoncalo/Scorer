"""Rebuild offline palettes from the reviewed factual colour manifest (no network)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def build():
    proof=json.loads((ROOT/'docs/data/club_kits.provenance.json').read_text(encoding='utf-8'))
    return {'version':1,'clubs':{uid:{'home':row['home']} for uid,row in proof['clubs'].items()}}

if __name__=='__main__':
    (ROOT/'assets/data/club_kits.json').write_text(json.dumps(build(),indent=2)+'\n',encoding='utf-8')
