"""Install only public policy configuration; does not touch tunnel/admin secrets."""
import argparse,json,os
from pathlib import Path
from server.public_pages import page,load_config
from online_safety import atomic_json
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('config',type=Path);p.add_argument('--output',type=Path,default=Path('/opt/scorer/public.json'));args=p.parse_args()
    status,_=page('/privacy',args.config)
    if status!=200:raise SystemExit('Complete all public policy fields first; legal/provider/children review must reflect actual deployment.')
    if args.output==Path('/opt/scorer/public.json') and os.geteuid()!=0:raise SystemExit('Run as root to install /opt/scorer/public.json')
    data=json.loads(args.config.read_text());atomic_json(args.output,data);args.output.chmod(0o644)
    status=load_config(args.config)['publication_status']
    print('Public documents installed ('+status+'). Verify /privacy, /terms and /delete; no credentials changed.')
    if status=='draft':print('Draft policy remains under review; this does not enable production publication.')
