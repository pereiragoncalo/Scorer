"""Explicitly submitted completed seasons, pooled across countries by division."""
import hashlib
from datetime import datetime,timezone
from division_records import valid_record
from server.season_records import identity

def initialize(db):
    db.execute('''CREATE TABLE IF NOT EXISTS division_records(owner TEXT,division INTEGER,season INTEGER,player TEXT,goals INTEGER,state TEXT NOT NULL,consent INTEGER NOT NULL,updated TEXT NOT NULL,PRIMARY KEY(owner,division,season))''')
    # Existing explicit season choices become visible; rejected records stay removed.
    db.execute("UPDATE division_records SET state='approved' WHERE state='pending' AND consent=1")

def submit(db,payload):
    if not isinstance(payload,dict) or set(payload)!={'token','record','consent_version'} or type(payload['consent_version'])is not int or payload['consent_version']!=1 or not valid_record(payload['record']):raise ValueError('Invalid season consent')
    from server.moderation import public_id
    owner=identity(payload['token']);r=payload['record'];publisher=public_id(owner)
    if db.execute('SELECT 1 FROM banned_publishers WHERE publisher=?',(publisher,)).fetchone():raise PermissionError('Suspended')
    old=db.execute('SELECT player,goals,state FROM division_records WHERE owner=? AND division=? AND season=?',(owner,r['division'],r['season'])).fetchone()
    if old and old[:2]==(r['player'],r['goals']):
        if old[2]=='rejected':raise PermissionError('Record removed')
        return
    db.execute("INSERT INTO division_records VALUES(?,?,?,?,?,'approved',1,?) ON CONFLICT(owner,division,season) DO UPDATE SET player=excluded.player,goals=excluded.goals,state='approved',consent=1,updated=excluded.updated",(owner,r['division'],r['season'],r['player'],r['goals'],datetime.now(timezone.utc).isoformat()))

def leaders(db,division):
    if type(division)is not int or division not in (1,2):raise ValueError('Invalid division')
    from server.moderation import public_id
    rows=db.execute("SELECT owner,player,goals,season FROM division_records WHERE division=? AND state='approved' AND consent=1 ORDER BY goals DESC,season ASC,player ASC",(division,)).fetchall()
    seen=set();entries=[]
    for owner,player,goals,season in rows:
        publisher=public_id(owner)
        if owner in seen or db.execute('SELECT 1 FROM banned_publishers WHERE publisher=?',(publisher,)).fetchone():continue
        seen.add(owner);entries.append(dict(player=player,goals=goals,publisher=publisher))
        if len(entries)>=100:break
    return dict(schema=5,division=division,verified=False,entries=entries)
