"""Explicit career category. No fabricated aggregation of best-season records."""
from season_records import FIELDS,safe_text,scope
def valid_record(r):
 return (isinstance(r,dict) and set(r)==FIELDS and r['edition'] in ('free','world') and safe_text(r['country'],64) and safe_text(r['player'],60) and safe_text(r['team'],100) and all(type(r[k])is int for k in ('division','season','matches','goals')) and 1<=r['division']<=20 and 2026<=r['season']<=2500 and 1<=r['matches']<=100000 and 0<=r['goals']<=r['matches']*20 and (r['edition']=='world' or (r['country']=='Scorer' and r['division']==1)))
def snapshot(c,world):
 if not c.club or c.development['career_matches']<1:return None
 edition,country,division=scope(c,world)
 return dict(edition=edition,country=country,division=division,season=c.season,player=c.player_name,team=c.display_club(c.club),matches=c.development['career_matches'],goals=c.development['career_goals'])
