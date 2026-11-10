"""Create a new LOCAL Play upload identity; refuse existing keys/certificates.
Run on the owner's bastion/laptop. Never send the private key or password in chat.
"""
import argparse,getpass,hashlib,os,shutil,ssl,stat,subprocess,tempfile
from pathlib import Path

def create_key(keystore,password,alias='scorer-upload',owner='Gonçalo Pereira'):
    requested=Path(keystore).expanduser().absolute()
    path=requested.parent.resolve()/requested.name
    certificate=path.with_suffix('.certificate.pem')
    for output in (path,certificate):
        if os.path.lexists(output):raise FileExistsError('Refusing existing output: '+str(output))
    if len(password)<12 or not password.isascii():raise ValueError('Use at least 12 characters without accents (letters, numbers, symbols or spaces).')
    if not shutil.which('keytool'):raise RuntimeError('keytool missing. Install a full JDK (default-jdk-headless on Debian).')
    path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    if stat.S_IMODE(path.parent.stat().st_mode)&0o077:
        raise ValueError('Use a private signing directory (permissions 700): '+str(path.parent))
    env=dict(os.environ,SCORER_NEW_KEY_PASSWORD=password)
    previous_mask=os.umask(0o077)
    try:
        with tempfile.TemporaryDirectory(prefix='.scorer-key-',dir=path.parent) as directory:
            temporary=Path(directory)/'upload.p12';public=Path(directory)/'certificate.pem'
            subprocess.run(['keytool','-genkeypair','-storetype','PKCS12','-keystore',str(temporary),'-alias',alias,'-keyalg','RSA','-keysize','4096','-sigalg','SHA256withRSA','-validity','10000','-dname','CN='+owner+', O=clemir','-storepass:env','SCORER_NEW_KEY_PASSWORD','-keypass:env','SCORER_NEW_KEY_PASSWORD'],env=env,check=True)
            subprocess.run(['keytool','-exportcert','-rfc','-keystore',str(temporary),'-alias',alias,'-file',str(public),'-storepass:env','SCORER_NEW_KEY_PASSWORD'],env=env,check=True)
            fingerprint=hashlib.sha256(ssl.PEM_cert_to_DER_cert(public.read_text())).hexdigest()
            temporary.chmod(0o600);public.chmod(0o644)
            # Same-filesystem exclusive links cannot overwrite an existing key,
            # even if another process creates the destination after preflight.
            os.link(temporary,path)
            try:os.link(public,certificate)
            except OSError as error:
                raise RuntimeError('Private key was created at '+str(path)+'; public certificate export could not be committed. Preserve the key; do not regenerate it.') from error
    finally:
        env.pop('SCORER_NEW_KEY_PASSWORD',None);os.umask(previous_mask)
    return path,certificate,fingerprint

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--keystore',type=Path,required=True);parser.add_argument('--alias',default='scorer-upload');parser.add_argument('--owner',default='Gonçalo Pereira');args=parser.parse_args()
    # Check outputs before asking for any password.
    for output in (args.keystore.expanduser(),args.keystore.expanduser().with_suffix('.certificate.pem')):
        if os.path.lexists(output):raise SystemExit('Refusing existing output: '+str(output))
    if not shutil.which('keytool'):raise SystemExit('Install default-jdk-headless first: keytool is missing.')
    password=getpass.getpass('New upload-key password (12+ characters, no accents): ')
    if password!=getpass.getpass('Repeat password: '):raise SystemExit('Passwords do not match. No key created.')
    try:path,certificate,fingerprint=create_key(args.keystore,password,args.alias,args.owner)
    except (ValueError,FileExistsError,RuntimeError) as error:raise SystemExit(str(error))
    print('Upload key created locally:',path)
    print('Public certificate:',certificate)
    print('Upload certificate SHA256:',fingerprint)
    print('Back up the private .p12 and its password securely in separate locations before Play enrollment.')
    print('Only the SHA256 fingerprint/public certificate may be shared. No upload or Play enrollment performed.')
if __name__=='__main__':main()
