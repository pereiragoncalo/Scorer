"""Reproducible sourced prestige; missing histories are explicit, never invented."""
import json,urllib.request,csv,io,concurrent.futures,unicodedata,re,hashlib,os,tempfile,threading
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];CACHE=Path(os.environ.get('SCORER_REPUTATION_CACHE',Path(tempfile.gettempdir())/'scorer-reputation-cache'));CACHE.mkdir(parents=True,exist_ok=True);OUT=ROOT/'docs/data/reputation'
def norm(s):
 s=re.sub(r'\b(?:FC|AFC|CF|SC|SK|BK|BSC|AC|CD|FK|IK|IF|IFK|FF|SS|AS)\b','',s,flags=re.I)
 return ''.join(c for c in unicodedata.normalize('NFKD',s).lower() if c.isalnum() and not unicodedata.combining(c))
fifa=json.loads((OUT/'fifa-ranking-2026-07-20.json').read_text())['Results'];uefa=json.loads((OUT/'uefa-associations-2026.json').read_text())['data']['members']
locks=defaultdict(threading.Lock)
# Public source snapshots are compact factual rows, with source URLs and hashes.
countries={}
alias={'Korea Republic':'South Korea','IR Iran':'Iran','USA':'United States','Türkiye':'Turkey','Congo DR':'DR Congo','China PR':'China','Brunei Darussalam':'Brunei','Cabo Verde':'Cape Verde','Curaçao':'Curacao','The Gambia':'Gambia','Hong Kong, China':'Hong Kong','Kyrgyz Republic':'Kyrgyzstan','DPR Korea':'North Korea','St Kitts and Nevis':'Saint Kitts and Nevis','St Lucia':'Saint Lucia','St Vincent and the Grenadines':'Saint Vincent and the Grenadines','São Tomé and Príncipe':'Sao Tome and Principe','Côte d\'Ivoire':'Ivory Coast'}
for r in fifa:
 name=r['TeamName'][0]['Description'];name=alias.get(name,name)
 countries[name]=dict(fifa_rank=r['Rank'],fifa_points=r['DecimalTotalPoints'],fifa_date=r['PubDate'][:10],status=round(25+60*max(0,1-(r['Rank']-1)/210)**.7),method='FIFA national-team proxy: game adaptation')
# UEFA fields are inspected and passed below; European club coefficients supersede national-team proxy.
for r in uefa:
 member=r['member'];name=member.get('name') or member.get('associationName') or member.get('countryName')
 rank=r['overallRanking']['position']
 if name and rank:
  countries.setdefault(name,{}) .update(uefa_rank=int(rank),uefa_coefficient=r['overallRanking']['totalPoints'],uefa_period=[r['overallRanking']['baseSeasonYear'],r['overallRanking']['targetSeasonYear']],status=round(45+55*(1-(int(rank)-1)/55)**2),method='UEFA five-season association coefficient: game scaling')
import sys
sys.path.insert(0,str(ROOT))
from career import WORLD_COUNTRIES
countries={country:countries.get(country,dict(status=25,method='Unranked association: explicit game fallback, not an official league rank')) for country in WORLD_COUNTRIES}
provenance=json.loads((ROOT/'docs/data/world_club_provenance.json').read_text())['clubs']
profiles={uid:dict(club=r['reference'],country=r['country']) for uid,r in provenance.items() if r.get('reference')}
profiles.update(json.loads((ROOT/'assets/data/club_profiles.json').read_text())['clubs'])
codes={'England':('E0','E1'),'Scotland':('SC0','SC1'),'Germany':('D1','D2'),'Italy':('I1','I2'),'Spain':('SP1','SP2'),'France':('F1','F2'),'Netherlands':('N1',),'Belgium':('B1',),'Portugal':('P1',),'Greece':('G1',),'Turkey':('T1',)}
tasks=[(country,tier+1,code,season) for country,cs in codes.items() for tier,code in enumerate(cs) for season in ('2122','2223','2324','2425','2526')]
tasks += [(country,1,code,year) for country,code in (('Brazil','BRA'),('Argentina','ARG')) for year in ('2021','2022','2023','2024','2025')]
extra={'China':'CHN','Japan':'JPN','South Korea':'KOR','United States':'USA','Australia':'AUS','Mexico':'MEX','Finland':'FIN','Norway':'NOR','Sweden':'SWE','Ireland':'IRL','Poland':'POL','Romania':'ROM','Denmark':'DNK','Austria':'AUT','Switzerland':'SWZ','Russia':'RUS'}
calendar_codes={'BRA','ARG','CHN','JPN','KOR','USA','FIN','NOR','SWE','IRL'}
for country,code in extra.items():
 tasks.extend((country,1,code,season) for season in (('2021','2022','2023','2024','2025') if code in calendar_codes else ('2122','2223','2324','2425','2526')))
