"""Build passive editor aliases from the game's club references and public CSV data.
No downloads, executable pack content, career writes or fuzzy club assignment.
"""
import argparse,csv,gzip,hashlib,json,re,unicodedata
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COMPETITIONS={'Portugal':'PO1','England':'GB1','Spain':'ES1','Germany':'L1','Italy':'IT1','France':'FR1'}
ALIASES={
 'Portugal':{'Vitória de Guimarães':'Vitória Guimarães SC','Os Belenenses':'CF Os Belenenses','Casa Pia':'Casa Pia AC','Estoril Praia':'GD Estoril Praia','Vitória de Setúbal':'Vitória Setúbal FC','CD Nacional Madeira':'CD Nacional','Académica de Coimbra':'Académica Coimbra','Desportivo de Chaves':'GD Chaves','CF Estrela da Amadora':'CF Estrela Amadora'},
 'Spain':{'Atlético Madrid':'Atlético de Madrid','Athletic Club Bilbao':'Athletic Bilbao','Real Betis':'Real Betis Balompié','RCD Espanyol':'RCD Espanyol Barcelona','RCD La Coruña':'Deportivo de La Coruña','RC Celta Vigo':'Celta de Vigo'},
 'Germany':{'Bayern München':'Bayern Munich','1. FC Nürnberg':'1.FC Nuremberg','Bor. Mönchengladbach':'Borussia Mönchengladbach'},
 'Italy':{'FC Internazionale Milano':'Inter Milan','AS Roma':'Associazione Sportiva Roma','Atalanta Bergamo':'Atalanta BC','SS Lazio':'Società Sportiva Lazio S.p.A.','Bologna FC':'Bologna Football Club 1909','US Sassuolo Calcio':'US Sassuolo','SPAL Ferrara':'SPAL','AC Pisa':'Pisa Sporting Club','Parma Calcio':'Parma Calcio 1913','Pescara':'Delfino Pescara 1936','Salernitana':'US Salernitana 1919','AC Chievo Verona':'Chievo Verona'},
 'France':{'Olympique de Marseille':'Olympique Marseille','Olympique Lyonnais':'Olympique Lyon','Lille OSC':'LOSC Lille','Girondins de Bordeaux':'FC Girondins Bordeaux','Stade Malherbe Caen':'SM Caen','RC Strasbourg':'RC Strasbourg Alsace','Toulouse FC':'FC Toulouse','ES Troyes AC':'ESTAC Troyes','Stade de Reims':'Stade Reims'},
}
def normalize(text):
    text=unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode().lower()
    words=re.findall(r'[a-z0-9]+',text)
    # Ignore only common legal football suffixes/prefixes. Never guess a city/team.
    return ''.join(w for w in words if w not in ('fc','afc'))
def rows(path):
    with gzip.open(path,'rt',encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def valid_name(value):
    value=unicodedata.normalize('NFC',value.strip())
    return 2<=len(value)<=56 and '://' not in value and not any(unicodedata.category(c).startswith('C') or c in '<>[]' for c in value)
def build(players_path,clubs_path,countries):
    club_rows=rows(clubs_path);players=defaultdict(list)
    for p in rows(players_path):
        if int(p.get('last_season') or 0)>=2025 and valid_name(p['name']) and p.get('position')!='Goalkeeper':players[p['current_club_id']].append(p)
    provenance=json.loads((ROOT/'docs/data/world_club_provenance.json').read_text())['clubs']
    pack={'version':1,'leagues':{},'clubs':{},'players':{}};matches=[];without=[]
    for country in countries:
        lookup=defaultdict(list)
        for c in club_rows:
            if c['domestic_competition_id']==COMPETITIONS[country]:lookup[normalize(c['name'])].append(c)
        for uid,c in provenance.items():
            if c['country']!=country or not c.get('reference'):continue
            real=c['reference'];pack['clubs'][uid]=real
            query=ALIASES.get(country,{}).get(real,real);candidates=lookup.get(normalize(query),[])
            # Ambiguous/unmatched clubs stay without a made-up real squad.
            if len(candidates)!=1:without.append(dict(uid=uid,country=country,club=real,reason='no unique club match'));continue
            club=candidates[0];roster=players.get(club['club_id'],[])
            # This striker game has 12 display slots, not a full real team formation.
            roster=sorted(roster,key=lambda p:({'Attack':0,'Midfield':1,'Defender':2}.get(p['position'],3),-float(p.get('market_value_in_eur') or 0),int(p['player_id'])))
            seen=set();selected=[]
            for p in roster:
                if p['name'] in seen:continue
                seen.add(p['name']);selected.append(p)
                if len(selected)==12:break
            for slot,p in enumerate(selected):pack['players'][f'{uid}:{slot}']=p['name']
            matches.append(dict(uid=uid,country=country,game_club_reference=real,source_club_name=club['name'],source_club_id=club['club_id'],player_names=[p['name'] for p in selected]))
            if len(selected)<12:without.append(dict(uid=uid,country=country,club=real,reason=f'only {len(selected)} eligible names'))
    if len(json.dumps(pack,ensure_ascii=False).encode())>262144 or sum(len(pack[k]) for k in ('leagues','clubs','players'))>4096:raise ValueError('Split this pack: editor limits exceeded')
    return pack,dict(countries=countries,club_entries=len(pack['clubs']),player_aliases=len(pack['players']),clubs_with_player_names=sum(bool(m['player_names']) for m in matches),matched_clubs=matches,clubs_with_missing_or_partial_player_data=without,input_sha256={Path(p).name:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (players_path,clubs_path)})
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--players',type=Path,required=True);p.add_argument('--clubs',type=Path,required=True);p.add_argument('--countries',nargs='+',choices=COMPETITIONS,default=list(COMPETITIONS));p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    pack,report=build(a.players,a.clubs,a.countries);text=json.dumps(pack,ensure_ascii=False,indent=2)+'\n'
    if len(text.encode())>262144:raise ValueError('Formatted pack exceeds editor limit')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text,encoding='utf-8');a.output.with_suffix('.provenance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(a.output,report['club_entries'],'club entries,',report['player_aliases'],'player names,',len(text.encode()),'bytes')
if __name__=='__main__':main()
