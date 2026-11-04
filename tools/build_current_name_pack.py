"""Extend the reviewed eight-country names pack to current initial UID capacities.

Offline inputs only. Preserve existing assignments; never borrow from another
real division, move clubs, guess rosters or rename any career's canonical IDs.
"""
import argparse
import copy
import hashlib
import json
import os
import tempfile
from collections import defaultdict
from pathlib import Path
from unittest.mock import patch

from tools.build_division_name_pack import load_registry,normalize,csv_rows
from tools.build_real_name_pack import COMPETITIONS,valid_name

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/data/name-packs/Scorer-World-Real-Names-Two-Divisions-2026.json'
MANIFEST=ROOT/'docs/data/real_divisions_2026.json'


def build(players_path,clubs_path,baseline=BASE,manifest=MANIFEST):
    from career import CareerMode
    source=json.loads(Path(baseline).read_text())
    previous=json.loads(Path(baseline).with_suffix('.provenance.json').read_text())
    registry,lookups=load_registry(manifest)
    pack=copy.deepcopy(source)
    references={row['uid']:row for row in previous['assignments']}
    sources=defaultdict(list)
    for club in csv_rows(clubs_path):
        for country,competition in COMPETITIONS.items():
            if club['domestic_competition_id']!=competition:continue
            team=lookups[country].get(normalize(club['name']))
            if team:sources[country,team['identity']].append(club)
    players=defaultdict(list)
    for row in csv_rows(players_path):
        if int(row.get('last_season') or 0)>=2025 and row.get('position')!='Goalkeeper' and valid_name(row['name']):
            players[row['current_club_id']].append(row)
    access=type('WorldAccess',(),{'has_world_access':lambda _:True})()
    assignments=[];omitted=[];seen=set();countries=tuple(k.split('|')[0] for k in source['leagues'] if k.endswith('|1'))
    with tempfile.TemporaryDirectory() as temp,patch.dict(os.environ,STRIKER_SAVE_DIR=temp):
        career=CareerMode(access,autoload=False,save_slot='world')
        for country in countries:
            for tier in (1,2,3):
                slots=career.reserve_clubs(country) if tier==3 else career.leagues[f'{country}|{tier}'].clubs
                slots=sorted(slots,key=lambda club:club.uid)
                teams=registry[country,tier]['teams'];chosen={};taken=set()
                for club in slots:
                    if club.uid not in source['clubs']:continue
                    team=lookups[country].get(normalize(source['clubs'][club.uid]))
                    if team not in teams:raise ValueError('Existing alias is outside its initial real division: '+club.uid)
                    if team['identity'] in taken:raise ValueError('Repeated existing real identity')
                    chosen[club.uid]=team;taken.add(team['identity'])
                remaining=[t for t in teams if t['identity'] not in taken]
                for club in slots:
                    if club.uid in chosen:continue
                    if not remaining:raise ValueError(f'{country}/{tier}: not enough verified real clubs')
                    team=remaining.pop(0);chosen[club.uid]=team;taken.add(team['identity'])
                    pack['clubs'][club.uid]=team['name']
                    matches=sources[country,team['identity']]
                    club_source=matches[0] if len(matches)==1 else None
                    roster=players[club_source['club_id']] if club_source else []
                    roster=sorted(roster,key=lambda p:({'Attack':0,'Midfield':1,'Defender':2}.get(p['position'],3),-float(p.get('market_value_in_eur') or 0),int(p['player_id'])))
                    selected=[]
                    for row in roster:
                        if row['name'] not in selected:selected.append(row['name'])
                        if len(selected)==12:break
                    for i,name in enumerate(selected):pack['players'][f'{club.uid}:{i}']=name
                    references[club.uid]=dict(uid=club.uid,country=country,tier=tier,club=team['name'],identity=team['identity'],source_team_url=team['wiki_path'],previous_reference=None,player_source_club_id=club_source['club_id'] if club_source else None,real_player_names=selected,retained_fictional_slots=12-len(selected))
                for club in slots:
                    team=chosen[club.uid]
                    identity=(country,team['identity'])
                    if identity in seen:raise ValueError('Real club assigned twice: '+str(identity))
                    seen.add(identity);assignments.append(references[club.uid])
                omitted.extend(dict(country=country,tier=tier,club=t['name'],wiki_path=t['wiki_path']) for t in teams if t['identity'] not in taken)
        career.preview_names(json.dumps(pack,ensure_ascii=False))
        # The smaller compatible file must import in both current and old saves.
        career.preview_names(json.dumps(source,ensure_ascii=False))
        legacy=CareerMode(access,autoload=False,save_slot='world',domestic_formats=False)
        legacy.preview_names(json.dumps(source,ensure_ascii=False))
    text=json.dumps(pack,ensure_ascii=False,indent=2)+'\n'
    if len(text.encode())>262144:raise ValueError('Formatted pack exceeds 256KiB')
    report=dict(layout='current-two-divisions',target='World0.9.7+ new-career capacities, verified against0.9.10',countries=list(countries),selection='Keep every previously reviewed UID assignment. Fill only additional slots from unused clubs in the same verified real division, in source order; sort extra slots by stable UID.',club_entries=len(pack['clubs']),active_club_entries=sum(a['tier']<=2 for a in assignments),reserve_club_entries=sum(a['tier']==3 for a in assignments),league_aliases=len(pack['leagues']),player_aliases=len(pack['players']),real_player_names=sum(len(a['real_player_names']) for a in assignments),total_aliases=sum(len(pack[k]) for k in ('clubs','players','leagues')),added_club_entries=len(pack['clubs'])-len(source['clubs']),preserved_existing_club_aliases=all(pack['clubs'][k]==v for k,v in source['clubs'].items()),preserved_existing_player_aliases=all(pack['players'][k]==v for k,v in source['players'].items()),player_reference_date=previous['player_reference_date'],membership_reference=previous['reference'],assignments=assignments,not_represented_due_to_game_capacity=omitted,input_sha256={Path(p).name:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (players_path,clubs_path,baseline,manifest)})
    return pack,source,report


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--players',type=Path,required=True);p.add_argument('--clubs',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--compatible-output',type=Path,required=True);a=p.parse_args()
    pack,compatible,report=build(a.players,a.clubs)
    for path,data in ((a.output,pack),(a.compatible_output,compatible)):
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    a.output.with_suffix('.provenance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(report['club_entries'],'clubs;',report['added_club_entries'],'new slots;',report['player_aliases'],'player aliases;',report['real_player_names'],'sourced player names')

if __name__=='__main__':main()
