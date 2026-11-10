"""Original fictional club names with explicit country conventions, offline only."""
import hashlib,json,re,unicodedata,os,tempfile
from pathlib import Path

# (fictional locality stems, endings, football name forms). No real club identity.
BANKS = {
'en':('Amber Birch Cedar Fern Glen Hazel Iron Lark','brook dale haven hill mere ridge vale well','{p} United|{p} Rovers|{p} Athletic|{p} Town|{p} City|{p} Rangers|{p} Wanderers|AFC {p}'),
'pt':('Vale Monte Ribeira Fonte Serra Vila Lago Penedo','douro lume alta clara verde brava nova serena','GD {p}|União de {p}|Atlético de {p}|CD {p}|Juventude de {p}|Estrela de {p}|SC {p}|CF {p}'),
'br':('Serra Vila Rio Porto Campo Lagoa Pedra Monte','dourada verde clara nova alta bela serena azul','EC {p}|Grêmio {p}|Atlético de {p}|AA {p}|SC {p}|AC {p}|GE {p}|CA {p}'),
'es':('Val Monte Peña Villa Fuente Sierra Prado Rio','claro dorado verde nuevo alto blanco sereno lindo','CD {p}|UD {p}|Atlético de {p}|Deportivo {p}|Unión de {p}|CF {p}|AD {p}|CA {p}'),
'fr':('Val Mont Roche Belle Clair Bois Font Haute','dor rive clair val bois lune mer pré','AS {p}|US {p}|Stade {p}|FC {p}|Union de {p}|RC {p}|Sporting {p}|Olympique de {p}'),
'de':('Berg Wald Linden Falken Sonnen Eichen Hohen Rosen','tal heim feld burg au dorf hain berg','SV {p}|VfB {p}|TSV {p}|SC {p}|FSV {p}|FC {p}|VfL {p}|Sportfreunde {p}'),
'it':('Val Monte Fonte Rocca Villa Colle Ponte Castel','chiara verde nuovo sereno alto doro luna mare','AC {p}|US {p}|AS {p}|Polisportiva {p}|FC {p}|Sporting {p}|Calcio {p}|CS {p}'),
'nl':('Zonne Linden Valken Duin Eiken Water Groen Zilver','dam veld wijk burg berg hout duin meer','VV {p}|SV {p}|SC {p}|FC {p}|AVV {p}|RKVV {p}|{p} Sport|RKSV {p}'),
'nordic':('Sol Björk Lind Gran Fjord Strand Skog Nord','vik lund dal berg sund heim by holm','IF {p}|{p} BK|{p} FK|{p} IF|IK {p}|IL {p}|{p} FF|SK {p}'),
'fi':('Kivi Koivu Kuusi Mänty Järvi Sini Kulta Lehti','lahti niemi järvi koski vaara mäki salo ranta','{p} FC|{p} JK|{p} United|{p} PS|{p} TP|{p} IF|{p} SK|FC {p}'),
'is':('Sól Bjark Lind Hrafn Silfur Stein Fjall Dal','vík dalur nes fjörður berg höfn lundur fell','ÍF {p}|{p} FK|{p} ÍF|FC {p}|{p} SK|{p} BK|{p} KF|KF {p}'),
'slavic':('Belo Novo Zelen Gora Rad Mira Slavo Zora','grad polje bor dolina gora most voda vec','FK {p}|SK {p}|NK {p}|FC {p}|Lokomotiv {p}|Spartak {p}|Dynamo {p}|Olimpik {p}'),
'ro':('Valea Poiana Piatra Dealul Runcul Izvorul Codrul Lacul','Nou Verde Mare Alb Senin Auriu Frumos Lin','FC {p}|CS {p}|AS {p}|Unirea {p}|Viitorul {p}|Sportul {p}|Olimpia {p}|Gloria {p}'),
'hu':('Arany Ezüst Fenyő Kő Hárs Duna Tölgy Nap','völgy hegy liget halom kert mező falu patak','{p} SE|{p} SC|FC {p}|{p} SK|{p} TE|{p} TC|{p} VSE|{p} AC'),
'lt':('Ąžuol Berž Saul Žal Aukso Šil Kaln Up','ynas giris upis kiemis alis inis avas ytis','FK {p}|FC {p}|SK {p}|{p} FK|{p} SC|{p} SK|{p} FC|FC Žara {p}'),
'lv':('Saul Ozol Bērz Zelt Zaļ Kaln Up Mež','upe kalne ciems mala lauki iņi āji ezers','FK {p}|SK {p}|FC {p}|{p} FK|{p} SK|{p} FC|FS {p}|{p} Sporta'),
'et':('Kase Tamme Päikese Kulla Männi Jõe Kivi Rohe','la küla mäe järve valla salu metsa ranna','JK {p}|FC {p}|SK {p}|{p} JK|{p} SK|{p} FC|JK Kalev {p}|FC Täht {p}'),
'ar':('Nur Safa Qamar Rimal Wadi Sahra Zahra Jabal','dara nura mira sahil farah zahir nada rawan','Al {p} SC|{p} SC|Al Ittihad {p}|Al Shabab {p}|Al Ahli {p}|{p} FC|Al Wahda {p}|Al Nahda {p}'),
'fa':('Roshan Mehr Dara Koh Gul Sabz Sorna Zarin','abad rud shahr dasht kuh zar van sar','FC {p}|{p} FC|{p} SC|Setareh {p}|Omid {p}|Navid {p}|Baharan {p}|Mehr {p}'),
'tr':('Altın Güneş Ak Yeşil Çam Gümüş Kuzey Kaya','dere tepe ova kent yurt hisar bağ dağ','{p} SK|{p} Spor|FK {p}|{p} Gençlik|{p} Belediye|SC {p}|{p} Atletik|FC {p}'),
'central':('Ak Altyn Kök Nur Tal Sary Kara Besh','tau dala su kent bulak tepa kala jar','FC {p}|FK {p}|{p} FK|{p} FC|SK {p}|SC {p}|{p} SK|{p} SC'),
'el':('Aster Akti Lefko Chryso Nea Petra Kato Ano','polis lithi vrysi limni kori nera xenia dora','AO {p}|AS {p}|PAE {p}|GS {p}|APO {p}|PO {p}|{p} FC|{p} SC'),
'sq':('Drita Lumi Guri Mali Besa Ylli Fusha Lule','bardh arta nova dora mira bora lira vala','KF {p}|KS {p}|FK {p}|FC {p}|{p} KF|{p} KS|{p} FK|{p} FC'),
'hy':('Arev Ardziv Lus Nor Tsagh Vard Sev Vos','avan kert dzor shen ak ar ir an','FC {p}|FK {p}|{p} FC|{p} SC|Ardziv {p}|Lus {p}|Nor {p}|Voski {p}'),
'ka':('Mze Mtsva Vard Gora Akha Dila Tskha Bela','nari veli dara turi neli vasi meri gori','FC {p}|FK {p}|{p} FC|{p} SC|SK {p}|SC {p}|Mze {p}|Dila {p}'),
'he':('Or Gan Tal Har Nof Neve Ein Sde','hadar rimon keren shahar alon zahav nitzan barak','Hapoel {p}|Maccabi {p}|Beitar {p}|FC {p}|SC {p}|Ironi {p}|Bnei {p}|{p} FC'),
'ja':('Aka Ao Kawa Yama Mizu Mori Hoshi Hara','sora kawa hara yama no mizu shima saki','{p} FC|{p} SC|FC {p}|{p} United|{p} Seiun|{p} Aozora|{p} Hikari|{p} Verde'),
'ko':('Haneul Pureun Saebit Byeol Nuri Haesol Dal Gang','san gang bit maeul uri won hae seong','{p} FC|{p} SC|FC {p}|{p} Citizen|{p} United|{p} SK|{p} City|SC {p}'),
'zh':('Jin Qing Bai Yun Hai Shan Long Xing','he shan lin cheng jiang hai guang yue','{p} FC|{p} SC|FC {p}|{p} United|{p} City|{p} Athletic|SC {p}|{p} Sport'),
'vi':('Sơn Hải Kim Thanh Minh Hồng Lam Thiên','Hà Sơn Giang Lâm Phong Châu Minh Ngọc','CLB {p}|{p} FC|FC {p}|{p} SC|{p} Sport|{p} United|SC {p}|{p} City'),
'sea':('Surya Bumi Taman Nusa Bukit Sinar Laut Bintang','jaya sari indah baru raya emas hijau muda','FC {p}|{p} FC|SC {p}|{p} SC|{p} United|{p} City|{p} Putra|{p} Muda'),
'th':('Saeng Dao Khao Nam Thong Fah Ban Phu','sai thara nara wan buri dara chom kaew','{p} FC|FC {p}|{p} United|{p} City|{p} SC|SC {p}|{p} Sport|{p} Athletic'),
'southasia':('Surya Tara Nadi Sona Pahar Naya Shanti Hima','pur nagar gaon bari nadi tara ban giri','{p} FC|{p} SC|{p} United|FC {p}|SC {p}|{p} Sporting|{p} Club|{p} Athletic'),
'mn':('Altan Tsagaan Khukh Naran Saran Boro Ulaan Nogoon','tal gol uul nuur khangai bulag khad tolg','FC {p}|{p} FC|SC {p}|{p} SC|{p} United|{p} SK|{p} Sport|{p} City'),
'sw':('Mwangaza Kijani Mto Jua Mlima Nyota Bahari Dhahabu','pya njema wazi kuu safi bora mbali nuru','FC {p}|SC {p}|{p} FC|{p} SC|Nyota {p}|Umoja {p}|{p} United|{p} Stars'),
'pacific':('Mata Vala Moana Aro Tasi Luma Fetu Namo','lani nalu vai fenua tahi roa manu lea','FC {p}|SC {p}|{p} FC|{p} SC|{p} United|{p} Stars|{p} Sport|{p} City'),
}
PLACES = {
'pt': ('Valedouro','Montelume','Ribeiralta','Fonteclara','Serralva','Vilaserena','Penedouro','Vale Sereno','Monte Claro','Ribeira Nova','Fonte Dourada','Serra Brava','Vila do Lume','Lago Sereno','Penedo Alto','Vale da Aurora','Monte das Fontes','Ribeira do Sol','Fonte do Mar','Serra do Vale','Vila da Encosta','Lago das Flores','Penedo Verde','Vale das Oliveiras'),
'br': ('Vila Serena','Serra Dourada','Rio Claro do Sul','Porto das Estrelas','Campo da Aurora','Lagoa Verde','Pedra Serena','Monte do Sol','Vila das Palmeiras','Serra do Luar','Rio das Flores','Porto do Vale','Campo das Águas','Lagoa Dourada','Pedra Azul','Monte Sereno','Vila do Horizonte','Serra Bonita','Rio do Cedro','Porto das Flores','Campo do Luar','Lagoa do Sol','Pedra Dourada','Monte da Aurora'),
'es': ('Valle Sereno','Monte Claro','Peña Dorada','Villa del Alba','Fuente Serena','Sierra Verde','Prado del Sol','Río del Alba','Valle Dorado','Monte del Cielo','Peña Verde','Villa Serena','Fuente del Alba','Sierra Clara','Prado Dorado','Río Sereno','Valle del Olivo','Monte de la Luna','Peña Clara','Villa del Sol','Fuente Dorada','Sierra del Alba','Prado Sereno','Río de la Luna'),
'it': ('Valserena','Montechiaro','Fontechiara','Roccaluna','Villaverde','Collesereno','Pontedoro','Castelverde','Valdiluce','Montelume','Fontenuova','Roccaverde','Villaluna','Colledoro','Pontechiaro','Castellume','Valdoro','Montesereno','Fonteluna','Roccaserena','Villachiara','Colleverde','Pontelume','Castelnuovo'),
}

