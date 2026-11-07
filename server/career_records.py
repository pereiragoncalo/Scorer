"""v4 career board, separate from the best-completed-season table."""
from career_records import valid_record
from season_records import FIELDS
from server.season_records import identity
from server.moderation import now,public_id
import hashlib

def initialize(db):db.execute('CREATE TABLE IF NOT EXISTS career_records(id TEXT,edition TEXT,country TEXT,division INTEGER,season INTEGER,player TEXT,team TEXT,matches INTEGER,goals INTEGER,PRIMARY KEY(id,edition,country,division))')
def submit(db,payload):
 if not isinstance(payload,dict) or set(payload)!={'token','record','terms_version'} or type(payload['terms_version'])is not int or payload['terms_version']!=1 or not valid_record(payload['record']):raise ValueError('invalid career')
 owner=identity(payload['token']);r=payload['record'];publisher=public_id(owner)
 if db.execute('SELECT 1 FROM banned_publishers WHERE publisher=?',(publisher,)).fetchone():raise PermissionError('suspended')
 key=(owner,r['edition'],r['country'],r['division']);old=db.execute('SELECT matches,goals FROM career_records WHERE id=? AND edition=? AND country=? AND division=?',key).fetchone()
 if old and (r['matches']<old[0] or r['goals']<old[1]):return
 if old==(r['matches'],r['goals']):return
 db.execute('INSERT INTO career_records VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(id,edition,country,division) DO UPDATE SET season=excluded.season,player=excluded.player,team=excluded.team,matches=excluded.matches,goals=excluded.goals',(*key,r['season'],r['player'],r['team'],r['matches'],r['goals']))
 db.execute("INSERT INTO moderation VALUES(?,?,?,?,'pending',1,?) ON CONFLICT(owner,edition,country,division) DO UPDATE SET state='pending',terms=1,updated=excluded.updated",(*key,now()))
def leaders(db,edition,country,division):
 from server.season_records import leaders as validate
 validate(db,edition,country,division);entries=[]
 for owner,*values in db.execute("SELECT s.id,s.edition,s.country,s.division,s.season,s.player,s.team,s.matches,s.goals FROM career_records s JOIN moderation m ON s.id=m.owner AND s.edition=m.edition AND s.country=m.country AND s.division=m.division WHERE s.edition=? AND s.country=? AND s.division=? AND m.state='approved' AND m.terms=1 ORDER BY s.goals DESC,s.matches,s.player",(edition,country,division)):
  publisher=public_id(owner)
  if db.execute('SELECT 1 FROM banned_publishers WHERE publisher=?',(publisher,)).fetchone():continue
  e=dict(zip(('edition','country','division','season','player','team','matches','goals'),values));e.update(publisher=publisher,record_id=hashlib.sha256((publisher+'|career|'+edition+'|'+country+'|'+str(division)).encode()).hexdigest()[:32]);entries.append(e)
  if len(entries)>=100:break
 return dict(schema=4,category='career',verified=False,entries=entries)
