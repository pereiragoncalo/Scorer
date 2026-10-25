import json,pathlib,importlib.metadata,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from babel import Locale
from device_locale import REGIONS
from career import WORLD_COUNTRIES
out=ROOT/'assets/i18n';langs=['en','pt','es','de','it','ko','ja','zh','vi']
iso={name:code for code,name in REGIONS.items()};data={}
manual={
'England':['England','Inglaterra','Inglaterra','England','Inghilterra','잉글랜드','イングランド','英格兰','Anh'],
'Scotland':['Scotland','Escócia','Escocia','Schottland','Scozia','스코틀랜드','スコットランド','苏格兰','Scotland'],
'Wales':['Wales','País de Gales','Gales','Wales','Galles','웨일스','ウェールズ','威尔士','Wales'],
'Northern Ireland':['Northern Ireland','Irlanda do Norte','Irlanda del Norte','Nordirland','Irlanda del Nord','북아일랜드','北アイルランド','北爱尔兰','Bắc Ireland'],
'Chinese Taipei':['Chinese Taipei','Taipé Chinês','Taipéi Chino','Chinesisch Taipeh','Taipei Cinese','차이니스 타이베이','チャイニーズタイペイ','中华台北','Đài Bắc Trung Hoa']}
for i,lang in enumerate(langs):
 locale=Locale.parse({'pt':'pt_PT','zh':'zh_Hans'}.get(lang,lang))
 data[lang]={}
 for country in WORLD_COUNTRIES:
  value=country if lang=='en' else str(locale.territories.get(iso.get(country,''),country))
  if country in manual:value=manual[country][i]
  data[lang][country]=value
(out/'countries.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
dist=importlib.metadata.distribution('Babel')
for f in dist.files:
 if f.name=='LICENSE':(out/'Babel.license').write_bytes(pathlib.Path(dist.locate_file(f)).read_bytes());break
print('Country labels:',len(WORLD_COUNTRIES),'languages:',len(langs),'Babel',dist.version)
