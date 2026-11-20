"""Sign a verified unsigned AAB on the owner's machine. Password stays local."""
import argparse,getpass,hashlib,os,re,shutil,ssl,subprocess,tempfile,zipfile
from pathlib import Path

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def fingerprint(pem):
    match=re.search(r'-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----',pem,re.S)
    if not match:raise ValueError('Public certificate not found')
    return hashlib.sha256(ssl.PEM_cert_to_DER_cert(match.group())).hexdigest()

def sign_bundle(source,output,keystore,password,expected_input,expected_certificate,alias='scorer-upload'):
    source=Path(source).resolve();output=Path(output).absolute();keystore=Path(keystore).resolve()
    if os.path.lexists(output):raise FileExistsError('Refusing existing output: '+str(output))
    if not source.is_file() or not keystore.is_file():raise ValueError('Bundle and local upload keystore must exist')
    if not re.fullmatch('[0-9a-fA-F]{64}',expected_input) or not re.fullmatch('[0-9a-fA-F]{64}',expected_certificate):raise ValueError('Expected SHA256 fingerprints must have64hex characters')
    if digest(source)!=expected_input.lower():raise ValueError('Unsigned bundle SHA256 does not match the verified build')
    for tool in ('keytool','jarsigner'):
        if not shutil.which(tool):raise RuntimeError('A full JDK is required: missing '+tool)
    with zipfile.ZipFile(source) as archive:
        names=archive.namelist()
        if not {'BundleConfig.pb','base/manifest/AndroidManifest.xml'}<=set(names):raise ValueError('Not an Android App Bundle')
        if any(n.upper().startswith('META-INF/') and n.upper().endswith(('.RSA','.DSA','.EC','.SF')) for n in names):raise ValueError('Input is already signed; use the verified unsigned AAB')
    env=dict(os.environ,SCORER_LOCAL_UPLOAD_PASSWORD=password)
    def run(command):
        result=subprocess.run(command,env=env,capture_output=True,text=True)
        if result.returncode:raise RuntimeError('Local JDK operation failed: '+(result.stderr or result.stdout).strip())
        return result.stdout
    public=run(['keytool','-exportcert','-rfc','-keystore',str(keystore),'-alias',alias,'-storepass:env','SCORER_LOCAL_UPLOAD_PASSWORD'])
    if fingerprint(public)!=expected_certificate.lower():raise ValueError('Upload key certificate does not match the expected owner fingerprint')
    output.parent.mkdir(parents=True,exist_ok=True)
    old_mask=os.umask(0o077)
    try:
        with tempfile.TemporaryDirectory(prefix='.scorer-sign-',dir=output.parent) as directory:
            temporary=Path(directory)/'signed.aab'
            run(['jarsigner','-keystore',str(keystore),'-storepass:env','SCORER_LOCAL_UPLOAD_PASSWORD','-keypass:env','SCORER_LOCAL_UPLOAD_PASSWORD','-sigalg','SHA256withRSA','-digestalg','SHA-256','-signedjar',str(temporary),str(source),alias])
            run(['jarsigner','-verify',str(temporary)])
            actual=run(['keytool','-printcert','-rfc','-jarfile',str(temporary)])
            if fingerprint(actual)!=expected_certificate.lower():raise ValueError('Signed AAB certificate mismatch')
            with zipfile.ZipFile(temporary) as archive:
                if not any(n.upper().startswith('META-INF/') and n.upper().endswith('.SF') for n in archive.namelist()):raise ValueError('AAB signature missing')
            temporary.chmod(0o644);os.link(temporary,output)
    finally:env.pop('SCORER_LOCAL_UPLOAD_PASSWORD',None);os.umask(old_mask)
    return digest(output)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--keystore',type=Path,required=True)
    p.add_argument('--input-sha256',required=True);p.add_argument('--certificate-sha256',required=True);p.add_argument('--alias',default='scorer-upload');a=p.parse_args()
    if os.path.lexists(a.output):raise SystemExit('Refusing existing output. Preserve the existing signed bundle.')
    password=getpass.getpass('Existing upload-key password (hidden): ')
    try:sha=sign_bundle(a.input,a.output,a.keystore,password,a.input_sha256,a.certificate_sha256,a.alias)
    except (ValueError,FileExistsError,RuntimeError) as error:raise SystemExit(str(error))
    print('Signed AAB:',a.output)
    print('Signed AAB SHA256:',sha)
    print('Upload certificate SHA256:',a.certificate_sha256.lower())
    print('Signature verified locally. Private key/password stayed on this machine. No upload performed.')
if __name__=='__main__':main()
