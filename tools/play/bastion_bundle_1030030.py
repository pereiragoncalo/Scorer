"""Download pinned1030030 and sign locally with the existing owner upload key."""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.request

BASE='https://github.com/pereiragoncalo/Scorer/releases/download/world-1.0-1030030/'
BUNDLE='Scorer-World-1.0-1030030-unsigned.aab'
BUNDLE_SHA='cc7f48ac2aacb1c1cb01ccf3fccc8816f0d0b50f8c89fb74ec61175364f5d072'
HELPER_SHA='5492d1fa8de0e3072960a0c34eaf05548cdaaa51c84f154d8ef579c885fa6761'
CERT='2259de229b49bb40e158d3c015fe1e0d2426becb4e1a4f110dbcd183b51e59a0'
OUTPUT=Path('/home/clemir/Scorer-World-1.0-1030030.aab')
KEY=Path('/root/scorer-signing/scorer-upload.p12')


def download(name,destination,expected):
    print('Downloading '+name,flush=True)
    digest=hashlib.sha256();total=0
    with urllib.request.urlopen(BASE+name,timeout=90) as response, destination.open('xb') as output:
        while True:
            chunk=response.read(1024*1024)
            if not chunk:break
            digest.update(chunk);output.write(chunk);total+=len(chunk)
            if total%(16*1024*1024)==0:print(str(total//(1024*1024))+' MiB',flush=True)
    if digest.hexdigest()!=expected:raise ValueError('Download checksum mismatch: '+name)
    print('SHA256 verified: '+name,flush=True)


def main():
    if OUTPUT.exists() or OUTPUT.is_symlink():raise ValueError('Output already exists; nothing overwritten: '+str(OUTPUT))
    if not KEY.is_file():raise ValueError('Existing upload key not found; do not create a replacement key')
    with tempfile.TemporaryDirectory(prefix='scorer-1030030-') as directory:
        directory=Path(directory);bundle=directory/BUNDLE;helper=directory/'sign_local_bundle.py'
        download(BUNDLE,bundle,BUNDLE_SHA);download('sign_local_bundle.py',helper,HELPER_SHA)
        subprocess.run([sys.executable,str(helper),'--input',str(bundle),'--output',str(OUTPUT),
                        '--keystore',str(KEY),'--input-sha256',BUNDLE_SHA,'--certificate-sha256',CERT],check=True)
    print('Ready for INTERNAL Play upload only: '+str(OUTPUT))
    print('Use a NEW release containing1030030; exclude superseded1030000/1030001/1030002/1030003/1030004. No upload performed.')

if __name__=='__main__':
    try:main()
    except (OSError,ValueError,subprocess.CalledProcessError) as error:
        print('Stopped: '+str(error),file=sys.stderr);sys.exit(1)
