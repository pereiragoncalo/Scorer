"""Offline UI localisation. Never translate stored names, IDs or career data."""
from contextlib import contextmanager
from contextvars import ContextVar
from functools import lru_cache
import json
import os
from pathlib import Path
import re
import string
import tempfile

LANGUAGES = {'en':'English','pt':'Português','es':'Español','de':'Deutsch',
             'it':'Italiano','ko':'한국어','ja':'日本語','zh':'简体中文','vi':'Tiếng Việt'}
ROOT = Path(__file__).resolve().parent
class Rendered(str):
    pass

_ACTIVE = ContextVar('scorer_ui_language', default=None)
CJK_FONTS = {'ko':'NotoSansCJKkr-Regular.otf','ja':'NotoSansCJKjp-Regular.otf','zh':'NotoSansCJKsc-Regular.otf'}


def language_for_tag(tag):
    code=str(tag or '').replace('_','-').split('-')[0].lower()
    return code if code in LANGUAGES else 'en'


@lru_cache(maxsize=9)
def catalogue(language):
    if language not in LANGUAGES:language='en'
    try:
        path=ROOT/'assets/i18n'/f'{language}.json'
        if path.stat().st_size>256*1024:raise ValueError('Oversized UI catalogue')
        data=json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data,dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in data.items()):raise ValueError('Invalid UI catalogue')
        return data
    except (OSError,ValueError):return {}


@lru_cache(maxsize=1)
def country_catalogue():
    try:return json.loads((ROOT/'assets/i18n/countries.json').read_text(encoding='utf-8'))
    except (OSError,ValueError):return {}


@lru_cache(maxsize=1)
def patterns():
    rows=[]
    for source in catalogue('en'):
        pieces=[];fields=[];literals=''
        for literal,field,_,_ in string.Formatter().parse(source):
            literals+=literal;pieces.append(re.escape(literal))
            if field is not None:
                if not re.fullmatch(r'[a-z][a-z0-9_]*',field):raise ValueError('Invalid UI placeholder')
                pieces.append('(?P<'+field+'>.*?)' if field not in fields else '(?P='+field+')');fields.append(field)
        if fields and sum(x.isalpha() for x in literals)>=2:
            rows.append((len(literals),re.compile(''.join(pieces),re.DOTALL),source))
    return [(regex,source) for _,regex,source in sorted(rows,key=lambda x:-x[0])]


class Localizer:
    def __init__(self,world=False,tag='',directory=None):
        self.world=bool(world);self.system_language=language_for_tag(tag)
        self.choice='auto';self.directory=Path(directory) if directory is not None else None
        self.revision=0;self.missing=set()
        if self.world and self.directory:
            try:
                p=self.directory/'scorer_language.json'
                if p.stat().st_size<=1024:
                    data=json.loads(p.read_text(encoding='utf-8'))
                    if type(data.get('version')) is int and data.get('version')==1 and data.get('language') in ('auto',*LANGUAGES):self.choice=data['language']
            except (OSError,ValueError,AttributeError):pass

    @property
    def language(self):
        return (self.system_language if self.choice=='auto' else self.choice) if self.world else 'en'

    def choose(self,choice):
        if not self.world or choice not in ('auto',*LANGUAGES):return False
        temporary=None
        try:
            if self.directory:
                self.directory.mkdir(parents=True,exist_ok=True)
                with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=self.directory,prefix='.scorer-language-',delete=False) as out:
                    temporary=Path(out.name);json.dump({'version':1,'language':choice},out)
                    out.flush();os.fsync(out.fileno())
                os.replace(temporary,self.directory/'scorer_language.json')
            self.choice=choice;self.revision+=1;self.missing.clear();return True
        except OSError:return False
        finally:
            if temporary:temporary.unlink(missing_ok=True)

    def refresh_system(self,tag):
        language=language_for_tag(tag)
        if language!=self.system_language:
            self.system_language=language
            if self.world and self.choice=='auto':self.revision+=1

    def country(self,name):
        return country_catalogue().get(self.language,{}).get(str(name),str(name)) if self.world else str(name)

    def tr(self,text,**values):
        if isinstance(text,Rendered):return text
        text=str(text)
        language=self.language
        if language=='en':return text.format(**values) if values else text
        translated=catalogue(language)
        if text in translated:
            result=translated[text]
            return Rendered(result.format(**values) if values else result)
        if text in translated.values():return Rendered(text)
        if not values:
            for regex,source in patterns():
                match=regex.fullmatch(text)
                if match:
                    data=match.groupdict()
                    if 'country' in data:data['country']=self.country(data['country'])
                    return Rendered(translated.get(source,source).format(**data))
        if len(self.missing)<256 and any(c.isalpha() for c in text) and text.strip():self.missing.add(text)
        return text.format(**values) if values else text

    def date(self,value):
        if self.language=='en':
            months=('JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC')
            return f'{value.day:02d} {months[value.month-1]} {value.year}'
        if self.language in ('ko','ja','zh'):return value.strftime('%Y/%m/%d')
        return value.strftime('%d/%m/%Y')

    def league(self,career,league):
        shown=career.display_league(league)
        if league.key in career.display_aliases.get('leagues',{}):return Rendered(shown)
        if league.name==f'{league.country} Division {league.tier}':
            return self.tr('{country} Division {tier}',country=self.country(league.country),tier=league.tier)
        return Rendered(shown)

    def competition(self,career,title,country=None):
        for league in career.leagues.values():
            if (country is None or league.country==country) and title==league.name:
                return self.league(career,league)
        suffix=' National Cup'
        if title.endswith(suffix) and title[:-len(suffix)] in country_catalogue().get('en',{}):
            return self.tr('{country} National Cup',country=self.country(title[:-len(suffix)]))
        return Rendered(career.display_text(title,country))

    def font(self,text='',explicit=None):
        if explicit:return explicit
        if not self.world:return 'Roboto'
        if self.language in CJK_FONTS:return str(ROOT/'assets/fonts'/CJK_FONTS[self.language])
        if any('\uac00'<=c<='\ud7af' for c in text):return str(ROOT/'assets/fonts'/CJK_FONTS['ko'])
        if any('\u3040'<=c<='\u30ff' for c in text):return str(ROOT/'assets/fonts'/CJK_FONTS['ja'])
        if any('\u0400'<=c<='\u052f' or '\u0370'<=c<='\u03ff' for c in text):return str(ROOT/'assets/fonts'/CJK_FONTS['zh'])
        if any('\u3400'<=c<='\u9fff' for c in text):return str(ROOT/'assets/fonts'/CJK_FONTS['zh'])
        return str(ROOT/'assets/fonts/Barlow-Regular.ttf')


_DEFAULT=Localizer()

def current():return _ACTIVE.get() or _DEFAULT


@contextmanager
def using(localizer):
    token=_ACTIVE.set(localizer)
    try:yield
    finally:_ACTIVE.reset(token)
