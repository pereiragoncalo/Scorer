"""Rebuild offline palettes from the reviewed factual colour manifest (no network)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def build():
    proof=json.loads((ROOT/'docs/data/club_kits.provenance.json').read_text(encoding='utf-8'))
    pack_path=ROOT/'docs/data/name-packs/Scorer-World-Real-Names-0.9.10.json'
    pack=json.loads(pack_path.read_text(encoding='utf-8'))
    assignments=json.loads(pack_path.with_suffix('.provenance.json').read_text(encoding='utf-8'))['assignments']
    by_uid={row['uid']:row for row in assignments}
    for uid,name in pack['clubs'].items():
        row=proof['clubs'].get(uid)
        if not row or row['club']!=name or row['identity']!=by_uid[uid]['identity']:
            raise ValueError('Missing or mismatched home colours for '+name+' ('+uid+')')
    return {'version':1,'clubs':{uid:{'home':row['home']} for uid,row in proof['clubs'].items()}}

if __name__=='__main__':
    (ROOT/'assets/data/club_kits.json').write_text(json.dumps(build(),indent=2)+'\n',encoding='utf-8')