GROUPS={
'pt':'Portugal|Angola|Cape Verde|Guinea-Bissau|Mozambique|Sao Tome and Principe|Timor-Leste',
'br':'Brazil',
'es':'Andorra|Spain|Argentina|Bolivia|Chile|Colombia|Ecuador|Paraguay|Peru|Uruguay|Venezuela|Costa Rica|Cuba|Dominican Republic|El Salvador|Guatemala|Honduras|Mexico|Nicaragua|Panama|Puerto Rico|Equatorial Guinea',
'fr':'France|Luxembourg|Belgium|Haiti|Benin|Burkina Faso|Burundi|Cameroon|Central African Republic|Chad|Comoros|Congo|DR Congo|Djibouti|Gabon|Guinea|Ivory Coast|Madagascar|Mali|Mauritius|Niger|Rwanda|Senegal|Seychelles|Togo|New Caledonia|Tahiti',
'de':'Austria|Germany|Liechtenstein|Switzerland',
'it':'Italy|San Marino', 'nl':'Netherlands|Aruba|Curacao|Suriname',
'nordic':'Denmark|Sweden|Norway|Faroe Islands','fi':'Finland','is':'Iceland',
'slavic':'Russia|Ukraine|Belarus|Czechia|Slovakia|Slovenia|Croatia|Serbia|Montenegro|North Macedonia|Bosnia and Herzegovina|Bulgaria|Poland',
'ro':'Romania|Moldova','hu':'Hungary','lt':'Lithuania','lv':'Latvia','et':'Estonia',
'ar':'Algeria|Bahrain|Egypt|Iraq|Jordan|Kuwait|Lebanon|Libya|Mauritania|Morocco|Oman|Palestine|Qatar|Saudi Arabia|Sudan|Syria|Tunisia|United Arab Emirates|Yemen',
'fa':'Afghanistan|Iran|Tajikistan','tr':'Turkey|Azerbaijan','central':'Kazakhstan|Kyrgyzstan|Turkmenistan|Uzbekistan',
'el':'Greece|Cyprus','sq':'Albania|Kosovo','hy':'Armenia','ka':'Georgia','he':'Israel',
'ja':'Japan','ko':'South Korea|North Korea','zh':'China|Chinese Taipei|Hong Kong|Macau','vi':'Vietnam',
'sea':'Indonesia|Malaysia|Brunei|Singapore','th':'Thailand|Cambodia|Laos|Myanmar','southasia':'Bangladesh|Bhutan|India|Maldives|Nepal|Pakistan|Sri Lanka','mn':'Mongolia',
'sw':'Kenya|Tanzania|Uganda|Ethiopia|Eritrea|Somalia',
'pacific':'American Samoa|Cook Islands|Fiji|Samoa|Solomon Islands|Tonga|Vanuatu',
'en':'England|Scotland|Wales|Northern Ireland|Republic of Ireland|Gibraltar|Malta|United States|Canada|Australia|New Zealand|Anguilla|Antigua and Barbuda|Bahamas|Barbados|Belize|Bermuda|British Virgin Islands|Cayman Islands|Dominica|Grenada|Guyana|Jamaica|Montserrat|Saint Kitts and Nevis|Saint Lucia|Saint Vincent and the Grenadines|Trinidad and Tobago|Turks and Caicos Islands|US Virgin Islands|Guam|Northern Mariana Islands|Philippines|Botswana|Eswatini|Gambia|Ghana|Lesotho|Liberia|Malawi|Namibia|Nigeria|Sierra Leone|South Africa|South Sudan|Zambia|Zimbabwe|Papua New Guinea'
}
COUNTRY_FAMILY={country:family for family,countries in GROUPS.items() for country in countries.split('|')}

