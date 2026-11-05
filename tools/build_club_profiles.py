"""Build offline club facts from cached, revision-pinned public wiki source.

Build dependency: mwparserfromhell. Never required by the game. Missing or
ambiguous factual values remain null; stadium modelling is a separate runtime step.
"""
import argparse,html,json,re
from pathlib import Path
import mwparserfromhell as mw

SKIP=re.compile(r'runner|second.place|reserve|youth|junior|women|double|treble|individual|friendly|unofficial|others?|play.off|promot|semi.final|quarter.final|finalists|third.place|vice|subcampe|finalista|promotion|aufstieg|jugend|femin|femmin|fémin|dauphin|under.?\d',re.I)

def clean(value):
    code=mw.parse(str(value))
    for link in list(code.filter_wikilinks()):
        if str(link.title).strip().lower().startswith(('file:','image:','category:')):
            try:code.remove(link)
            except ValueError:pass
    for tag in list(code.filter_tags()):
        if str(tag.tag).lower() in ('ref','sup','small'):
            try:code.remove(tag)
            except ValueError:pass
    for template in list(code.filter_templates()):
        name=str(template.name).strip().lower()
        if name in ('lang','langx','nowrap','nobr','small') and template.params:
            values=[p for p in template.params if not p.showkey]
            replacement=str(values[-1].value) if values else ''
        elif name in ('interlanguage link','ill'):
            replacement=str(template.get('lt').value) if template.has('lt') else str(template.get('1').value) if template.has('1') else ''
        elif name in ('ubl','hlist','plainlist','unbulleted list','bulleted list'):
            replacement=' '.join(str(p.value) for p in template.params if not p.showkey)
        elif name in ('formatnum','val','nts','formatnum:') and template.params:replacement=str(template.params[0].value)
        elif name.startswith('formatnum:'):replacement=str(template.name).split(':',1)[1]
        elif name in ('start date','start date and age','start-date and age','birth date and age','foundation date'):
            replacement=' '.join(str(p.value) for p in template.params if not p.showkey)
        else:replacement=''
        try:code.replace(template,replacement)
        except ValueError:pass
    return re.sub(r'\s+',' ',html.unescape(code.strip_code())).strip(' \n:*;')

def infobox(text):
    for template in mw.parse(text).filter_templates(recursive=False):
        if str(template.name).strip().lower() in ('infobox football club','football club infobox','ficha de equipo de fútbol'):
            return {str(p.name).strip().lower():str(p.value).strip() for p in template.params}
    return {}

def capacity(value):
    raw=clean(value)
    # First stated capacity, accepting thousands separators without reading dates
    # in refs or a later construction/expansion note as a stadium size.
    match=re.search(r'(?<!\d)(\d{1,3}(?:[,.\s]\d{3})+|\d{3,6})(?!\d)',raw)
    if not match:return None
    result=int(re.sub(r'\D','',match.group(1)))
    return result if 250<=result<=150000 else None

