import sys,json,gzip,base64,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from server.install_play_candidate import FILES
payload={name:dict(data=base64.b64encode((ROOT/('server/public.world.policy.json' if name=='public.json' else name)).read_bytes()).decode(),sha256=hashlib.sha256((ROOT/('server/public.world.policy.json' if name=='public.json' else name)).read_bytes()).hexdigest()) for name in FILES}
encoded=base64.b64encode(gzip.compress(json.dumps(payload).encode(),mtime=0)).decode()
source=(ROOT/'server/install_play_candidate.py').read_text().replace('PAYLOAD=None','PAYLOAD='+repr(encoded))
out=ROOT/'docs/data/server/Scorer-Play-Policy-0.9.40.py';out.write_text(source);print(out.name,hashlib.sha256(out.read_bytes()).hexdigest())
