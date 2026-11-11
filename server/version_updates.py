"""Local operator control of the public minimum version. No database or user data."""
import argparse,json,os,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from version_policy import validate,read,PACKAGE

def policy_path(public_config):return Path(public_config).parent/'version-policy.json'

def write(path,data):
    path=Path(path);data=validate(data)
    if path.is_symlink():raise ValueError('Refusing policy symlink')
    path.parent.mkdir(parents=True,exist_ok=True)
    previous=path.stat() if path.exists() else None
    fd,name=tempfile.mkstemp(prefix='.version-policy-',dir=path.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf8') as f:json.dump(data,f,separators=(',',':'));f.flush();os.fsync(f.fileno())
        os.chmod(name,0o644)
        if previous and os.geteuid()==0:os.chown(name,previous.st_uid,previous.st_gid)
        os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--path',type=Path,default=Path('/opt/scorer/version-policy.json'))
    parser.add_argument('--minimum',type=int);parser.add_argument('--latest',type=int);parser.add_argument('--name')
    args=parser.parse_args()
    if args.minimum is None:print(json.dumps(read(args.path),indent=2));return
    if args.latest is None or not args.name:parser.error('--minimum requires --latest and --name')
    write(args.path,dict(schema=1,package=PACKAGE,minimum_version_code=args.minimum,latest_version_code=args.latest,latest_version_name=args.name))
    print('Public version policy updated atomically. Activate a higher minimum only after Play makes that version available to every intended player.')
if __name__=='__main__':main()
