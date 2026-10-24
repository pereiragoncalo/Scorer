"""One-installation owner QA: Free and World slots, test entitlement, NO payments.

This is not a store or ownership-verified build. It replaces the previous beta
using the SAME package/certificate; it is not a second paid application.
"""
import argparse
import configparser
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.play.prepare import ROOT, prepare


def prepare_qa(target):
    config=json.loads((ROOT/'release/play.example.json').read_text())
    target=prepare(config,Path(target),'rehearsal')
    edition=target/'edition.py'
    edition.write_text(edition.read_text().replace('WORLD_PREVIEW = False','WORLD_PREVIEW = True',1))
    settings=target/'release_settings.py'
    settings.write_text(settings.read_text().replace("CHANNEL = 'rehearsal'","CHANNEL = 'qa-world'",1))
    spec=configparser.ConfigParser(interpolation=None);spec.read(target/'buildozer.spec')
    spec['app']['title']='SCORER QA — Free + World'
    with (target/'buildozer.spec').open('w') as out:spec.write(out)
    (target/'.scorer-world-qa').write_text('SAME-APP QA TEST ENTITLEMENT. Not paid ownership. Billing disabled.\n')
    return target


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    print(prepare_qa(parser.parse_args().output))
