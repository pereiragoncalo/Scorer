"""Build stable World-only presentation defaults from pinned local reference checkouts.

Source checkouts are read as passive data, never imported or executed. This tool
is not run in the game. Do not change canonical clubs/UIDs to change presentation.
"""
import argparse
import csv
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from career import CareerMode, FAMOUS_CLUBS, WORLD_COUNTRIES

COUNTRY_CODES = {'England':'GB','Scotland':'GB','Wales':'GB','Northern Ireland':'GB',
                 'Cape Verde':'CV','Chinese Taipei':'TW','Congo':'CG','DR Congo':'CD',
                 'Macau':'MO','Republic of Ireland':'IE','Tahiti':'PF','Timor-Leste':'TL',
                 'Turkey':'TR','US Virgin Islands':'VI'}
FOOTBALL_NAMES = {'congo-dr':'DR Congo','bosnia-n-herzegovina':'Bosnia and Herzegovina',
                  'czech-republic':'Czechia','ireland':'Republic of Ireland', 'latvija':'Latvia',
                  'macedonia':'North Macedonia','united-states':'United States','monaco':'France'}
CAPITALS = {'England':'London','Scotland':'Edinburgh','Wales':'Cardiff','Northern Ireland':'Belfast','Macau':'Macao'}

CITY_COUNTRY_NAMES = {
 'Moldova':'Moldova, Republic of','Russia':'Russian Federation',
 'Bolivia':'Bolivia, Plurinational State of','Venezuela':'Venezuela, Bolivarian Republic of',
 'British Virgin Islands':'Virgin Islands, British','US Virgin Islands':'Virgin Islands, U.S.',
 'Curacao':'Curaçao','Brunei':'Brunei Darussalam','Chinese Taipei':'Taiwan, Province of China',
 'Iran':'Iran, Islamic Republic of','Laos':"Lao People's Democratic Republic",
 'North Korea':"Korea, Democratic People's Republic of",'South Korea':'Korea, Republic of',
 'Palestine':'Palestine, State of','Syria':'Syrian Arab Republic','Timor-Leste':'Timor-Leste',
 'Vietnam':'Viet Nam','Congo':'Congo','DR Congo':'Congo, The Democratic Republic of the',
 'Ivory Coast':"Côte d'Ivoire",'Tanzania':'Tanzania, United Republic of',
}

FORMS = {
 'en': ('{city} Athletic','{city} Albion','{city} Rovers','AFC {city}','{city} Rangers','{city} Wanderers','{city} United','{city} City'),
 'pt': ('SC {city}','CD {city}','GD {city}','CF {city}','União {city}','Atlético {city}','Estrela {city}','Juventude {city}'),
 'es': ('CD {city}','UD {city}','CF {city}','Atlético {city}','Deportivo {city}','Unión {city}','AD {city}','CA {city}'),
 'fr': ('AS {city}','US {city}','FC {city}','Stade {city}','Racing {city}','Union {city}','Olympique {city}','RC {city}'),
 'de': ('SV {city}','SC {city}','VfB {city}','TSV {city}','FSV {city}','FC {city}','VfL {city}','Sportfreunde {city}'),
 'it': ('AC {city}','US {city}','AS {city}','Polisportiva {city}','FC {city}','Sporting {city}','Calcio {city}','CS {city}'),
 'nl': ('SC {city}','VV {city}','SV {city}','FC {city}','AVV {city}','RKVV {city}','{city} Sport','RKSV {city}'),
 'nordic': ('IF {city}','{city} BK','{city} FK','{city} IF','IK {city}','IL {city}','{city} FF','SK {city}'),
 'slavic': ('FK {city}','SK {city}','NK {city}','FC {city}','FC Lokomotiv {city}','FC Spartak {city}','FC Dynamo {city}','FC Olimpik {city}'),
 'ar': ('Al {city} SC','{city} SC','Al Ittihad {city}','Al Shabab {city}','Al Ahli {city}','{city} FC','Al Wahda {city}','Al Nahda {city}'),
 'tr': ('{city} SK','{city} Spor','FK {city}','{city} Gençlik','{city} Belediye','SC {city}','{city} Atletik','FC {city}'),
 'greek': ('AO {city}','AS {city}','PAE {city}','GS {city}','APO {city}','PO {city}','{city} FC','{city} SC'),
 'br': ('EC {city}','SC {city}','AC {city}','CA {city}','AA {city}','GE {city}','Grêmio {city}','Atlético {city}'),
 'global': ('FC {city}','SC {city}','AC {city}','{city} FC','{city} SC','Sporting {city}','United {city}','{city} Athletic'),
}
MODIFIERS = {'en':('North','South','East','West','Central','Park','Vale','Harbour'),
 'pt':('Norte','Sul','Leste','Oeste','Centro','Atlântico','Jardim','Vale'),
 'es':('Norte','Sur','Este','Oeste','Central','Costa','Parque','Valle'),
 'fr':('Nord','Sud','Est','Ouest','Centre','Maritime','Parc','Vallée'),
 'de':('Nord','Süd','Ost','West','Mitte','Wald','Berg','Tal'),
 'it':('Nord','Sud','Est','Ovest','Centro','Marina','Parco','Valle')}

