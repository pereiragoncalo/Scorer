"""Generate a protected LOCAL upload key only for new Play app enrollment.
Never run over an existing key. Confirm existing Play signing requirements first.
"""
import argparse,getpass,os,subprocess
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--keystore',type=Path,required=True);p.add_argument('--alias',default='scorer-upload');p.add_argument('--owner',default='Gonçalo Pereira');a=p.parse_args()
    path=a.keystore.expanduser().resolve()
    if path.exists():raise SystemExit('Refusing to overwrite a keystore')
    password=getpass.getpass('New keystore password (at least12characters): ')
    if len(password)<12 or password!=getpass.getpass('Repeat password: '):raise SystemExit('Password mismatch or too short')
    path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    env=dict(os.environ,SCORER_NEW_KEY_PASSWORD=password)
    old_mask=os.umask(0o077)
    try:
        subprocess.run(['keytool','-genkeypair','-storetype','PKCS12','-keystore',str(path),'-alias',a.alias,'-keyalg','RSA','-keysize','4096','-validity','10000','-dname','CN='+a.owner+', O=clemir','-storepass:env','SCORER_NEW_KEY_PASSWORD','-keypass:env','SCORER_NEW_KEY_PASSWORD'],env=env,check=True)
        path.chmod(0o600)
    finally:os.umask(old_mask)
    print('Local upload key created. Back it up securely offline before enrolling in Play. No upload performed.')
if __name__=='__main__':main()
