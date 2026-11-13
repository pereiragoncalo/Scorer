"""Frozen season-end facts. Optional save extension; never simulates fixtures."""
import copy,json,re
from datetime import date

def capture(c):
    if getattr(c,'season_review',None) and c.season_review['season']==c.season:return
    club=c.club
    if club is None:return
    league=c.current_league;table=league.table()
    position=next((i+1 for i,t in enumerate(table) if t.uid==club.uid),len(table))
    scorers=league.scorer_goals;goals=scorers.get(c.player_name,0)
    def rank(n):return 1+sum(v>n for v in scorers.values())
    leaders=[dict(name=c.display_scorer(name),goals=n,rank=rank(n)) for name,n in sorted(scorers.items(),key=lambda r:(-r[1],r[0])) if n>0][:5]
    matches=[];start=date(c.season,7,12).isoformat();end=date(c.season+1,7,12).isoformat()
    for f in c.fixture_history:
        if not f.get('played') or f.get('club_match') is False:continue
        if f.get('season',c.season if start<=f.get('date','')<end else -1)!=c.season:continue
        team=f.get('player_club',club.name)
        if team not in (f.get('home'),f.get('away')):continue
        score=re.match(r'^(\d+)-(\d+)',f.get('status',''))
        if not score:continue
        home,away=map(int,score.groups());own,other=(home,away) if f['home']==team else (away,home)
        matches.append(dict(home=c.display_text(f['home']),away=c.display_text(f['away']),score=f['status'],competition=f['competition'],date=f['date'],difference=own-other,goals=own))
    key=lambda f:(f['difference'],f['goals'])
    from coach import appearance_for
    d=c._ensure_development()
    from division_records import snapshots
    public_records=snapshots(c)
    c.season_review=dict(version=1,season=c.season,pending=True,club=c.display_club(club),player=c.player_name,
        league=c.display_league(league),position=position,teams=len(table),points=club.points,
        matches=c.matches,goals=c.goals,best=max(matches,key=key) if matches else None,worst=min(matches,key=key) if matches else None,
        leaders=leaders,player_goals=goals,player_rank=rank(goals) if goals else None,
        portrait=appearance_for(club.uid,c.coach_appearance)['portrait'],target=d['goal_target'],target_met=c.goals>=d['goal_target'],
        share_choice='unasked',public_records=public_records,assessment='strong' if position<=3 else 'poor' if position>len(table)*.75 else 'mixed',next_goal_target=None)

def finalize(c):
    report=getattr(c,'season_review',None)
    if report and report['season']<c.season:
        report['next_goal_target']=c._ensure_development()['goal_target'] if c.club and not c.free_agent else None

def clean(raw):
    try:
        if not isinstance(raw,dict) or raw.get('version')!=1 or len(json.dumps(raw,allow_nan=False))>40000:return None
        for key in ('season','position','teams','matches','goals','player_goals','target'):
            if type(raw[key])is not int or not 0<=raw[key]<=100000:return None
        if type(raw['points'])is not int or not -100000<=raw['points']<=100000:return None
        if type(raw['target_met'])is not bool:return None
        if type(raw['pending'])is not bool or raw['assessment']not in ('strong','poor','mixed'):return None
        if type(raw['portrait'])is not int or not 0<=raw['portrait']<10:return None
        for key in ('player_rank','next_goal_target'):
            if raw[key]is not None and (type(raw[key])is not int or not 1<=raw[key]<=100000):return None
        for key in ('club','player','league'):
            if not isinstance(raw[key],str) or len(raw[key])>200 or not raw[key].isprintable():return None
        for key in ('best','worst'):
            item=raw[key]
            if item is not None:
                for field in ('home','away','score','competition','date'):
                    if not isinstance(item[field],str) or len(item[field])>200 or not item[field].isprintable():return None
        if not isinstance(raw['leaders'],list) or len(raw['leaders'])>5:return None
        for item in raw['leaders']:
            if not isinstance(item['name'],str) or len(item['name'])>200 or not item['name'].isprintable():return None
            if any(type(item[k])is not int or not 1<=item[k]<=100000 for k in ('rank','goals')):return None
        from division_records import valid_record
        if raw.get('share_choice','unasked')not in ('unasked','declined','queued'):return None
        if not isinstance(raw.get('public_records',[]),list) or len(raw.get('public_records',[]))>2 or any(not valid_record(r)for r in raw.get('public_records',[])):return None
        result=copy.deepcopy(raw);result.setdefault('share_choice','unasked');result.setdefault('public_records',[]);return result
    except (ValueError,KeyError,TypeError,OverflowError):return None

def visible(game):
    c=game.career;r=getattr(c,'season_review',None)
    from title_events import pending
    return bool(r and r['pending'] and not c.post_match_stage and not pending(c) and game.view in ('hub','coach','private_coach','agent','training'))

def dismiss(c):
    report=getattr(c,'season_review',None)
    if not report or not report['pending']:return False
    report['pending']=False
    if c.save() is False:report['pending']=True;return False
    return True
