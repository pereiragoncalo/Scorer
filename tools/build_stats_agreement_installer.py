"""Bundle complete reviewed version-gate server closure; never include credentials."""
import base64,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from server.install_stats_agreement import sources,preflight
payload=sources();preflight(payload)
data={name:dict(data=base64.b64encode(raw).decode(),sha256=hashlib.sha256(raw).hexdigest()) for name,raw in payload.items()}
encoded=base64.b64encode(gzip.compress(json.dumps(data).encode(),mtime=0)).decode()
source=(ROOT/'server/install_stats_agreement.py').read_text().replace('PAYLOAD=None','PAYLOAD='+repr(encoded))
p=ROOT/'docs/data/server/Scorer-Statistics-Agreement-Backend.py';p.write_text(source);print(p.name,hashlib.sha256(p.read_bytes()).hexdigest())
