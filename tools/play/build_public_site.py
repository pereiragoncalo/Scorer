"""Build only reviewed public legal HTML for GitHub Pages; no app data or JS."""
import argparse
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from server.public_pages import load_config,page
BASE='/Scorer'

def build(target,config=ROOT/'server/public.world.policy.json'):
 target=Path(target)
 if load_config(config)['publication_status']!='published':raise ValueError('Do not deploy a draft policy')
 target.mkdir(parents=True,exist_ok=True)
 for name in ('privacy','terms','delete'):
  status,raw=page('/'+name,config)
  if status!=200:raise ValueError('Public page failed: '+name)
  text=raw.decode('utf8')
  for route in ('privacy','terms','delete'):
   text=text.replace('href="/'+route+'"','href="'+BASE+'/'+route+'/"')
  if 'DRAFT UNDER REVIEW' in text or '<script' in text.lower():raise ValueError('Unpublishable public page')
  path=target/name/'index.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf8')
 (target/'.nojekyll').write_text('')
 (target/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Scorer World</title><body><h1>Scorer World</h1><p>Gonçalo Pereira · goncalo@clemir.com</p><ul><li><a href="'+BASE+'/privacy/">Privacy Policy</a></li><li><a href="'+BASE+'/terms/">Community Rules</a></li><li><a href="'+BASE+'/delete/">Data and Record Removal</a></li></ul></body></html>',encoding='utf8')
 return target
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(build(a.output))
