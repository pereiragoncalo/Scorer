"""Stage/build the original Kivy Free game for Windows; no cross-compilation."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tools.prepare_editions import prepare_edition


def stage_windows(target,source=ROOT):
    target=prepare_edition('free',target,source=source)
    for name in ('android','tools'):
        shutil.rmtree(target/name,ignore_errors=True)
    (target/'buildozer.spec').unlink(missing_ok=True)
    (target/'release_settings.py').write_text((target/'release_settings.py').read_text()+"\nDESKTOP_WINDOWS = True\n",encoding='utf8')
    return target


def build(output):
    if sys.platform != 'win32':
        raise RuntimeError('Build Scorer-Free.exe on Windows with Python 3.12 x64; Linux cannot generate this executable')
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='scorer-windows-') as temporary:
        folder=Path(temporary);stage=stage_windows(folder/'source')
        env=dict(os.environ,SCORER_WINDOWS_STAGE=str(stage))
        subprocess.run([sys.executable,'-m','PyInstaller','--noconfirm','--clean',
                        '--distpath',str(output),'--workpath',str(folder/'work'),
                        str(ROOT/'tools/windows/ScorerFree.spec')],env=env,check=True)
    exe=output/'Scorer-Free.exe'
    if not exe.is_file():raise RuntimeError('PyInstaller did not produce Scorer-Free.exe')
    return exe


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--stage-only',type=Path)
    group.add_argument('--output',type=Path)
    args=parser.parse_args()
    print(stage_windows(args.stage_only) if args.stage_only else build(args.output))
