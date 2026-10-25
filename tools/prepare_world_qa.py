"""Compatibility entry point: World QA is now a separate application."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.prepare_editions import prepare_edition


def prepare_qa(target):
    return prepare_edition('world',target)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    print(prepare_qa(p.parse_args().output))
