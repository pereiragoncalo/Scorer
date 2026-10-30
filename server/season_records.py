"""Separate v2 completed-season boards; old live v1 scores are never promoted."""
import hashlib
from season_records import valid_record
from server.leaderboard import withdraw as withdraw_legacy

def initialize(db):
    db.execute('CREATE TABLE IF NOT EXISTS season_records(id TEXT,edition TEXT,country TEXT,division INTEGER,season INTEGER,player TEXT,team TEXT,matches INTEGER,goals INTEGER,PRIMARY KEY(id,edition,country,division))')

def identity(token):
    import re
    if not isinstance(token,str) or not re.fullmatch('[0-9a-f]{64}',token):raise ValueError('invalid token')
    return hashlib.sha256(token.encode()).hexdigest()

def submit(db,payload):
    if not isinstance(payload,dict) or set(payload)!={'token','record'} or not valid_record(payload['record']):raise ValueError('invalid record')
    key=identity(payload['token']);r=payload['record']
    old=db.execute('SELECT goals FROM season_records WHERE id=? AND edition=? AND country=? AND division=?',(key,r['edition'],r['country'],r['division'])).fetchone()
    if old is None or r['goals']>old[0]:
        db.execute('INSERT INTO season_records VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(id,edition,country,division) DO UPDATE SET season=excluded.season,player=excluded.player,team=excluded.team,matches=excluded.matches,goals=excluded.goals',(key,r['edition'],r['country'],r['division'],r['season'],r['player'],r['team'],r['matches'],r['goals']))

def leaders(db,edition,country,division):
    if edition not in ('free','world') or not isinstance(country,str) or not 1<=len(country)<=64 or not 1<=division<=20:raise ValueError('invalid filter')
    columns=('edition','country','division','season','player','team','matches','goals')
    rows=db.execute('SELECT edition,country,division,season,player,team,matches,goals FROM season_records WHERE edition=? AND country=? AND division=? ORDER BY goals DESC,season ASC,player ASC LIMIT 100',(edition,country,division)).fetchall()
    return dict(schema=2,verified=False,entries=[dict(zip(columns,r)) for r in rows])

def withdraw(db,token):
    db.execute('DELETE FROM season_records WHERE id=?',(identity(token),));withdraw_legacy(db,token)
