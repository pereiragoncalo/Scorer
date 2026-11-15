"""Dated club rounds with international release breaks and bounded midweek capacity."""
from datetime import date,timedelta
from functools import lru_cache

@lru_cache(maxsize=65536)
def blocked(day,season,country=None):
    from international_calendar import window_spans,finals_dates,NATIONAL_TOURNAMENTS
    if any(a<=day<=b for a,b in window_spans(season-1)+window_spans(season)+window_spans(season+1)):return True
    if country:
        from career import EUROPE_COUNTRIES,AFRICA_COUNTRIES,ASIA_COUNTRIES,NORTH_AMERICA_COUNTRIES,SOUTH_AMERICA_COUNTRIES,OCEANIA_COUNTRIES
        regions={'euro':EUROPE_COUNTRIES,'afcon':AFRICA_COUNTRIES,'asian':ASIA_COUNTRIES,'gold':NORTH_AMERICA_COUNTRIES,'copa':SOUTH_AMERICA_COUNTRIES+NORTH_AMERICA_COUNTRIES,'ofc_nations':OCEANIA_COUNTRIES}
        for year in (season,season+1):
            for key,_,period,offset in NATIONAL_TOURNAMENTS:
                if year%period!=offset or key!='world_cup'and country not in regions[key]:continue
                days=finals_dates(year-1,key)
                if days[0]<=day<=days[-1]:return True
    return False

@lru_cache(maxsize=256)
def remaining_dates(season,count,start,country):
    start=max(start,date(season,8,1));end=date(season+1,5,15)
    if start>end:end=date(season+1,7,10)
    days=[start+timedelta(days=i)for i in range((end-start).days+1)]
    weekend=[d for d in days if d.weekday()==5 and not blocked(d,season,country)]
    if count<=len(weekend):
        return tuple(weekend[round(i*(len(weekend)-1)/max(1,count-1))]for i in range(count))
    midweek=[d for d in days if d.weekday()==2 and not blocked(d,season,country)]
    extra=count-len(weekend)
    if extra>len(midweek):raise ValueError('Remaining club rounds exceed available release-safe dates')
    return tuple(sorted(weekend+[midweek[round(i*(len(midweek)-1)/max(1,extra-1))]for i in range(extra)]))

def ensure(c):
    book=c.world_competitions
    if getattr(book,'calendar_version',1)<2:return
    if not hasattr(book,'league_dates'):book.league_dates={}
    league=c.current_league
    current=book.league_dates.get(league.key)
    if current and(league.round_index>=len(current)or current[league.round_index]and date.fromisoformat(current[league.round_index])>=c.current_date):
        refresh_cups(c,current);return
    played=league.round_index;total=league.total_rounds
    history=[date.fromisoformat(e['date'])for e in c.fixture_history if e.get('season',c.season)==c.season and e.get('played')and e.get('competition')==league.name]
    start=max(c.current_date,max(history)+timedelta(days=3)if history else c.current_date)
    dates=remaining_dates(c.season,max(0,total-played),start,league.country)
    # Historical entries themselves are immutable. Prefix is never displayed/replayed.
    prefix=[None]*played
    book.league_dates[league.key]=prefix+[d.isoformat()for d in dates]
    refresh_cups(c,book.league_dates[league.key])

def refresh_cups(c,dates):
    if not c.club:return
    days=[date.fromisoformat(d)for d in dates if d]
    changed=False
    for cup in c.world_competitions.tournaments.values():
        if cup.national:continue
        for f in cup.fixtures:
            if f['score']is None and f.get('date')and c.club.uid in (f['home'],f['away']):
                day=date.fromisoformat(f['date'])
                if any(abs((day-d).days)<2 for d in days):f.pop('date');changed=True
    if changed:c.world_competitions._club_scheduled_count=-1

def league_date(c,index=None):
    book=c.world_competitions
    dates=getattr(book,'league_dates',{}).get(c.current_league.key)
    index=c.current_league.round_index if index is None else index
    return date.fromisoformat(dates[index])if dates and index<len(dates)and dates[index]else None

