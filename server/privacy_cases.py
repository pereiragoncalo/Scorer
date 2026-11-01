"""Minimal private rights cases; never attach case IDs to usage reports."""
from datetime import datetime,timezone,timedelta
import hashlib,re
from privacy_requests import reference

def initialize(db):
    db.execute('CREATE TABLE IF NOT EXISTS privacy_cases(id TEXT PRIMARY KEY,reference TEXT UNIQUE,status TEXT,created TEXT,updated TEXT)')

def request(db,data):
    if not isinstance(data,dict) or set(data)!={'token','action'} or not isinstance(data['token'],str) or not re.fullmatch('[0-9a-f]{64}',data['token']) or data['action'] not in ('object','withdraw'):raise ValueError('Invalid rights request')
    key=hashlib.sha256(data['token'].encode()).hexdigest();ref=reference(data['token']);now=datetime.now(timezone.utc).isoformat()
    old=db.execute('SELECT status FROM privacy_cases WHERE id=?',(key,)).fetchone()
    if data['action']=='withdraw':
        db.execute("INSERT INTO privacy_cases VALUES(?,?,'closed',?,?) ON CONFLICT(id) DO UPDATE SET status='closed',updated=excluded.updated",(key,ref,now,now));status='closed'
    elif old and old[0] in ('pending','granted'):status=old[0]
    else:
        db.execute("INSERT INTO privacy_cases VALUES(?,?,'pending',?,?) ON CONFLICT(id) DO UPDATE SET status='pending',updated=excluded.updated",(key,ref,now,now));status='pending'
    return dict(schema=1,reference=ref,status=status)

def queue(db,offset=0):
    if type(offset) is not int or not 0<=offset<=1000000000:raise ValueError('Invalid page')
    total=db.execute('SELECT COUNT(*) FROM privacy_cases').fetchone()[0]
    return dict(entries=[dict(reference=r,status=s,created=c,updated=u) for r,s,c,u in db.execute('SELECT reference,status,created,updated FROM privacy_cases ORDER BY created DESC LIMIT 100 OFFSET ?',(offset,))],offset=offset,next=offset+100 if offset+100<total else None,total=total)

def resolve(db,data):
    if not isinstance(data,dict) or set(data)!={'reference','action'} or data['action']!='grant' or not isinstance(data['reference'],str) or not re.fullmatch('SCW-[0-9A-F]{20}',data['reference']):raise ValueError('Invalid case action')
    # Controller can uphold the objection; only the requester's secret can withdraw it.
    db.execute("UPDATE privacy_cases SET status='granted',updated=? WHERE reference=? AND status='pending'",(datetime.now(timezone.utc).isoformat(),data['reference']))

def prune(db):
    cutoff=(datetime.now(timezone.utc)-timedelta(days=90)).isoformat()
    db.execute("DELETE FROM privacy_cases WHERE status IN ('granted','closed') AND updated < ?",(cutoff,))
