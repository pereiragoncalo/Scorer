"""Pre-publication review, public opaque IDs, reports and publisher suspension."""
from datetime import datetime,timezone,timedelta
import hashlib,re
from server import season_records as records
from season_records import FIELDS,valid_record

REASONS={'personal_info','abuse','spam','other'}
def now():return datetime.now(timezone.utc).isoformat()
def public_id(owner):return hashlib.sha256(('scorer-public:'+owner).encode()).hexdigest()[:32]
def initialize(db):
    db.executescript('''CREATE TABLE IF NOT EXISTS moderation(owner TEXT,edition TEXT,country TEXT,division INTEGER,state TEXT NOT NULL DEFAULT 'pending',terms INTEGER NOT NULL DEFAULT 0,updated TEXT NOT NULL,PRIMARY KEY(owner,edition,country,division));
CREATE TABLE IF NOT EXISTS banned_publishers(publisher TEXT PRIMARY KEY,created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS reports(reporter TEXT,publisher TEXT,reason TEXT,created TEXT NOT NULL,PRIMARY KEY(reporter,publisher,reason));''')
    db.execute("INSERT OR IGNORE INTO moderation SELECT id,edition,country,division,'pending',0,? FROM season_records",(now(),))
def submit(db,payload):
    if not isinstance(payload,dict) or set(payload)!={'token','record','terms_version'} or type(payload['terms_version']) is not int or payload['terms_version']!=1 or not valid_record(payload['record']):raise ValueError('invalid submission')
    owner=records.identity(payload['token']);publisher=public_id(owner);r=payload['record']
    if db.execute('SELECT 1 FROM banned_publishers WHERE publisher=?',(publisher,)).fetchone():raise PermissionError('suspended')
    old=db.execute('SELECT goals FROM season_records WHERE id=? AND edition=? AND country=? AND division=?',(owner,r['edition'],r['country'],r['division'])).fetchone()
    key=(owner,r['edition'],r['country'],r['division'])
    current=db.execute('SELECT terms FROM moderation WHERE owner=? AND edition=? AND country=? AND division=?',key).fetchone()
    if current and current[0]!=1:db.execute('DELETE FROM season_records WHERE id=? AND edition=? AND country=? AND division=?',key)
    records.submit(db,{'token':payload['token'],'record':r})
    if old is None or r['goals']>old[0] or not current or current[0]!=1:
        db.execute("INSERT INTO moderation VALUES(?,?,?,?,'pending',1,?) ON CONFLICT(owner,edition,country,division) DO UPDATE SET state='pending',terms=1,updated=excluded.updated",(*key,now()))

def leaders(db,edition,country,division,version=3):
    # Reuse the input validation; do not use its unmoderated result/limit.
    records.leaders(db,edition,country,division)
    rows=db.execute("SELECT s.id,s.edition,s.country,s.division,s.season,s.player,s.team,s.matches,s.goals FROM season_records s JOIN moderation m ON (s.id=m.owner AND s.edition=m.edition AND s.country=m.country AND s.division=m.division) WHERE s.edition=? AND s.country=? AND s.division=? AND m.state='approved' AND m.terms=1 ORDER BY s.goals DESC,s.season,s.player",(edition,country,division)).fetchall()
    entries=[]
    for owner,*values in rows:
        publisher=public_id(owner)
        if db.execute('SELECT 1 FROM banned_publishers WHERE publisher=?',(publisher,)).fetchone():continue
        e=dict(zip(('edition','country','division','season','player','team','matches','goals'),values))
        if version==3:e.update(publisher=publisher,record_id=hashlib.sha256((publisher+'|'+edition+'|'+country+'|'+str(division)).encode()).hexdigest()[:32])
        entries.append(e)
        if len(entries)>=100:break
    return {'schema':version,'verified':False,'entries':entries}
def report(db,payload):
    if not isinstance(payload,dict) or set(payload)!={'token','publisher','reason'} or not isinstance(payload['reason'],str) or payload['reason'] not in REASONS or not re.fullmatch('[0-9a-f]{32}',str(payload['publisher'])):raise ValueError('invalid report')
    reporter=records.identity(payload['token']);publisher=payload['publisher']
    owners=db.execute('SELECT DISTINCT id FROM season_records').fetchall()
    if not any(public_id(o)==publisher for o, in owners):raise ValueError('unknown publisher')
    if db.execute('SELECT COUNT(*) FROM reports WHERE reporter=?',(reporter,)).fetchone()[0]>=20:raise ValueError('report limit')
    db.execute('INSERT OR IGNORE INTO reports VALUES(?,?,?,?)',(reporter,publisher,payload['reason'],now()))
def queue(db,offset=0):
    if type(offset) is not int or not 0<=offset<=1000000000:raise ValueError('invalid page')
    entries=[]
    for row in db.execute('SELECT s.id,s.edition,s.country,s.division,s.season,s.player,s.team,s.matches,s.goals,m.state,m.terms FROM season_records s JOIN moderation m ON (s.id=m.owner AND s.edition=m.edition AND s.country=m.country AND s.division=m.division) ORDER BY m.updated DESC LIMIT 100 OFFSET ?',(offset,)):
        owner,edition,country,division,season,player,team,matches,goals,state,terms=row
        entries.append(dict(publisher=public_id(owner),edition=edition,country=country,division=division,season=season,player=player,team=team,matches=matches,goals=goals,state=state,terms=terms))
    total=db.execute('SELECT COUNT(*) FROM season_records').fetchone()[0]
    return {'offset':offset,'total':total,'next':offset+100 if offset+100<total else None,'entries':entries,'reports':[dict(publisher=p,reason=r,count=c) for p,r,c in db.execute('SELECT publisher,reason,COUNT(*) FROM reports GROUP BY publisher,reason')],'banned':[p for p, in db.execute('SELECT publisher FROM banned_publishers')]}
def moderate(db,payload):
    if not isinstance(payload,dict) or set(payload)!={'publisher','action'} or not re.fullmatch('[0-9a-f]{32}',str(payload['publisher'])) or payload['action'] not in ('approve','reject','ban','unban','erase'):raise ValueError('invalid action')
    publisher=payload['publisher'];action=payload['action']
    owners=[o for o, in db.execute('SELECT DISTINCT id FROM season_records') if public_id(o)==publisher]
    if action=='ban':db.execute('INSERT OR IGNORE INTO banned_publishers VALUES(?,?)',(publisher,now()))
    elif action=='unban':db.execute('DELETE FROM banned_publishers WHERE publisher=?',(publisher,))
    for owner in owners:
        if action=='erase':
            db.execute('DELETE FROM season_records WHERE id=?',(owner,));db.execute('DELETE FROM moderation WHERE owner=?',(owner,))
        elif action in ('approve','reject'):
            db.execute('UPDATE moderation SET state=?,updated=? WHERE owner=? AND terms=1',('approved' if action=='approve' else 'rejected',now(),owner))
    if action in ('erase','reject','ban'):db.execute('DELETE FROM reports WHERE publisher=?',(publisher,))
def withdraw(db,token):
    owner=records.identity(token);publisher=public_id(owner);records.withdraw(db,token)
    db.execute('DELETE FROM moderation WHERE owner=?',(owner,));db.execute('DELETE FROM reports WHERE reporter=? OR publisher=?',(owner,publisher))
def prune(db):
    today=datetime.now(timezone.utc).date()
    db.execute('DELETE FROM totals WHERE day < ?',((today-timedelta(days=90)).isoformat(),))
    db.execute('DELETE FROM reports WHERE created < ?',((datetime.now(timezone.utc)-timedelta(days=30)).isoformat(),))