def norm(text):return ''.join(c for c in unicodedata.normalize('NFKD',text).casefold() if c.isalnum())

def build(root):
    root=Path(root);world=json.loads((root/'assets/data/world_clubs.json').read_text())['clubs']
    provenance=json.loads((root/'docs/data/world_club_provenance.json').read_text())['clubs']
    # Include clubs created by the current domestic formats, beyond legacy archive UIDs.
    import sys
    sys.path.insert(0,str(root))
    from career import CareerMode
    class Access:
        def has_world_access(self):return True
    from unittest.mock import patch
    with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ,STRIKER_SAVE_DIR=directory):
        career=CareerMode(Access(),autoload=False,save_slot='world')
        for league in career.leagues.values():
            for club in league.clubs:
                if club.uid not in world:
                    world[club.uid]={'canonical':club.name,'name':club.name}
                    provenance[club.uid]={'country':club.country}
    banned={norm(row['name']) for row in world.values()}|{norm(row['reference']) for row in provenance.values() if row.get('reference')}
    profiles=json.loads((root/'assets/data/club_profiles.json').read_text())['clubs'];banned|={norm(row['club']) for row in profiles.values()}
    countries={row['country'] for row in provenance.values()}
    if countries-set(COUNTRY_FAMILY):raise ValueError('Country conventions missing: '+str(countries-set(COUNTRY_FAMILY)))
    output={};used={country:set() for country in countries}
    for uid,row in sorted(world.items()):
        country=provenance[uid]['country'];family=COUNTRY_FAMILY[country];starts,ends,forms=BANKS[family];starts=starts.split();ends=ends.split();forms=forms.split('|')
        seed=int.from_bytes(hashlib.sha256(('scorer-local-v1:'+uid).encode()).digest()[:8],'big')
        for attempt in range(4096):
            value=seed+attempt;first=starts[(value//8)%len(starts)];last=ends[(value//64)%len(ends)]
            place=PLACES[family][(value//8)%len(PLACES[family])] if family in PLACES else first+(' ' if family in ('ro','sw','vi') else '')+last
            name=forms[value%len(forms)].format(p=place)
            if norm(name) not in used[country] and norm(name) not in banned:
                output[uid]={'country':country,'family':family,'name':name,'canonical':row['canonical']};used[country].add(norm(name));break
        else:raise ValueError('Cannot assign distinct fictional name')
    return {'version':1,'identity':'fictional-local-v1','clubs':output}

if __name__=='__main__':
    root=Path(__file__).resolve().parents[2];result=build(root)
    (root/'assets/data/fictional_names.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
    for country in ('Portugal','Brazil','Argentina','France','Germany','Italy','Japan'):
        print(country,[r['name'] for r in result['clubs'].values() if r['country']==country][:5])
