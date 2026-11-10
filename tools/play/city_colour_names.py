"""City/colour display aliases tied to current club identity and home-kit references."""
import colorsys,json,os,tempfile
from pathlib import Path
from unittest.mock import patch
from tools.play.local_club_names import COUNTRY_FAMILY,norm

COLOURS={
'pt':'Vermelho|Azul|Verde|Branco|Preto|Amarelo|Laranja|Roxo|Bordô|Castanho|Cinza|Celeste',
'br':'Vermelho|Azul|Verde|Branco|Preto|Amarelo|Laranja|Roxo|Bordô|Marrom|Cinza|Celeste',
'en':'Red|Blue|Green|White|Black|Yellow|Orange|Purple|Claret|Brown|Grey|Sky Blue',
'es':'Rojo|Azul|Verde|Blanco|Negro|Amarillo|Naranja|Violeta|Granate|Marrón|Gris|Celeste',
'de':'Rot|Blau|Grün|Weiß|Schwarz|Gelb|Orange|Violett|Weinrot|Braun|Grau|Himmelblau',
'it':'Rosso|Blu|Verde|Bianco|Nero|Giallo|Arancione|Viola|Granata|Marrone|Grigio|Celeste',
'fr':'Rouge|Bleu|Vert|Blanc|Noir|Jaune|Orange|Violet|Bordeaux|Brun|Gris|Ciel',
'nl':'Rood|Blauw|Groen|Wit|Zwart|Geel|Oranje|Paars|Bordeaux|Bruin|Grijs|Hemelsblauw',
}
# Readable identifiers where a white shirt base/overlay alone hides the club colours.
OVERRIDES={
'Benfica':'Vermelho','Benfica B':'Vermelho','Sporting CP':'Verde','Sporting CP B':'Verde','Porto':'Azul','Porto B':'Azul',
'Vitória de Guimarães':'Branco','Casa Pia':'Preto','Nacional':'Branco-Preto','Marítimo':'Verde-Vermelho','Moreirense':'Verde-Branco','Rio Ave':'Verde-Branco','Estoril Praia':'Amarelo-Azul',
'Arsenal':'Red','Chelsea':'Blue','Tottenham Hotspur':'White','Manchester City':'Sky Blue','Manchester United':'Red','Liverpool':'Red','Everton':'Blue','Aston Villa':'Claret','Crystal Palace':'Blue-Red','West Ham United':'Claret-Blue','Newcastle United':'Black-White','Sheffield United':'Red-White','Sheffield Wednesday':'Blue-White',
'Real Madrid':'Blanco','Atlético Madrid':'Rojo-Blanco','Barcelona':'Azul-Grana','Real Betis':'Verde-Blanco','Sevilla':'Blanco','Athletic Bilbao':'Rojo-Blanco','Real Sociedad':'Azul-Blanco','Real Sociedad B':'Azul-Blanco',
'VfL Osnabrück':'Violett','Cremonese':'Rosso-Grigio','Bayern Munich':'Rot','Borussia Dortmund':'Gelb-Schwarz','Bayer Leverkusen':'Rot-Schwarz','RB Leipzig':'Weiß-Rot','Hertha BSC':'Blau-Weiß','Union Berlin':'Rot-Weiß','Borussia Mönchengladbach':'Weiß-Grün',
'Inter Milan':'Nerazzurro','AC Milan':'Rossonero','Juventus':'Bianconero','Torino':'Granata','Roma':'Giallorosso','Lazio':'Celeste','Napoli':'Azzurro','Genoa':'Rosso-Blu','Sampdoria':'Blu-Bianco','Atalanta':'Nero-Blu',
'Paris Saint-Germain':'Bleu-Rouge','Paris FC':'Bleu','Marseille':'Blanc-Ciel','Lyon':'Blanc','Lille':'Rouge','Lens':'Sang-Or','Monaco':'Rouge-Blanc',
'Flamengo':'Vermelho-Preto','Palmeiras':'Verde','Corinthians':'Branco','São Paulo':'Tricolor','Fluminense RJ':'Tricolor','Grêmio':'Azul-Preto','Santos':'Branco','Botafogo':'Branco-Preto','Vasco da Gama':'Preto','Atlético Mineiro':'Preto-Branco','Cruzeiro':'Azul','Internacional':'Vermelho','Bahia':'Tricolor','Vitória BA':'Vermelho-Preto','Sport':'Vermelho-Preto','Náutico':'Vermelho-Branco',
'River Plate':'Blanco-Rojo','Boca Juniors':'Azul-Oro','Racing Club':'Celeste','Independiente':'Rojo','San Lorenzo':'Azul-Rojo','Vélez Sarsfield':'Blanco-Azul','Deportivo Riestra':'Negro','Huracán':'Blanco','Nueva Chicago':'Verde-Negro','Atlanta':'Azul-Oro',
}