# Stable representative home colours (shirt, shorts, socks, trim), not current
# licensed kit artwork. These factual supplements are identified in provenance.
COLOURS = {
 'England': {'Arsenal FC':('EF0107','FFFFFF','EF0107','FFFFFF'),'Manchester City FC':('6CABDD','FFFFFF','6CABDD','1C2C5B'),
              'Liverpool FC':('C8102E','C8102E','C8102E','FFFFFF'),'Chelsea FC':('034694','034694','034694','FFFFFF'),
              'Manchester United FC':('DA291C','FFFFFF','111111','FFFFFF'),'Tottenham Hotspur FC':('FFFFFF','132257','FFFFFF','132257')},
 'Portugal': {'SL Benfica':('E60000','FFFFFF','E60000','FFFFFF'), 'Sporting CP':('008548','FFFFFF','008548','FFFFFF'),
             'FC Porto':('005CA9','FFFFFF','005CA9','FFFFFF'),'SC Braga':('D71920','FFFFFF','D71920','FFFFFF'),
             'Vitória de Guimarães':('FFFFFF','111111','FFFFFF','111111'),'Rio Ave FC':('00834A','FFFFFF','00834A','FFFFFF')},
 'Spain': {'Real Madrid CF':('FFFFFF','FFFFFF','FFFFFF','C7A14A'),'FC Barcelona':('004D98','004D98','004D98','A50044'),
           'Atlético Madrid':('CB3524','143E83','CB3524','FFFFFF'),'Athletic Club':('D71920','111111','D71920','FFFFFF'),
           'Villarreal CF':('F5E500','F5E500','F5E500','17459E'),'Real Sociedad':('0067B1','FFFFFF','0067B1','FFFFFF')},
 'Germany': {'Bayern München':('DC052D','DC052D','DC052D','FFFFFF'),'Borussia Dortmund':('FDE100','111111','FDE100','111111'),
             'Bayer 04 Leverkusen':('D0021B','111111','D0021B','111111'),'RB Leipzig':('FFFFFF','DD0741','FFFFFF','DD0741'),
             'Eintracht Frankfurt':('111111','111111','111111','E1000F'),'VfB Stuttgart':('FFFFFF','FFFFFF','FFFFFF','E32219')},
 'Italy': {'Inter':('0068A8','111111','111111','111111'),'AC Milan':('E21B23','111111','111111','111111'),
           'Juventus':('FFFFFF','FFFFFF','FFFFFF','111111'),'Napoli':('12A0D7','FFFFFF','12A0D7','FFFFFF'),
           'AS Roma':('8E1F2F','8E1F2F','8E1F2F','F7B633'),'Atalanta':('1E71B8','111111','111111','111111')},
 'France': {'Paris Saint-Germain':('004170','004170','004170','DA291C'),'Olympique Marseille':('FFFFFF','FFFFFF','FFFFFF','2FAEE0'),
            'AS Monaco':('E21B23','FFFFFF','E21B23','FFFFFF'),'Olympique Lyon':('FFFFFF','FFFFFF','FFFFFF','DA291C'),
            'Lille OSC':('D71920','122C63','D71920','FFFFFF'),'RC Lens':('F7D117','D71920','F7D117','D71920')},
 'Netherlands': {'Ajax':('FFFFFF','FFFFFF','FFFFFF','D71920'),'PSV Eindhoven':('E21B23','111111','FFFFFF','FFFFFF'),
                 'Feyenoord':('D71920','111111','111111','FFFFFF'),'AZ Alkmaar':('D71920','FFFFFF','FFFFFF','FFFFFF')},
 'Scotland': {'Celtic FC':('008E45','FFFFFF','FFFFFF','FFFFFF'),'Rangers FC':('005EB8','FFFFFF','111111','D71920'),
              'Aberdeen FC':('D71920','D71920','D71920','FFFFFF'),'Heart of Midlothian':('800020','FFFFFF','800020','FFFFFF')},
 'Brazil': {'CR Flamengo':('C8102E','FFFFFF','C8102E','111111'),'Palmeiras':('006437','FFFFFF','006437','FFFFFF'),
            'Corinthians':('FFFFFF','111111','FFFFFF','111111'),'São Paulo FC':('FFFFFF','111111','FFFFFF','E21B23'),
            'Fluminense FC':('7B173B','FFFFFF','FFFFFF','00613C'),'Grêmio':('0D80BF','111111','FFFFFF','111111')},
 'Argentina': {'River Plate':('FFFFFF','111111','FFFFFF','E21B23'),'Boca Juniors':('003B7A','003B7A','003B7A','F6C700'),
               'Racing Club':('67BCE8','111111','67BCE8','FFFFFF'),'Independiente':('D71920','FFFFFF','D71920','FFFFFF')},
 'United States': {'Inter Miami':('F7B5CD','111111','F7B5CD','111111'),'LAFC':('111111','111111','111111','C39E6D'),
                  'Seattle Sounders':('5D9741','005695','5D9741','005695'),'Atlanta United':('A6192E','111111','A6192E','111111')},
 'Saudi Arabia': {'Al Hilal':('005DAA','005DAA','005DAA','FFFFFF'),'Al Nassr':('F6D900','00519A','F6D900','00519A'),
                  'Al Ittihad':('F9D616','111111','111111','111111'),'Al Ahli':('00873E','FFFFFF','00873E','FFFFFF')},
}
PRIORITY = {
 'England':('Arsenal FC','Manchester City FC','Liverpool FC','Chelsea FC','Manchester United FC','Tottenham Hotspur FC'),
 'Portugal':('SL Benfica','Sporting CP','FC Porto','SC Braga','Vitória de Guimarães','Rio Ave FC'),
 'Spain':('Real Madrid CF','FC Barcelona','Atlético Madrid','Athletic Club','Villarreal CF','Real Sociedad'),
 'Germany':('Bayern München','Borussia Dortmund','Bayer 04 Leverkusen','RB Leipzig','Eintracht Frankfurt','VfB Stuttgart'),
 'Italy':('Inter','AC Milan','Juventus','Napoli','AS Roma','Atalanta'),
 'France':('Paris Saint-Germain','Olympique Marseille','AS Monaco','Olympique Lyon','Lille OSC','RC Lens'),
 'Netherlands':('Ajax','PSV Eindhoven','Feyenoord','AZ Alkmaar','FC Twente','FC Utrecht'),
 'Scotland':('Celtic FC','Rangers FC','Aberdeen FC','Heart of Midlothian','Hibernian FC','Dundee United FC'),
 'Brazil':('CR Flamengo','Palmeiras','Corinthians','São Paulo FC','Fluminense FC','Grêmio'),
 'Argentina':('River Plate','Boca Juniors','Racing Club','Independiente','San Lorenzo','Vélez Sarsfield'),
 'United States':('Inter Miami','LAFC','Seattle Sounders','Atlanta United','New York City','Columbus Crew'),
 'Saudi Arabia':('Al Hilal','Al Nassr','Al Ittihad','Al Ahli','Al Ettifaq','Al Shabab'),
}


