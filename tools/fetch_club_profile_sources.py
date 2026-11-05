"""Fetch the exact public source revisions cited by an existing club-fact snapshot.

Python standard library only; network is build-time, never an app dependency.
Stops on rate limits/errors. Does not publish or modify the reviewed fact snapshot.
"""
import argparse,json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlencode,urlparse
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[1]

def fetch(manifest,output):
    groups=defaultdict(list)
    for uid,row in json.loads(manifest.read_text(encoding='utf8'))['clubs'].items():
        host=urlparse(row['source']).hostname
        if host not in ('en.wikipedia.org','es.wikipedia.org'):raise ValueError('Unreviewed primary source host')
        groups[host].append((uid,row))
    result={}
    for host,items in groups.items():
        for offset in range(0,len(items),20):
            chunk=items[offset:offset+20];by_revision=defaultdict(list)
            for uid,row in chunk:by_revision[row['revision']].append((uid,row))
            url='https://'+host+'/w/api.php?'+urlencode(dict(action='query',prop='revisions',revids='|'.join(map(str,by_revision)),rvprop='ids|content',rvslots='main',format='json',formatversion=2))
            request=Request(url,headers={'User-Agent':'ScorerClubFacts/1.0 (https://github.com/pereiragoncalo/Scorer)'})
            with urlopen(request,timeout=60) as response:data=json.load(response)
            for page in data['query']['pages']:
                for revision in page.get('revisions',[]):
                    for uid,row in by_revision.get(revision['revid'],[]):
                        result[uid]=dict(club=row['club'],country=row['country'],source=row['source'],title=page['title'],revision=revision['revid'],text=revision['slots']['main']['content'])
            output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,ensure_ascii=False),encoding='utf8')
            print('Fetched',len(result),'source records',flush=True)
    expected=sum(len(rows) for rows in groups.values())
    if len(result)!=expected:raise ValueError('Source revision coverage is incomplete')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--manifest',type=Path,default=ROOT/'assets/data/club_profiles.json');parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();fetch(args.manifest,args.output)