def colour(hex_value):
    hex_value=hex_value.lstrip('#')
    rgb=tuple(int(hex_value[i:i+2],16)/255 for i in (0,2,4));h,s,v=colorsys.rgb_to_hsv(*rgb);h*=360
    if v<.05 or (s<.16 and v<.24):return 'Black'
    if s<.16:return 'White' if v>.72 else 'Grey'
    if 170<=h<225 and s<.65 and v>.65:return 'Sky Blue'
    if h<18 or h>=345:return 'Claret' if v<.7 else 'Red'
    if h<47:return 'Brown' if v<.65 else 'Orange'
    if h<70:return 'Yellow'
    if h<170:return 'Green'
    if h<255:return 'Blue'
    if h<345:return 'Purple'
    return 'Red'

def translated(colour_name,family):
    words=COLOURS.get(family,COLOURS['en']).split('|')
    return dict(zip(COLOURS['en'].split('|'),words))[colour_name]

def build(root):
    root=Path(root)
    def read(name):return json.loads((root/name).read_text())
    old=read('assets/data/world_clubs.json')['clubs'];references=read('docs/data/world_club_provenance.json')['clubs'];cities=read('docs/data/club_city_reference.json')['clubs']
    kits=read('assets/data/club_kits.json')['clubs'];proof=read('docs/data/club_kits.provenance.json')['clubs'];current=read('docs/data/name-packs/Scorer-World-Real-Names-0.9.10.json')['clubs']
    from career import CareerMode,club_kit
    class Access:
        def has_world_access(self):return True
    canonical={uid:row['canonical'] for uid,row in old.items()};countries={uid:row['country'] for uid,row in references.items()}
    with tempfile.TemporaryDirectory() as directory,patch.dict(os.environ,STRIKER_SAVE_DIR=directory):
        career=CareerMode(Access(),autoload=False,save_slot='world')
        for league in career.leagues.values():
            for club in league.clubs:canonical[club.uid]=club.name;countries[club.uid]=club.country
    if set(cities)!=set(current) or set(kits)!=set(current):raise ValueError('Current city/name/kit identity coverage mismatch')
    used={};result={};audit=[]
    # Current identities take precedence over old archival source assignments.
    for uid in sorted(canonical,key=lambda u:(u not in current,u)):
        country=countries[uid];family=COUNTRY_FAMILY[country];ref=references.get(uid,{})
        real=current.get(uid)
        if real:
            if cities[uid]['club']!=real or cities[uid]['country']!=country or proof[uid]['country']!=country or proof[uid]['club']!=real or kits[uid]['home']!=proof[uid]['home']:raise ValueError('Current source identity mismatch: '+uid)
            city=cities[uid]['city'];palette=kits[uid]['home'];status='current-real-identity-and-home-colours'
        else:
            city=ref.get('city') or country;palette=old.get(uid,{}).get('colours')
            if not palette:palette=[''.join(f'{round(channel*255):02X}' for channel in rgba[:3]) for rgba in club_kit(canonical[uid])]
            status='legacy-reference-palette' if old.get(uid,{}).get('colours') else 'geography-existing-game-palette'
        primary=('Celeste-Rojo' if country=='Argentina' and real=='Arsenal' else OVERRIDES.get(real)) or translated(colour(palette[0]),family)
        reserve=' B' if real and real.endswith(' B') else ''
        base=f'{city} {primary}';candidates=[base+reserve]
        secondary=translated(colour(palette[3]),family)
        if secondary!=primary:candidates.append(f'{base}-{secondary}{reserve}')
        for form in ('FC {b}','{b} FC','SC {b}','{b} SC','AC {b}','{b} AC','CD {b}','{b} CD','CF {b}','{b} CF','AS {b}','{b} AS','US {b}','{b} US'):
            candidates.append(form.format(b=base+reserve))
        seen=used.setdefault(country,set())
        name=next((n for n in candidates if len(n)<=56 and norm(n) not in seen),None)
        if name is None:raise ValueError('Ambiguous city/colour identifier: '+country+' '+base)
        seen.add(norm(name));result[uid]=dict(country=country,family=family,name=name,canonical=canonical[uid])
        audit.append(dict(uid=uid,country=country,city=city,alias=name,reference=real or ref.get('reference'),palette=palette,status=status))
    return {'version':1,'identity':'city-colour-v1','clubs':result},audit

if __name__=='__main__':
    root=Path(__file__).resolve().parents[2];data,audit=build(root)
    (root/'assets/data/fictional_names.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
    from collections import Counter
    report=dict(version=1,coverage=dict(Counter(r['status'] for r in audit)),current_clubs=[r for r in audit if r['status'].startswith('current')],extra_reference_palettes=[r for r in audit if r['status']=='legacy-reference-palette'])
    (root/'docs/play/CITY_COLOUR_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    for row in audit:
        if row['reference'] in ('Benfica','Sporting CP','Porto','Flamengo','Vitória BA'):print(row['reference'],'->',row['alias'],row['palette'])