def norm(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value).casefold() if c.isalnum())


def read_refs(root):
    result, banned = defaultdict(list), set()
    for path in sorted(root.rglob('*.clubs.txt')):
        country = FOOTBALL_NAMES.get(path.parent.name, path.parent.name.replace('-', ' ').title())
        if country not in WORLD_COUNTRIES: continue
        current = None
        for raw in path.read_text(encoding='utf-8-sig').splitlines():
            line = raw.split('#',1)[0].strip()
            if not line or line.startswith(('=', '@')): continue
            if line.startswith('|'):
                if current:
                    for alias in line.split('|')[1:]:
                        alias = re.sub(r'\[[^]]+\]', '', alias).strip()
                        if alias: current['aliases'].append(alias); banned.add(norm(alias))
                continue
            if raw[:1].isspace() or line.startswith(('i)', 'ii)', 'iii)')): continue
            parts = [s.strip() for s in line.split(',')]
            name = re.sub(r'\s*\([^)]*\)', '', parts[0]).strip()
            if not name: continue
            banned.add(norm(name));current=None
            if len(parts)<2 or re.search(r'\(\d{4}-|\(-\d',line): continue
            city = re.sub(r'\s*\([^)]*\)', '', parts[-1]).split('›')[0].strip()
            if not 2 <= len(city) <= 45 or city.startswith('@') or city[:1].isdigit(): continue
            if any(x in city for x in ('http', '[', ']', '?', '=')): continue
            current = {'name':name,'city':city,'aliases':[name]}
            result[country].append(current)
    return result, banned


