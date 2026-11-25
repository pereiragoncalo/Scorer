"""Dated qualifying campaigns that survive a July club-season boundary."""
import copy
from datetime import date

def year_for(book,cup):
    return next((p.get('year',book.season+1)for p in book.qualification_paths if cup.key in p['qualifiers']),book.season+1)

def prepare_groups(cup,top_league):
    """Reserve six autumn rounds for Nations League A entrants (four-team groups)."""
    from world_competitions import round_robin
    small=[g for g in cup.groups if len(g)==4]
    for large in [g for g in cup.groups if len(g)>4]:
        for uid in list(large):
            if uid not in top_league:continue
            replacement=next(((g,x)for g in small for x in g if x not in top_league),None)
            if replacement:
                group,other=replacement;large[large.index(uid)]=other;group[group.index(other)]=uid
    cup.fixtures=[];cup.active=[]
    for i,group in enumerate(cup.groups):
        for r,pairs in enumerate(round_robin(group,2)):
            for a,b in pairs:cup._add(a,b,1+2*r,group=i)
    cup.last_week=max(f['week']for f in cup.fixtures)

def qualifier_dates(book,cup,fixture):
    from international_calendar import window_dates
    year=year_for(book,cup)-1
    dates=[d for s in (year-1,year)for d in window_dates(s)if d.year==year]
    dates=sorted(set(dates));group=cup.groups[fixture['group']]
    if cup.key.startswith('world_cup_q')and cup.key!='world_cup_q0':return [d for d in dates if d.month>=9]
    # Membership can be inherited in an off-year without a current NL tournament.
    a=book.tournaments.get('nations_a')
    top=set(a.teams)if a else {t['uid']for t in book.national_membership.get('nations_a',[])}
    if not top:
        from career import EUROPE_COUNTRIES
        top={t['uid']for t in sorted((t for t in book.nations.values()if t['country']in EUROPE_COUNTRIES),key=lambda t:(-t['rating'],t['uid']))[:16]}
    if len(group)==4 or cup.key.startswith('euro_q') and len(group)<4:
        if top.intersection(group):dates=[d for d in dates if d.month>=9]
        else:dates=[d for d in dates if d.month in (3,6,11)]
    return dates

def carried(book):
    from world_competitions import Tournament
    season=book.season+1;paths=[];cups={}
    for path in book.qualification_paths:
        if path.get('year',book.season+1)<=book.season+1:continue
        paths.append(copy.deepcopy(path))
        for key in path['qualifiers']:
            raw=book.tournaments[key].to_dict()
            for f in raw['fixtures']:
                if f.get('date'):f['week']=(date.fromisoformat(f['date'])-date(season,7,12)).days//7
            raw['last_week']=max(f['week']for f in raw['fixtures']);cups[key]=raw
    return dict(season=season,paths=paths,tournaments=cups)

def validate(state,season):
    from world_competitions import Tournament
    if not isinstance(state,dict)or set(state)!={'season','paths','tournaments'}or type(state['season'])is not int or state['season']!=season:raise ValueError('Invalid national campaign season')
    if not isinstance(state['paths'],list)or len(state['paths'])>8 or not isinstance(state['tournaments'],dict)or len(state['tournaments'])>16:raise ValueError('Invalid national campaigns')
    keys=[]
    for path in state['paths']:
        if not isinstance(path,dict)or path.get('key')not in ('euro','world_cup')or path.get('year')!=season+1 or path.get('created')is not False or not isinstance(path.get('qualifiers'),list):raise ValueError('Invalid national path')
        if set(path)!={'year','key','title','groups','thirds','wildcards','qualifiers','created'}or any(type(path.get(k))is not int or not 0<=path[k]<=24 for k in ('groups','thirds','wildcards'))or not 1<=path['groups']<=12 or not isinstance(path['title'],str)or not 1<=len(path['title'])<=120 or any(not isinstance(k,str)or not k.startswith(path['key']+'_q')for k in path['qualifiers']):raise ValueError('Invalid national format')
        expected=(6,4,0)if path['key']=='euro'else(12,8,2)
        if tuple(path[k]for k in ('groups','thirds','wildcards'))!=expected:raise ValueError('Unsupported national finals format')
        keys.extend(path['qualifiers'])
    if len(keys)!=len(set(keys))or set(keys)!=set(state['tournaments']):raise ValueError('Incomplete national campaign')
    for key,raw in state['tournaments'].items():
        cup=Tournament.from_dict(raw)
        if cup.key!=key or not cup.national or cup.kind!='qualifying' or not key.startswith(('euro_q','world_cup_q')):raise ValueError('Invalid carried qualifier')
        from career import WORLD_COUNTRIES
        if any(t.get('country')not in WORLD_COUNTRIES or uid!='nation:'+str(t.get('country'))for uid,t in cup.teams.items()):raise ValueError('Unknown carried nation')
        target=next(p['year']-1 for p in state['paths']if key in p['qualifiers'])
        for f in cup.fixtures:
            if f.get('date')and date.fromisoformat(f['date']).year!=target:raise ValueError('Qualifier outside campaign year')
            if f['week']<0 and f['score']is None:raise ValueError('Unplayed past qualifier')
            if not f.get('date')or (date.fromisoformat(f['date'])-date(season,7,12)).days//7!=f['week']:raise ValueError('Invalid carried fixture date')
    return copy.deepcopy(state)

def restore(book,state):
    if not state:return
    from world_competitions import Tournament
    state=validate(state,book.season)
    for path in state['paths']:
        book.qualification_paths=[p for p in book.qualification_paths if p['key']!=path['key']]+[path]
    for key,raw in state['tournaments'].items():book.tournaments[key]=Tournament.from_dict(raw)

def upgrade(c):
    """Retain played draws/results; redraft dates only for unplayed fixtures."""
    book=c.world_competitions
    if getattr(book,'calendar_version',1)>=2 or getattr(book,'calendar_upgrade_deferred',False):return
    from world_competitions import CompetitionBook
    from international_calendar import schedule_book
    trial=copy.deepcopy(book);fresh=CompetitionBook(book.season,book.seed,c.leagues,book.national_membership)
    trial.calendar_version=2
    for path in trial.qualification_paths:path.setdefault('year',book.season+1)
    for path in fresh.qualification_paths:
        if any(p['key']==path['key']for p in trial.qualification_paths):continue
        trial.qualification_paths.append(copy.deepcopy(path))
        for key in path['qualifiers']:trial.tournaments[key]=copy.deepcopy(fresh.tournaments[key])
    for cup in trial.tournaments.values():
        if cup.national:
            for f in cup.fixtures:
                if f['score']is None:f.pop('date',None)
    try:schedule_book(trial)
    except ValueError:
        # An oversized, already-started legacy qualifying draw cannot be shortened
        # or replayed. Finish that saved campaign; the next season uses the new model.
        book.calendar_upgrade_deferred=True;return
    for key,cup in trial.tournaments.items():
        if key not in book.tournaments and cup.national:cup.advance(max(0,c.week-1),until=c.current_date.isoformat())
    c.world_competitions=trial
