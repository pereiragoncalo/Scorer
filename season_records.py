"""Completed personal-season snapshots, captured before promotion and reset."""
import unicodedata

FIELDS={'edition','country','division','season','player','team','matches','goals'}

def safe_text(value,maximum):
    return (isinstance(value,str) and 1<=len(value.strip())<=maximum
            and all(unicodedata.category(c)[0]!='C' and c not in '<>' for c in value))

def valid_record(record):
    return (isinstance(record,dict) and set(record)==FIELDS
        and record['edition'] in ('free','world')
        and safe_text(record['country'],64) and safe_text(record['player'],60) and safe_text(record['team'],100)
        and all(type(record[k]) is int for k in ('division','season','matches','goals'))
        and 1<=record['division']<=20 and 2026<=record['season']<=2500
        and 1<=record['matches']<=200 and 0<=record['goals']<=record['matches']*20
        and (record['edition']=='world' or (record['country']=='Scorer' and record['division']==1)))

def scope(career,world):
    return ('world',career.current_league.country,career.current_league.tier) if world else ('free','Scorer',1)

def completed_snapshot(career):
    if career.matches<1 or career.club is None:return {}
    edition,country,division=scope(career,career.world_unlocked)
    return dict(edition=edition,country=country,division=division,season=career.season,
                player=career.player_name,team=career.display_club(career.club),
                matches=career.matches,goals=career.goals)

def keep_best(existing,record):
    records=[dict(r) for r in existing if valid_record(r)] if isinstance(existing,list) else []
    if not valid_record(record):return records
    key=lambda r:(r['edition'],r['country'],r['division'])
    old=next((r for r in records if key(r)==key(record)),None)
    if old is None or record['goals']>old['goals']:
        records=[r for r in records if key(r)!=key(record)]+[dict(record)]
    return records[-256:]
