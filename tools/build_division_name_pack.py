"""Build v1 editor aliases against reviewed season/division membership.
Offline inputs only. Never move career clubs, guess a city or repeat a real team.
"""
import argparse,collections,gzip,csv,hashlib,json,re,sys,tempfile,unicodedata,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.build_real_name_pack import COMPETITIONS,valid_name
LEGAL={'fc','cf','sc','cd','gd','ud','rc','afc','ac','as','us','ss','ca','ad','sv','tsv','vfl','vfb','ssc','fsv','sl','osc','losc'}
LEAGUES={'Portugal':['Primeira Liga','Liga Portugal 2','Liga 3','Campeonato de Portugal'],'England':['Premier League','EFL Championship','EFL League One','EFL League Two','National League'],'Spain':['La Liga','Segunda División','Primera Federación'],'Germany':['Bundesliga','2. Bundesliga','3. Liga'],'Italy':['Serie A','Serie B','Serie C'],'France':['Ligue 1','Ligue 2','Ligue 3'],'Brazil':['Série A','Série B','Série C','Série D'],'Argentina':['Primera División','Primera Nacional','Primera B Metropolitana','Primera C']}

def normalize(text):
    text=unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode().lower()
    return ''.join(w for w in re.findall('[a-z0-9]+',text) if w not in LEGAL)

def load_registry(path):
    data=json.loads(Path(path).read_text());registry={};lookups=collections.defaultdict(dict)
    for row in data['divisions']:
        key=(row['country'],row['tier']);assert key not in registry
        registry[key]=row
        for team in row['teams']:
            for alias in [team['name']]+team['aliases']:
                n=normalize(alias);old=lookups[row['country']].get(n)
                if old is not None and old['identity']!=team['identity']:raise ValueError('Ambiguous club alias: '+row['country']+' / '+alias)
                lookups[row['country']][n]=team
    return registry,lookups

