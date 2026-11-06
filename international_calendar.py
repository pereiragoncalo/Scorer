"""Persistent international windows and dated national fixtures for a game season.

Opponent draws and qualification formats are the game's models. Window dates
are separate from eligibility: a window call-up is locked once it begins.
"""
from datetime import date,timedelta
from functools import lru_cache

FINALS={'world_cup','euro','afcon','asian','gold','copa','ofc_nations'}

NATIONAL_TOURNAMENTS=(
    ('world_cup','FIFA World Cup',4,2),
    ('euro','European Championship',4,0),
    ('copa','Copa America',4,0),
    ('afcon','Africa Cup of Nations',2,1),
    ('asian','AFC Asian Cup',4,3),
    ('gold','Concacaf Gold Cup',2,1),
    ('ofc_nations','OFC Nations Cup',4,0),
)

def national_tournament_calendar(season):
    result=[]
    for key,title,period,offset in NATIONAL_TOURNAMENTS:
        year=season+1
        year+=(offset-year)%period
        result.append((key,title,year))
    return result

@lru_cache(maxsize=1)
def calendar_source():
    from pathlib import Path
    import json
    return json.loads((Path(__file__).resolve().parent/'assets/data/international_calendar.json').read_text())

def window_dates(season):
    source=calendar_source()['windows'];spans=[]
    for year in (season,season+1):
        if str(year) in source:
            spans += [(date.fromisoformat(a),date.fromisoformat(b)) for a,b in source[str(year)] if (year==season and date.fromisoformat(a).month>=8) or (year==season+1 and date.fromisoformat(a).month<8)]
        else:
            # Post-2030 careers remain playable; dates are explicitly projections.
            for month,day,length in ([(9,21,15),(11,9,8)] if year==season else [(3,22,8),(6,7,8)]):
                a=date(year,month,day);a-=timedelta(days=a.weekday());spans.append((a,a+timedelta(days=length)))
    return [a+timedelta(days=n) for a,b in spans for n in range((b-a).days+1) if (a+timedelta(days=n)).weekday() in (1,4)]

def finals_dates(season,key):
    year=season+1;span=calendar_source()['finals'].get(str(year),{}).get(key)
    if span:
        a,b=map(date.fromisoformat,span)
        dates=[a+timedelta(days=n) for n in range(0,(b-a).days+1,4)]
        if dates[-1]!=b:dates.append(b)
        return dates
    return [date(year,6,3)+timedelta(days=4*i) for i in range(12)]

def match_date(season,cup,f):
    return date.fromisoformat(f['date']) if f.get('date') else date(season,7,12)+timedelta(weeks=f['week'],days=3 if cup and cup.key.startswith('nations_') else 2 if cup is None or cup.national else 0 if cup.key.startswith('domestic:') else 1)

def window_key(season,day):
    if day.month in (9,10):return str(season)+':autumn'
    if day.month==11:return str(season)+':november'
    if day.month==3:return str(season)+':march'
    if day.month in (1,2):return str(season)+':winter-finals'
    return str(season)+':summer'

def schedule_book(book):
    occupied={}
    for cup in book.tournaments.values():
        if not cup.national:continue
        for f in cup.fixtures:
            if not f.get('date'):continue
            d=date.fromisoformat(f['date'])
            for uid in (f['home'],f['away']):occupied[uid,d]=f['id']
    pending=[]
    for cup in book.tournaments.values():
        if not cup.national:continue
        for f in cup.fixtures:
            if f.get('date') or f['score'] is not None:continue
            pending.append((f['week'],cup.key,f['id'],cup,f))
    for _,_,_,cup,f in sorted(pending,key=lambda item:item[:3]):
        finals=cup.key in FINALS or (cup.key.startswith('nations_') and f['stage']!='League phase')
        slots=finals_dates(book.season,cup.key) if finals else window_dates(book.season)
        previous=[date.fromisoformat(p['date']) for p in cup.fixtures if p.get('date') and p['group']==f['group'] and (p['home'] in (f['home'],f['away']) or p['away'] in (f['home'],f['away']))]
        floor=max(previous,default=date(book.season,7,12))
        available=[d for d in slots if d>floor and all((uid,d) not in occupied for uid in (f['home'],f['away']))]
        if not available:raise ValueError('National calendar exceeds available match dates')
        d=available[0];f['date']=d.isoformat();f['week']=(d-date(book.season,7,12)).days//7
        for uid in (f['home'],f['away']):occupied[uid,d]=f['id']
    for cup in book.tournaments.values():
        if cup.national:cup.last_week=max((f['week'] for f in cup.fixtures),default=cup.last_week)


def prepare_friendlies(book,nationality):
    from world_competitions import rng_for
    actor='nation:'+nationality
    if actor not in book.nations:return
    competitive={(uid,f['date']) for cup in book.tournaments.values() if cup.national for f in cup.fixtures if f.get('date') for uid in (f['home'],f['away'])}
    for key,f in list(book.friendlies.items()):
        if f.get('date') and f['score'] is None and (actor,f['date']) in competitive and actor in (f['home'],f['away']):del book.friendlies[key]
    for d in window_dates(book.season):
        if (actor,d.isoformat()) in competitive:continue
        key='friendly:'+nationality+':'+d.isoformat()
        if key in book.friendlies:continue
        opponents=[uid for uid in book.nations if uid!=actor and (uid,d.isoformat()) not in competitive]
        if not opponents:continue
        opponent=rng_for(book.seed,book.season,key).choice(sorted(opponents));home,away=(actor,opponent) if d.day%2 else (opponent,actor)
        book.friendlies[key]=dict(id=key,home=home,away=away,week=(d-date(book.season,7,12)).days//7,date=d.isoformat(),stage='International friendly',score=None)


def selected(book,nationality,day,eligible,current_week):
    key=nationality+':'+window_key(book.season,day)
    if key not in book.callups:
        if (day-date(book.season,7,12)).days//7>current_week:return False
        book.callups[key]=bool(eligible)
    return book.callups[key]


def selection_label(book,nationality,day):
    decision=book.callups.get(nationality+':'+window_key(book.season,day))
    return 'Selection pending' if decision is None else 'Called up' if decision else 'Not selected'
