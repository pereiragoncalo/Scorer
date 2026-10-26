"""Server-side opt-in session notices. Default is preview; no app SMTP secrets."""
import argparse
from pathlib import Path
import sqlite3
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from server.usage_digest import send_message

EVENTS=('sessions','sessions_ended')
LABELS={'sessions':'Sessões iniciadas','sessions_ended':'Sessões terminadas normalmente'}

def pending(database):
    with sqlite3.connect(database) as db:
        db.execute('CREATE TABLE IF NOT EXISTS session_notices(day TEXT NOT NULL,event TEXT NOT NULL,count INTEGER NOT NULL,PRIMARY KEY(day,event))')
        rows=db.execute("SELECT t.day,t.event,t.count,COALESCE(n.count,0) FROM totals t LEFT JOIN session_notices n ON t.day=n.day AND t.event=n.event WHERE t.event IN ('sessions','sessions_ended') ORDER BY t.day,t.event").fetchall()
    return [(day,event,count,count-old) for day,event,count,old in rows if count>old]

def acknowledge(database,rows):
    with sqlite3.connect(database) as db:
        for day,event,count,_ in rows:
            db.execute('INSERT INTO session_notices(day,event,count) VALUES(?,?,?) ON CONFLICT(day,event) DO UPDATE SET count=MAX(count,excluded.count)',(day,event,count))
        db.execute('DELETE FROM session_notices WHERE day NOT IN (SELECT DISTINCT day FROM totals)')

def preview(rows):
    if not rows:return ''
    return ('SCORER Free — atividade de sessões recebida\n\n'+'\n'.join(day+' (UTC): '+LABELS[event]+': '+str(delta) for day,event,_,delta in rows)+
            '\n\nContadores opcionais e aproximados, sem nomes ou identificadores de jogadores. Podem incluir eventos offline recebidos com atraso. Um fecho forçado pode não produzir aviso de fim. Inícios e fins não são associados à mesma pessoa.\n')

def run(database,send=False,baseline=False):
    rows=pending(database);text=preview(rows)
    if baseline:
        acknowledge(database,rows);return ''
    if send and rows:
        send_message('SCORER Free — início/fim de sessões',text)
        acknowledge(database,rows)
    return text

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',type=Path,required=True)
    group=p.add_mutually_exclusive_group();group.add_argument('--send',action='store_true');group.add_argument('--baseline',action='store_true',help='Skip current historical totals without sending')
    a=p.parse_args();print(run(a.db,a.send,a.baseline))