def csv_rows(path):
    with gzip.open(path,'rt',encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def build(players_path,clubs_path,manifest_path,previous_path,layout="two-divisions"):
    registry,lookups=load_registry(manifest_path)
    clubs_by_team=collections.defaultdict(list)
    for c in csv_rows(clubs_path):
        for country,competition in COMPETITIONS.items():
            if c['domestic_competition_id']!=competition:continue
            team=lookups[country].get(normalize(c['name']))
            if team is not None:clubs_by_team[country,team['identity']].append(c)
    rosters=collections.defaultdict(list)
    for p in csv_rows(players_path):
        if int(p.get('last_season') or 0)>=2025 and p.get('position')!='Goalkeeper' and valid_name(p['name']):rosters[p['current_club_id']].append(p)
    references=json.loads((ROOT/'docs/data/world_club_provenance.json').read_text())['clubs']
    priorities={};slot_order={uid:index for index,uid in enumerate(references)}
    for old in references.values():
        country=old['country'];team=lookups[country].get(normalize(old.get('reference') or ''))
        if team is not None:priorities.setdefault((country,team['identity']),len(priorities))
    previous=json.loads(Path(previous_path).read_text());pack={'version':1,'leagues':{},'clubs':{},'players':{}};assignments=[];omitted=[];seen=set()
    from career import CareerMode
    from unittest.mock import patch
    access=type('WorldAccess',(),{'has_world_access':lambda _:True})()
    with tempfile.TemporaryDirectory() as folder,patch.dict(os.environ,STRIKER_SAVE_DIR=folder):
        career=CareerMode(access,autoload=False,save_slot='world')
        for (country,tier),division in registry.items():
            if layout=='two-divisions' and tier>3:continue
            league=career.leagues[f'{country}|{tier}']
            slots=career.reserve_clubs(country) if layout=='two-divisions' and tier==3 else league.clubs
            slots=sorted(slots,key=lambda club:slot_order[club.uid]);all_teams=division['teams']
            teams=sorted(all_teams,key=lambda t:priorities.get((country,t['identity']),100000))[:len(slots)]
            taken=set();chosen={}
            # Keep a reference on its UID only when it really belongs to this tier.
            for club in slots:
                old=references[club.uid].get('reference') or ''
                team=lookups[country].get(normalize(old))
                if team in teams and team['identity'] not in taken:chosen[club.uid]=team;taken.add(team['identity'])
            remaining=[t for t in teams if t['identity'] not in taken]
            for club in slots:
                if club.uid not in chosen:
                    if not remaining:raise ValueError(f'{country}/{tier}: insufficient real clubs; no fabricated filler permitted')
                    chosen[club.uid]=remaining.pop(0)
            omitted+= [dict(country=country,tier=tier,club=t['name'],wiki_path=t['wiki_path']) for t in all_teams if t not in teams]
            if layout!='two-divisions' or tier<=2:pack['leagues'][league.key]=LEAGUES[country][tier-1]
            for club in slots:
                team=chosen[club.uid];identity=(country,team['identity'])
                if identity in seen:raise ValueError('Repeated club identity: '+str(identity))
                seen.add(identity);pack['clubs'][club.uid]=team['name'];default_names=league.squad_names(club.name)
                candidates=clubs_by_team[identity];source=candidates[0] if len(candidates)==1 else None
                roster=rosters[source['club_id']] if source is not None else []
                roster=sorted(roster,key=lambda p:({'Attack':0,'Midfield':1,'Defender':2}.get(p['position'],3),-float(p.get('market_value_in_eur') or 0),int(p['player_id'])))
                selected=[]
                for p in roster:
                    if p['name'] not in selected:selected.append(p['name'])
                    if len(selected)==12:break
                for slot in range(12):
                    key=f'{club.uid}:{slot}'
                    if slot<len(selected):pack['players'][key]=selected[slot]
                    elif key in previous.get('players',{}):pack['players'][key]=default_names[slot]
                assignments.append(dict(uid=club.uid,country=country,tier=tier,club=team['name'],identity=team['identity'],source_team_url=team['wiki_path'],previous_reference=references[club.uid].get('reference'),player_source_club_id=source['club_id'] if source else None,real_player_names=selected,retained_fictional_slots=12-len(selected)))
        career.preview_names(pack)
    text=json.dumps(pack,ensure_ascii=False,indent=2)+'\n'
    if len(text.encode())>262144:raise ValueError('Formatted pack exceeds 256KiB')
    report=dict(layout=layout,selection='Within each verified division prefer real references already present anywhere in the country catalogue, then source table order. Keep correct UID references where possible. Never use another division to fill slots.',reference='Europe2026-27; Brazil/Argentina2026',club_entries=len(pack['clubs']),player_aliases=len(pack['players']),league_aliases=len(pack['leagues']),total_aliases=sum(len(pack[k]) for k in ('clubs','players','leagues')),real_player_names=sum(len(a['real_player_names']) for a in assignments),changed_club_aliases=sum(pack['clubs'].get(k)!=v for k,v in previous['clubs'].items()),assignments=assignments,not_represented_due_to_game_capacity=omitted,player_reference_date='2026-07-06; membership correction is not a November squad update',input_sha256={Path(p).name:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (players_path,clubs_path,manifest_path,previous_path)})
    return pack,report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--players',type=Path,required=True);p.add_argument('--clubs',type=Path,required=True);p.add_argument('--manifest',type=Path,default=ROOT/'docs/data/real_divisions_2026.json');p.add_argument('--previous',type=Path,default=ROOT/'docs/data/name-packs/Scorer-World-Real-Names-Europe-Brazil-Argentina-2026-07.json');p.add_argument('--layout',choices=('historical','two-divisions'),default='two-divisions');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    pack,report=build(a.players,a.clubs,a.manifest,a.previous,a.layout);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n');a.output.with_suffix('.provenance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(report['club_entries'],'clubs;',report['player_aliases'],'player aliases;',report['real_player_names'],'sourced players;',report['changed_club_aliases'],'changed club labels')
if __name__=='__main__':main()
