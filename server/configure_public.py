"""Install only public policy configuration; does not touch tunnel/admin secrets."""
import argparse,json,os
from pathlib import Path
from server.public_pages import page
from online_safety import atomic_json
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('config',type=Path);p.add_argument('--output',type=Path,default=Path('/etc/scorer/public.json'));args=p.parse_args()
    status,_=page('/privacy',args.config)
    if status!=200:raise SystemExit('Complete all public policy fields first; legal/provider/children review must reflect actual deployment.')
    if args.output==Path('/etc/scorer/public.json') and os.geteuid()!=0:raise SystemExit('Run as root to install /etc/scorer/public.json')
    data=json.loads(args.config.read_text());atomic_json(args.output,data);args.output.chmod(0o644)
    print('Public policy configuration installed. Verify /privacy, /terms and /delete; no credentials changed.')