rawcache=CACHE/'tables';rawcache.mkdir(exist_ok=True)
def read(task):
 country,tier,code,season=task;calendar=code in calendar_codes;new=code in set(extra.values())|{'BRA','ARG'};url=f'https://www.football-data.co.uk/new/{code}.csv' if new else f'https://www.football-data.co.uk/mmz4281/{season}/{code}.csv';file=rawcache/(code+'.csv' if new else season+'-'+code+'.csv')
 try:
  with locks[str(file)]:
   if not file.exists():file.write_bytes(urllib.request.urlopen(url,timeout=25).read())
   raw=file.read_bytes()
  table={};matches=0
  for r in csv.DictReader(io.StringIO(raw.decode('utf-8-sig',errors='replace'))):
   if new:
    expected=season if calendar else '20'+season[:2]+'/20'+season[2:]
    if r.get('Season')!=expected:continue
    r.update(FTHG=r.get('HG',''),FTAG=r.get('AG',''),HomeTeam=r.get('Home',''),AwayTeam=r.get('Away',''))
   if not r.get('FTHG','').isdigit() or not r.get('FTAG','').isdigit():continue
   h,a=r['HomeTeam'],r['AwayTeam'];hg,ag=int(r['FTHG']),int(r['FTAG']);matches+=1
   for team,gf,ga in ((h,hg,ag),(a,ag,hg)):
    t=table.setdefault(team,dict(played=0,points=0,gf=0,ga=0));t['played']+=1;t['points']+=3 if gf>ga else 1 if gf==ga else 0;t['gf']+=gf;t['ga']+=ga
  order=sorted(table,key=lambda t:(-table[t]['points'],-(table[t]['gf']-table[t]['ga']),-table[t]['gf'],t))
  return dict(country=country,tier=tier,season=season if calendar else '20'+season[:2]+'-'+season[2:],url=url,sha256=hashlib.sha256(raw).hexdigest(),matches=matches,table=[dict(name=t,position=i+1,teams=len(order),**table[t]) for i,t in enumerate(order)],method='Reconstructed from results; disciplinary deductions and head-to-head tie-break adjustments not applied')
 except Exception as e:return dict(country=country,tier=tier,season=season,url=url,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:tables=list(pool.map(read,tasks))
name_alias={'Atletico-MG':'Atlético Mineiro','Atletico-PR':'Athletico Paranaense','Vitoria':'Vitória BA','Sao Paulo':'São Paulo','Bragantino':'RB Bragantino','Botafogo RJ':'Botafogo','Gremio':'Grêmio','Vasco':'Vasco da Gama','Estudiantes L.P.':'Estudiantes','Gimnasia L.P.':'Gimnasia La Plata','Newells Old Boys':"Newell’s Old Boys",'Velez Sarsfield':'Vélez Sarsfield','Union de Santa Fe':'Unión Santa Fe','CA Central Cordoba':'Central Córdoba','San Martin S.J.':'San Martín San Juan','Newcastle':'Newcastle United','West Ham':'West Ham United','Leeds':'Leeds United','Ipswich':'Ipswich Town','Brighton':'Brighton & Hove Albion','Celta':'Celta Vigo','Man United':'Manchester United','Man City':'Manchester City','Tottenham':'Tottenham Hotspur','Wolves':'Wolverhampton Wanderers','Nott\'m Forest':'Nottingham Forest','West Brom':'West Bromwich Albion','QPR':'Queens Park Rangers','Paris SG':'Paris Saint-Germain','Bayern Munich':'Bayern München','Dortmund':'Borussia Dortmund','M\'gladbach':'Borussia Mönchengladbach','Ein Frankfurt':'Eintracht Frankfurt','Leverkusen':'Bayer Leverkusen','RB Leipzig':'RB Leipzig','Ath Madrid':'Atlético Madrid','Ath Bilbao':'Athletic Bilbao','Sociedad':'Real Sociedad','Betis':'Real Betis','Sp Lisbon':'Sporting CP','Sp Braga':'Braga','Guimaraes':'Vitória Guimarães','Famalicao':'Famalicão','Porto':'FC Porto','St Pauli':'St. Pauli','Hamburg':'Hamburger SV','Hertha':'Hertha BSC','FC Koln':'1. FC Köln','Schalke 04':'Schalke 04','Nurnberg':'1. FC Nürnberg','Kaiserslautern':'1. FC Kaiserslautern','Dusseldorf':'Fortuna Düsseldorf','Greuther Furth':'Greuther Fürth','Karlsruhe':'Karlsruher SC','Paderborn':'SC Paderborn','Magdeburg':'1. FC Magdeburg','Braunschweig':'Eintracht Braunschweig','Paris FC':'Paris FC','St Etienne':'Saint-Étienne','Le Havre':'Le Havre','Ajaccio':'Ajaccio','Frosinone':'Frosinone','Sampdoria':'Sampdoria','Bari':'Bari'}
clubs={};unmapped=[]
for uid,profile in profiles.items():
 name=profile['club'];country=profile['country'];rows=[]
 for table in tables:
  if table['country']!=country or 'error'in table:continue
  matched=next((r for r in table['table'] if norm(name_alias.get(r['name'],r['name']))==norm(name)),None)
  if matched:rows.append(dict(season=table['season'],tier=table['tier'],**matched))
 if rows:
  rows.sort(key=lambda r:r['season']);values=[(60 if r['tier']==1 else 45)+30*(1-(r['position']-1)/max(1,r['teams']-1)) for r in rows]
  rating=round(sum(v*(i+1) for i,v in enumerate(values))/sum(range(1,len(values)+1)),2)
  clubs[uid]=dict(name=name,country=country,rating=rating,seasons=rows,complete_five_seasons=len({r['season'] for r in rows})==5)
 else:unmapped.append(dict(uid=uid,name=name,country=country,reason='No exact matched completed results source; retain existing game rating'))
result=dict(version=1,review_date='2026-11-07',sources=[dict(url='https://api.fifa.com/api/v3/rankings?gender=1&count=300&locale=en-US',sha256=hashlib.sha256((OUT/'fifa-ranking-2026-07-20.json').read_bytes()).hexdigest()),dict(url='https://comp.uefa.com/v2/coefficients?coefficientType=MEN_ASSOCIATION&coefficientRange=OVERALL&seasonYear=2026',sha256=hashlib.sha256((OUT/'uefa-associations-2026.json').read_bytes()).hexdigest())],countries=countries,clubs=clubs,origin_tiers={uid:r['tier_at_origin'] for uid,r in provenance.items()})
(ROOT/'assets/data/league_status.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');OUT.mkdir(exist_ok=True)
(OUT/'coverage.json').write_text(json.dumps(dict(tables=[{k:v for k,v in t.items() if k!='table'} for t in tables],clubs_matched=len(clubs),clubs_complete_five=sum(c['complete_five_seasons'] for c in clubs.values()),unmapped=unmapped,limitations=['Reconstructed standings, not verified official final tables','Missing country/division histories retain existing game ratings','FIFA ranks nations, not leagues; non-European league status is a labelled game proxy']),ensure_ascii=False,indent=2)+'\n')
print('countries',len(countries),'clubs',len(clubs),'complete',sum(c['complete_five_seasons'] for c in clubs.values()),'missing',len(unmapped),'tables',len(tables))
