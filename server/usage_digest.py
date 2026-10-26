"""Owner email summary of aggregate totals. No app email credentials or player mail."""
import argparse
from datetime import datetime,timezone,timedelta,date
from email.message import EmailMessage
from email.utils import parseaddr
import os
from pathlib import Path
import smtplib
import sqlite3
import ssl

LABELS={'sessions':'Sessões iniciadas','sessions_ended':'Sessões terminadas normalmente','new_careers':'Carreiras iniciadas','careers_loaded':'Carreiras carregadas',
        'trainings_completed':'Treinos concluídos','matches_completed':'Jogos concluídos',
        'goals_scored':'Golos dos jogadores','load_failures':'Falhas ao carregar','save_failures':'Falhas ao gravar'}

def summary(database,day):
    date.fromisoformat(day)
    with sqlite3.connect(database) as db:counts=dict(db.execute('SELECT event,count FROM totals WHERE day=?',(day,)))
    return 'SCORER Free — resumo de contadores recebidos ('+day+', UTC)\n\n'+'\n'.join(label+': '+str(counts.get(key,0)) for key,label in LABELS.items())+'\n\nTotais opcionais e aproximados, agrupados pelo dia de receção; podem incluir utilização offline anterior e não representam jogadores únicos. Não incluem nomes, emails dos jogadores, IDs de aparelhos ou dados de carreira.\n'

def address(value):
    if '\r' in value or '\n' in value or parseaddr(value)[1]!=value or '@' not in value:raise ValueError('Invalid server email configuration')
    return value

def send_message(subject,text):
    # Called only by the explicit server operator --send command.
    sender=address(os.environ.get('SCORER_STATS_MAIL_FROM',''))
    recipient=address(os.environ.get('SCORER_STATS_MAIL_TO',''))
    host=os.environ.get('SCORER_STATS_SMTP_HOST','')
    if not host or any(c.isspace() for c in host):raise ValueError('Server SMTP host required')
    message=EmailMessage();message['From']=sender;message['To']=recipient;message['Subject']=subject
    message.set_content(text)
    context=ssl.create_default_context()
    port=int(os.environ.get('SCORER_STATS_SMTP_PORT','587'))
    with smtplib.SMTP(host,port,timeout=10) as smtp:
        smtp.ehlo();smtp.starttls(context=context);smtp.ehlo()
        user=os.environ.get('SCORER_STATS_SMTP_USER','')
        if user:smtp.login(user,os.environ.get('SCORER_STATS_SMTP_PASSWORD',''))
        smtp.send_message(message)

def deliver(database,day):
    with sqlite3.connect(database) as db:
        db.execute('CREATE TABLE IF NOT EXISTS digests(day TEXT PRIMARY KEY)')
        if db.execute('SELECT 1 FROM digests WHERE day=?',(day,)).fetchone():return False
    send_message('SCORER Free — '+day,summary(database,day))
    with sqlite3.connect(database) as db:db.execute('INSERT OR IGNORE INTO digests(day) VALUES(?)',(day,))
    return True

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',type=Path,required=True);p.add_argument('--day',default=(datetime.now(timezone.utc).date()-timedelta(days=1)).isoformat());p.add_argument('--send',action='store_true',help='Explicit server-operator action; otherwise preview only')
    a=p.parse_args()
    if a.send:deliver(a.db,a.day)
    else:print(summary(a.db,a.day))