def honours(text):
    start=re.search(r'^==\s*(?:Honours|Honors|Palmarés|Palmarès|Títulos|Conquistas|Erfolge|Titles)(?: and [^=\n]+)?\s*==\s*$',text,re.I|re.M)
    sections=[]
    if start:
        remaining=text[start.end():];end=re.search(r'^==[^=].*?==\s*$',remaining,re.M)
        raw=remaining[:end.start()] if end else remaining
        kept=[];skip_depth=None
        for line in raw.splitlines():
            heading=re.match(r'^(=+)\s*(.*?)\s*\1\s*$',line)
            if heading:
                depth=len(heading.group(1))
                if skip_depth is not None and depth<=skip_depth:skip_depth=None
                if skip_depth is None and SKIP.search(clean(heading.group(2))):skip_depth=depth
            if skip_depth is None:kept.append(line)
        sections=[mw.parse('\n'.join(kept))]
    result=[]
    def add(title,count):
        title=clean(title);title=re.sub(r'\s*\(\d+\)\s*$','',title).strip(' :;–-')
        if not title or title.casefold() in ('winners','champions','runners-up','titles') or len(title)>160 or SKIP.search(title) or not 0<count<1000:return
        row=dict(title=title,count=count)
        if row not in result:result.append(row)
    for section in sections[:1]:
        # Wiki table cells, not a digit regex over arbitrary prose/season dates.
        for table in section.filter_tags(recursive=False):
            if str(table.tag)!='table':continue
            for tr in table.contents.filter_tags(recursive=False):
                if str(tr.tag)!='tr':continue
                cells=[cell for cell in tr.contents.filter_tags(recursive=False) if str(cell.tag) in ('th','td')]
                for index,cell in enumerate(cells[:-1]):
                    if not cell.contents.filter_wikilinks():continue
                    title=clean(cell.contents);number=clean(cells[index+1].contents)
                    m=re.fullmatch(r'(\d{1,3})(?:\s*\([^)]*\))?',number)
                    if m:add(title,int(m.group(1)));break
                    position=re.match(r'^(?:Champions?|Winners?)\s*:',number,re.I)
                    if position:
                        years=re.findall(r'(?<!\d)(?:18|19|20)\d{2}(?:[–—-](?:\d{4}|\d{2}))?(?!\d)',number[position.end():])
                        if years:add(title,len(years));break
                    if re.fullmatch(r'(?:Champions?|Winners?)',number,re.I) and index+2<len(cells):
                        years=re.findall(r'(?<!\d)(?:18|19|20)\d{2}(?:[–—-](?:\d{4}|\d{2}))?(?!\d)',clean(cells[index+2].contents))
                        if years:add(title,len(years));break
        current='';skip=False
        for line in str(section).splitlines():
            heading=re.match(r'^=+\s*(.*?)\s*=+\s*$',line)
            if heading:skip=bool(SKIP.search(clean(heading.group(1))));current='';continue
            if skip or not line.strip() or line.lstrip().startswith(('|','!','{','}')):continue
            plain=clean(line)
            if re.search(r'\b(?:winners?|champions?)\b',plain,re.I) and ';' in plain:plain=plain.split(';',1)[0]
            if SKIP.search(plain):current='';continue
            match=re.search(r'\b(?:Winners?|Champions?|Campeón|Campeones)\b\s*:?\s*\((\d{1,3})\)',plain,re.I)
            if match:
                title=plain[:match.start()].strip(' :;*') or current
                if title:add(title,int(match.group(1)))
                continue
            winners=re.match(r'^(?:Winners?|Champions?|Campeón|Campeones)\s*:?\s*(?=(?:18|19|20)\d{2})',plain,re.I)
            if winners and current:
                years=re.findall(r'(?<!\d)(?:18|19|20)\d{2}(?:[–—-](?:\d{4}|\d{2}))?(?!\d)',plain[winners.end():])
                if years:add(current,len(years))
                continue
            named=re.match(r'(.+?):\s*(\d{1,3})(?:\s*[–—(].*)?$',plain)
            if named:add(named.group(1),int(named.group(2)));current=named.group(1);continue
            inline=re.match(r'(.+?)\s*\((\d{1,3})\)\s*:',plain)
            if inline:add(inline.group(1),int(inline.group(2)));current=inline.group(1);continue
            named_winners=re.match(r'(.+?)\s*:?\s*\b(?:winners?|champions?)\b\s*[, :]\s*((?:18|19|20)\d{2}.*)',plain,re.I)
            if named_winners:
                years=re.findall(r'(?<!\d)(?:18|19|20)\d{2}(?:[–—-](?:\d{4}|\d{2}))?(?!\d)',named_winners.group(2))
                if years:add(named_winners.group(1),len(years))
                continue
            dates=re.findall(r'(?<!\d)(?:18|19|20)\d{2}(?:[–—-](?:\d{4}|\d{2}))?(?!\d)',plain)
            colon_years=re.match(r'(.+?):\s*(?=(?:18|19|20)\d{2})',plain)
            if colon_years and dates:add(colon_years.group(1),len(dates));continue
            if current and dates and re.match(r'^(?:18|19|20)\d{2}',plain):add(current,len(dates));continue
            leading=re.match(r'^(\d{1,3})\s*(?:[–—-].*?)?:',plain)
            if leading and current:add(current,int(leading.group(1)));continue
            if not re.search(r'\b\d{4}\b',plain) and ':' not in plain.rstrip(':') and any(c.isalpha() for c in plain) and (line.startswith('*') or mw.parse(line).filter_wikilinks()):current=plain.rstrip(':')
    # Never resolve contradictory totals by guessing. Keep the UI explicit about
    # unavailable records instead of calling a runner-up position a trophy.
    counts={}
    for row in result:counts.setdefault(row['title'],set()).add(row['count'])
    return [r for r in result if len(counts[r['title']])==1]

def build(cache,overrides=None):
    rows={}
    for uid,record in cache.items():
        if 'text' not in record:continue
        text=record['text'];fields=infobox(text)
        foundation=fields.get('founded',fields.get('fundación',''))
        foundation=re.sub(r'<ref\b[^>]*>.*?</ref>|<ref\b[^>]*/>','',foundation,flags=re.S|re.I)
        year=re.search(r'\b(?:18|19|20)\d{2}\b',foundation)
        ground=fields.get('stadium') or fields.get('ground') or fields.get('estadio','')
        links=mw.parse(ground).filter_wikilinks()
        stadium=clean(links[0].text or links[0].title) if links else clean(ground).split('<br')[0].strip()
        rows[uid]=dict(club=record['club'],country=record['country'],founded=int(year.group()) if year else None,stadium=stadium or None,capacity=capacity(fields.get('capacity',fields.get('capacidad',''))),honours=honours(text),supporters=None,source=record['source'],revision=record['revision'])
    if overrides is None:
        path=Path(__file__).resolve().parents[1]/'docs/data/club_profile_overrides.json'
        overrides=json.loads(path.read_text(encoding='utf8')) if path.exists() else {}
    for uid,values in overrides.items():
        if uid in rows:rows[uid].update(values)
    return dict(version=1,review_date='2026-11-05',clubs=rows)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache',type=Path);p.add_argument('--output',type=Path,default=Path('assets/data/club_profiles.json'));args=p.parse_args()
    data=build(json.loads(args.cache.read_text()));args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Profiles',len(data['clubs']),'missing foundation/stadium/capacity/honours',*[sum(not r[k] for r in data['clubs'].values()) for k in ('founded','stadium','capacity','honours')])
