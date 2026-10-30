"""Casual self-reported leaderboard; never trusted for prizes or payments."""
import hashlib
import re
from datetime import datetime,timezone


def valid_entry(data):
    return (isinstance(data,dict) and set(data)=={'token','alias','edition','season','matches','goals'}
        and isinstance(data['token'],str) and re.fullmatch(r'[0-9a-f]{64}',data['token']) is not None
        and isinstance(data['alias'],str) and re.fullmatch(r'[A-Za-z0-9 _-]{3,20}',data['alias']) is not None
        and data['edition'] in ('free','world')
        and all(type(data[k]) is int for k in ('season','matches','goals'))
        and 2026<=data['season']<=2200 and 1<=data['matches']<=100
        and 0<=data['goals']<=data['matches']*10)


def initialize(db):
    db.execute('CREATE TABLE IF NOT EXISTS leaderboard (id TEXT, edition TEXT, season INTEGER, alias TEXT, matches INTEGER, goals INTEGER, updated TEXT, PRIMARY KEY(id,edition,season))')


def submit(db,data):
    if not valid_entry(data):raise ValueError('invalid entry')
    identity=hashlib.sha256(data['token'].encode()).hexdigest()
    old=db.execute('SELECT matches,goals FROM leaderboard WHERE id=? AND edition=? AND season=?',(identity,data['edition'],data['season'])).fetchone()
    if old and (data['matches']<old[0] or data['goals']<old[1] or data['goals']-old[1]>(data['matches']-old[0])*10):raise ValueError('inconsistent progress')
    db.execute('INSERT INTO leaderboard VALUES(?,?,?,?,?,?,?) ON CONFLICT(id,edition,season) DO UPDATE SET alias=excluded.alias,matches=excluded.matches,goals=excluded.goals,updated=excluded.updated',(identity,data['edition'],data['season'],data['alias'],data['matches'],data['goals'],datetime.now(timezone.utc).date().isoformat()))
    db.execute('DELETE FROM leaderboard WHERE updated < date(?,"-90 days")',(datetime.now(timezone.utc).date().isoformat(),))


def leaders(db):
    rows=db.execute('SELECT edition,season,alias,matches,goals FROM leaderboard ORDER BY goals DESC,matches ASC,alias ASC LIMIT 100').fetchall()
    return {'verified':False,'entries':[dict(zip(('edition','season','alias','matches','goals'),r)) for r in rows]}


def withdraw(db,token):
    if not isinstance(token,str) or re.fullmatch(r'[0-9a-f]{64}',token) is None:raise ValueError('invalid token')
    db.execute('DELETE FROM leaderboard WHERE id=?',(hashlib.sha256(token.encode()).hexdigest(),))