def style_family(country, metadata):
    if country == 'Turkey': return 'tr'
    if country == 'Brazil': return 'br'
    if country in ('Greece','Cyprus'): return 'greek'
    if country in ('Denmark','Sweden','Norway','Finland','Iceland','Faroe Islands'): return 'nordic'
    if country in ('Russia','Ukraine','Belarus','Czechia','Slovakia','Slovenia','Croatia','Serbia','Montenegro','North Macedonia','Bosnia and Herzegovina','Bulgaria','Poland'): return 'slavic'
    language = metadata.get('languages',[''])[0]
    return language if language in FORMS else 'global'


def adapt(city, family, seed, used, banned):
    forms = FORMS[family]; offset=seed % len(forms)
    for generation in range(1000):
        form = forms[(offset+generation) % len(forms)]
        candidate = form.format(city=city)
        if generation >= len(forms):
            words = MODIFIERS.get(family, ('Central','North','South','East','West','Coastal','Valley','Park'))
            level = generation // len(forms)-1
            candidate += ' ' + words[level % len(words)]
            if level >= len(words): candidate += ' ' + forms[level//len(words) % len(forms)].split()[0].replace('{city}','SC')
        candidate = unicodedata.normalize('NFC', candidate)
        key=norm(candidate)
        if len(candidate)<=56 and key not in used and key not in banned:
            used.add(key);return candidate
    raise ValueError('Cannot generate a distinct adapted club name for '+city)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clubs',type=Path,required=True);parser.add_argument('--countries',type=Path,required=True)
    parser.add_argument('--football-data',type=Path,required=True)
    parser.add_argument('--cities',type=Path,required=True)
    args=parser.parse_args()
    countries=json.loads((args.countries/'dist/countries.min.json').read_text())
    by_name={v['name']:v for v in countries.values()}
    refs,banned=read_refs(args.clubs)
    city_rows=list(csv.DictReader((args.cities/'data/world-cities.csv').open(encoding='utf-8')))
    city_index=defaultdict(list)
    for city_row in city_rows:
        city_index[city_row['country']].append(city_row)
    espn=json.loads((args.football_data/'EPL 1992 - 2015/epl-teams-2013-2014.json').read_text())
    espn_colours={norm(t['name']):t['color'].upper() for t in espn['sports'][0]['leagues'][0]['teams'] if t.get('color')}
    class Access:
        def has_world_access(self):return True
    import os
    with tempfile.TemporaryDirectory() as temp:
        previous=os.environ.get('STRIKER_SAVE_DIR');os.environ['STRIKER_SAVE_DIR']=temp
        try:career=CareerMode(Access(),autoload=False,save_slot='world')
        finally:
            if previous is None:os.environ.pop('STRIKER_SAVE_DIR',None)
            else:os.environ['STRIKER_SAVE_DIR']=previous
    output={};provenance={};stats={'regions':0,'regions_with_club_city_references':0,'clubs_with_reference':0,'clubs_with_reference_palette':0,'regions_with_multiple_cities':0}
    for country in sorted(WORLD_COUNTRIES):
        metadata=by_name.get(country) or countries[COUNTRY_CODES[country]]
        capital=CAPITALS.get(country) or metadata['capital']
        if not capital:raise ValueError('Missing city for '+country)
        city_country=CITY_COUNTRY_NAMES.get(country, metadata['name'])
        geographic=city_index[city_country]
        if country in ('England','Scotland','Wales','Northern Ireland'):
            geographic=[row for row in geographic if row['subcountry']==country]
        city_pool=[capital]
        seen_cities={norm(capital)}
        for row in geographic:
            city=unicodedata.normalize('NFC',row['name'])
            if 2<=len(city)<=40 and norm(city) not in seen_cities and all(c.isprintable() and c not in '<>[]' for c in city):
                city_pool.append(city);seen_cities.add(norm(city))
        stats['regions_with_multiple_cities']+=len(city_pool)>1
        records=refs[country]
        priorities=[]
        for requested in PRIORITY.get(country,()):
            record=next((r for r in records if norm(requested) in {norm(x) for x in r['aliases']}),None)
            if record is None:
                record=next((r for r in records if norm(requested).removesuffix('fc') in {norm(x).removesuffix('fc') for x in r['aliases']}),None)
            if record and record not in priorities:priorities.append(record)
        ordered=priorities+[r for r in records if r not in priorities]
        used=set();family=style_family(country,metadata);sequence=0
        colour_index={norm(k):v for k,v in COLOURS.get(country,{}).items()}
        for league in sorted((v for v in career.leagues.values() if v.country==country),key=lambda l:l.tier):
            famous=FAMOUS_CLUBS.get(country,()) if league.tier==1 else ()
            clubs=sorted(league.clubs,key=lambda c:(famous.index(c.name) if c.name in famous else 100,c.uid))
            for club in clubs:
                reference=ordered[sequence % len(ordered)] if ordered else None
                city=unicodedata.normalize('NFC',reference['city'] if reference else city_pool[sequence % len(city_pool)])
                aliases={norm(x) for x in reference['aliases']} if reference else set()
                colours=next((v for k,v in colour_index.items() if k in aliases),None)
                if not colours and country=='England':
                    primary=next((v for k,v in espn_colours.items() if k in aliases or k in {a.removesuffix('fc') for a in aliases}),None)
                    if primary:colours=(primary,'FFFFFF',primary,'FFFFFF' if primary not in ('FFFFFF','ffffff') else '111111')
                name=adapt(city,family,sequence,used,banned)
                row={'canonical':club.name,'name':name,'city':city}
                if colours:row['colours']=['#'+v for v in colours]
                output[club.uid]=row
                provenance[club.uid]={'country':country,'tier_at_origin':league.tier,'adapted':name,'city':city,
                                      'reference':reference['name'] if reference else None,'colours':row.get('colours')}
                stats['clubs_with_reference']+=int(reference is not None)
                stats['clubs_with_reference_palette']+=int(bool(colours));sequence+=1
        stats['regions']+=1;stats['regions_with_club_city_references']+=bool(ordered)
    source_info={name:subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()
                 for name,path in [('openfootball/clubs',args.clubs),('annexare/Countries',args.countries),('jokecamp/FootballData',args.football_data),('datasets/world-cities',args.cities)]}
    (ROOT/'assets/data/world_clubs.json').write_text(json.dumps({'version':1,'sources':source_info,'clubs':output},ensure_ascii=False,separators=(',',':'))+'\n')
    (ROOT/'docs/data/world_club_provenance.json').write_text(json.dumps({'version':1,'sources':source_info,'stats':stats,'clubs':provenance},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'assets/data/OPENFOOTBALL-CC0.license').write_bytes((args.clubs/'LICENSE.md').read_bytes())
    (ROOT/'assets/data/COUNTRIES-MIT.license').write_bytes((args.countries/'LICENSE').read_bytes())
    (ROOT/'assets/data/GEONAMES-CCBY4.license').write_text('City names from GeoNames, https://www.geonames.org/, via https://github.com/datasets/world-cities at '+source_info['datasets/world-cities']+'; Creative Commons Attribution 4.0 International, https://creativecommons.org/licenses/by/4.0/. Changes: sampling cities and creating fictional club display names with local prefixes/suffixes. No endorsement by GeoNames or the source projects. Country labels used only to join against the existing game country model.\n')
    print(json.dumps(stats,indent=2));print('clubs:',len(output))


if __name__=='__main__':main()