def validate(calendars,season):
    if not isinstance(calendars,dict)or len(calendars)>256:raise ValueError('Invalid club calendars')
    for key,days in calendars.items():
        if not isinstance(key,str)or len(key)>100 or not isinstance(days,list)or len(days)>128:raise ValueError('Invalid club calendar')
        known=[d for d in days if d is not None]
        if days!=[None]*(len(days)-len(known))+known:raise ValueError('Unknown dates must precede scheduled rounds')
        if any(not isinstance(d,str)or not date(season,7,1)<=date.fromisoformat(d)<=date(season+1,7,31)for d in known):raise ValueError('Invalid club fixture date')
        if known!=sorted(set(known)):raise ValueError('Club calendar not chronological')

def schedule(book):
    if getattr(book,'calendar_version',1)<2:return
    count=sum(len(c.fixtures)for c in book.tournaments.values()if not c.national)
    if getattr(book,'_club_scheduled_count',-1)==count:return
    from world_competitions import fixture_day
    occupied={};pending=[]
    for cup in book.tournaments.values():
        if cup.national:continue
        for f in cup.fixtures:
            if f.get('date'):
                for uid in (f['home'],f['away']):occupied.setdefault(uid,set()).add(date.fromisoformat(f['date']))
            elif f['score']is None:pending.append((f['week'],cup.key,f['id'],cup,f))
    for _,_,_,cup,f in sorted(pending,key=lambda p:p[:3]):
        day=date(book.season,7,12)+timedelta(weeks=f['week'],days=fixture_day(cup))
        if cup.kind=='promotion':
            previous=[date.fromisoformat(p['date'])for p in cup.fixtures if p.get('date')and set((p['home'],p['away']))&set((f['home'],f['away']))]
            if previous:day=max(previous)+timedelta(days=3)
        for _ in range(400):
            free=True
            for uid in (f['home'],f['away']):
                team=cup.teams[uid];days=getattr(book,'league_dates',{}).get(team['country']+'|'+str(team.get('tier',1)),[])
                if blocked(day,book.season,team['country'])or any(abs((day-p).days)<2 for p in occupied.get(uid,()))or any(abs((day-date.fromisoformat(p)).days)<2 for p in days if p):free=False;break
            if free:break
            day+=timedelta(days=1)
        else:raise ValueError('No release-safe club fixture slot')
        f['date']=day.isoformat();f['week']=(day-date(book.season,7,12)).days//7
        for uid in (f['home'],f['away']):occupied.setdefault(uid,set()).add(day)
    for cup in book.tournaments.values():
        if not cup.national:cup.last_week=max((f['week']for f in cup.fixtures),default=cup.last_week)
    book._club_scheduled_count=count

def set_week(c,week):
    previous=c.week
    held=c.coach_meeting_held
    reserved=c.training_session_week==previous
    last=c.fixture_history[-1]if c.fixture_history else None
    completed=bool(last and last.get('season',c.season)==c.season and last.get('played')and(date.fromisoformat(last['date'])-date(c.season,7,12)).days//7==previous)
    c.week=week
    if previous!=week:
        if held and(reserved or not completed):c.coach_state['meeting']['key']=c.coach_key
        # Retiming the next appearance must not discard its already-reserved practice.
        for field in ('last_training_week','training_session_week'):
            if getattr(c,field,-1)==previous:setattr(c,field,week)

def upcoming_date(c,fixture):
    if fixture and fixture[0].startswith('world|'):
        from international_calendar import match_date
        _,key,uid=fixture[0].split('|',2);book=c.world_competitions
        cup=book.tournaments.get(key)
        row=next((f for f in cup.fixtures if f['id']==uid),None)if cup else book.friendlies.get(uid)
        if row:return match_date(c.season,cup,row)
    return league_date(c)or c.current_date+timedelta(days=4 if c.world_unlocked else 0)
