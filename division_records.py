"""Minimal completed league-season records, pooled by division across countries."""
from season_records import safe_text
FIELDS={'division','season','player','goals'}

def valid_record(r):
    return (isinstance(r,dict) and set(r)==FIELDS and type(r['division'])is int and r['division']in (1,2)
            and type(r['season'])is int and 2026<=r['season']<=2500
            and type(r['goals'])is int and 0<=r['goals']<=4000 and safe_text(r['player'],60))

def fresh(c):
    # Legacy saves contain real league scorer totals. Seed only known facts;
    # cups and international goals are not added to league divisions.
    goals={str(d):sum(l.scorer_goals.get(c.player_name,0)for l in c.leagues.values()if l.tier==d)for d in (1,2)}
    played={str(d):any(c.player_name in l.scorer_goals for l in c.leagues.values()if l.tier==d)for d in (1,2)}
    if c.club and c.matches and c.current_league.tier in (1,2):played[str(c.current_league.tier)]=True
    return dict(season=c.season,goals=goals,played=played)

def ensure(c):
    r=getattr(c,'division_stats',None)
    if not isinstance(r,dict) or r.get('season')!=c.season:
        c.division_stats=dict(season=c.season,goals={'1':0,'2':0},played={'1':False,'2':False})
    return c.division_stats

def record_match(c,goals):
    if c.current_league.tier not in (1,2):return
    state=ensure(c);key=str(c.current_league.tier);state['goals'][key]+=goals;state['played'][key]=True

def snapshots(c):
    state=ensure(c)
    return [dict(division=d,season=c.season,player=c.player_name,goals=state['goals'][str(d)])for d in (1,2)if state['played'][str(d)]] if c.world_unlocked else []

def clean(raw,c):
    try:
        if not isinstance(raw,dict) or raw['season']!=c.season:return fresh(c)
        for d in ('1','2'):
            if type(raw['goals'][d])is not int or not 0<=raw['goals'][d]<=4000 or type(raw['played'][d])is not bool:return fresh(c)
        return dict(season=c.season,goals={d:raw['goals'][d]for d in ('1','2')},played={d:raw['played'][d]for d in ('1','2')})
    except (KeyError,TypeError):return fresh(c)
