"""Minimal aggregate-only collector. Place behind HTTPS with access logs disabled."""
import argparse
from datetime import datetime,timezone,timedelta
import hmac
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
import os
from pathlib import Path
import sqlite3
import sys
import threading
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from anonymous_stats import valid_payload
from server.leaderboard import initialize,submit,leaders,withdraw
from server import season_records as records
from server import moderation,privacy_cases
from urllib.parse import urlsplit,parse_qs

def activity(db,today=None):
    """Thirty UTC receipt dates, inclusive of today, with zero-filled rows."""
    today=today or datetime.now(timezone.utc).date()
    start=today-timedelta(days=29)
    rows=db.execute("SELECT day,event,count FROM totals WHERE day BETWEEN ? AND ? AND event IN ('sessions','sessions_ended')",(start.isoformat(),today.isoformat())).fetchall()
    counts={(day,event):count for day,event,count in rows}
    days=[{'day':(today-timedelta(days=i)).isoformat(),
           'opens':counts.get(((today-timedelta(days=i)).isoformat(),'sessions'),0),
           'closes':counts.get(((today-timedelta(days=i)).isoformat(),'sessions_ended'),0)} for i in range(30)]
    return {'schema':1,'timezone':'UTC','start':start.isoformat(),'end':today.isoformat(),
            'opens':sum(d['opens'] for d in days),'closes':sum(d['closes'] for d in days),'days':days}

class Collector(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,address,database,admin_token='',public_config=None):
        self.database=str(database);self.admin_token=admin_token;self.public_config=public_config or '/opt/scorer/public.json';self._last_prune=0
        self._rate_lock=threading.Lock();self._second=0;self._requests=0;self._slots=threading.BoundedSemaphore(16)
        Path(self.database).parent.mkdir(parents=True,exist_ok=True)
        with self.db() as db:
            db.execute('CREATE TABLE IF NOT EXISTS totals(day TEXT NOT NULL,event TEXT NOT NULL,count INTEGER NOT NULL,PRIMARY KEY(day,event))')
            initialize(db)
            records.initialize(db)
            moderation.initialize(db)
            privacy_cases.initialize(db)
            moderation.prune(db);privacy_cases.prune(db)
        super().__init__(address,Handler)
    def service_actions(self):
        if time.monotonic()-self._last_prune>3600:
            try:
                with self.db() as db:moderation.prune(db);privacy_cases.prune(db)
                self._last_prune=time.monotonic()
            except sqlite3.Error:pass
    def get_request(self):
        connection,address=super().get_request();connection.settimeout(5);return connection,address
    def process_request(self,request,address):
        if not self._slots.acquire(blocking=False):self.shutdown_request(request);return
        try:super().process_request(request,address)
        except Exception:self._slots.release();raise
    def process_request_thread(self,request,address):
        try:super().process_request_thread(request,address)
        finally:self._slots.release()
    def db(self):return sqlite3.connect(self.database,timeout=3)
    def handle_error(self,*_):pass  # Never log a request address or raw body.
    def allow(self):
        with self._rate_lock:
            second=int(time.monotonic())
            if second!=self._second:self._second=second;self._requests=0
            self._requests+=1;return self._requests<=20

class Handler(BaseHTTPRequestHandler):
    server_version='ScorerStats';sys_version=''
    def log_message(self,*_):pass
    def log_error(self,*_):pass
    def reply(self,status,data):
        body=b'' if status==204 else json.dumps(data,separators=(',',':')).encode('utf8')
        self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers()
        try:self.wfile.write(body)
        except OSError:pass
    def authorized(self):
        return bool(self.server.admin_token) and hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+self.server.admin_token)
    def do_POST(self):
        if self.path in ('/v1/moderation','/v1/privacy/admin'):
            if not self.authorized():self.reply(404,{'error':'not_found'});return
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=4096 or self.headers.get('Transfer-Encoding') or self.headers.get_content_type()!='application/json':raise ValueError()
                data=json.loads(self.rfile.read(length))
                with self.server.db() as db:
                    if self.path=='/v1/privacy/admin':privacy_cases.resolve(db,data)
                    else:moderation.moderate(db,data)
                self.reply(204,{})
            except (ValueError,TypeError):self.reply(400,{'error':'invalid'})
            except Exception:self.reply(503,{'error':'unavailable'})
            return
        if self.path in ('/v1/leaderboard','/v2/records'):
            self.reply(426,{'error':'app_update_required'});return
        if self.path not in ('/v1/usage','/v1/leaderboard','/v1/leaderboard/withdraw','/v2/records','/v2/records/withdraw','/v3/records','/v3/records/withdraw','/v4/records','/v4/records/withdraw','/v3/reports','/v1/privacy/request'):self.reply(404,{'error':'not_found'});return
        if not self.server.allow():self.reply(429,{'error':'busy'});return
        try:length=int(self.headers.get('Content-Length','0'))
        except ValueError:self.reply(400,{'error':'invalid'});return
        if not 0<length<=4096 or self.headers.get('Transfer-Encoding') or self.headers.get_content_type()!='application/json':self.reply(400,{'error':'invalid'});return
        self.connection.settimeout(5)
        try:
            data=json.loads(self.rfile.read(length))
            if self.path=='/v1/privacy/request':
                with self.server.db() as db:result=privacy_cases.request(db,data)
                self.reply(200,result);return
            if self.path!='/v1/usage':
                with self.server.db() as db:
                    if self.path.endswith('/withdraw'):
                        if not isinstance(data,dict) or set(data)!={'token'}:raise ValueError('invalid')
                        moderation.withdraw(db,data['token'])
                    elif self.path=='/v4/records':
                        from server.career_records import submit as submit_career
                        submit_career(db,data)
                    elif self.path=='/v3/records':moderation.submit(db,data)
                    elif self.path=='/v3/reports':moderation.report(db,data)
                    else:submit(db,data)
                self.reply(204,{});return
            if not valid_payload(data):self.reply(400,{'error':'invalid'});return
            today=datetime.now(timezone.utc).date()
            with self.server.db() as db:
                for event,count in data['counts'].items():
                    db.execute('INSERT INTO totals(day,event,count) VALUES(?,?,?) ON CONFLICT(day,event) DO UPDATE SET count=count+excluded.count',(today.isoformat(),event,count))
                db.execute('DELETE FROM totals WHERE day < ?',((today-timedelta(days=90)).isoformat(),))
            self.reply(204,{})
        except PermissionError:self.reply(403,{'error':'suspended'})
        except (ValueError,UnicodeError,TimeoutError,OSError):self.reply(400,{'error':'invalid'})
        except Exception:self.reply(503,{'error':'unavailable'})
    def do_GET(self):
        if self.path=='/v1/app-version':
            if not self.server.allow():self.reply(429,{'error':'busy'});return
            try:
                from version_policy import read
                from server.version_updates import policy_path
                self.reply(200,read(policy_path(self.server.public_config)))
            except (OSError,ValueError,TypeError):self.reply(503,{'error':'version_policy_unavailable'})
            return
        if self.path in ('/privacy','/terms','/delete'):
            from server.public_pages import page
            status,body=page(self.path,self.server.public_config)
            self.send_response(status);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'none'; style-src 'unsafe-inline'; frame-ancestors 'none'")
            self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
        if self.path in ('/v1/moderation','/v1/privacy/admin') or self.path.startswith(('/v1/moderation?','/v1/privacy/admin?')):
            if not self.authorized():self.reply(404,{'error':'not_found'});return
            try:
                query=parse_qs(urlsplit(self.path).query,strict_parsing=True)
                if set(query)-{'offset'} or any(len(v)!=1 for v in query.values()):raise ValueError('invalid page')
                offset=int(query.get('offset',['0'])[0])
                with self.server.db() as db:data=privacy_cases.queue(db,offset) if self.path.startswith('/v1/privacy/admin') else moderation.queue(db,offset)
                self.reply(200,data)
            except ValueError:self.reply(400,{'error':'invalid'})
            except Exception:self.reply(503,{'error':'unavailable'})
            return
        if self.path=='/v1/activity':
            if not self.authorized():self.reply(404,{'error':'not_found'});return
            try:
                with self.server.db() as db:data=activity(db)
                self.reply(200,data)
            except Exception:self.reply(503,{'error':'unavailable'})
            return
        if self.path in ('/admin','/admin/manage'):
            body=(Path(__file__).parent/('dashboard.html' if self.path=='/admin' else 'management.html')).read_bytes()
            self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Cache-Control','no-store');self.send_header('X-Frame-Options','DENY')
            self.send_header('Content-Security-Policy',"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
            self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
        if self.path.startswith('/v4/records?'):
            if not self.server.allow():self.reply(429,{'error':'busy'});return
            try:
                q=parse_qs(urlsplit(self.path).query,strict_parsing=True)
                if set(q)!={'edition','country','division'} or any(len(v)!=1 for v in q.values()):raise ValueError('invalid filter')
                from server.career_records import leaders as career_leaders
                with self.server.db() as db:data=career_leaders(db,q['edition'][0],q['country'][0],int(q['division'][0]))
                self.reply(200,data)
            except ValueError:self.reply(400,{'error':'invalid'})
            except Exception:self.reply(503,{'error':'unavailable'})
            return
        if self.path.startswith(('/v2/records?','/v3/records?')):
            if not self.server.allow():self.reply(429,{'error':'busy'});return
            try:
                q=parse_qs(urlsplit(self.path).query,strict_parsing=True)
                if set(q)!={'edition','country','division'} or any(len(v)!=1 for v in q.values()):raise ValueError('invalid filter')
                with self.server.db() as db:data=moderation.leaders(db,q['edition'][0],q['country'][0],int(q['division'][0]),3 if self.path.startswith('/v3/') else 2)
                self.reply(200,data)
            except (ValueError,KeyError):self.reply(400,{'error':'invalid'})
            except Exception:self.reply(503,{'error':'unavailable'})
            return
        if self.path=='/health':self.reply(200,{'ok':True});return
        if self.path=='/v1/leaderboard':
            if not self.server.allow():self.reply(429,{'error':'busy'});return
            try:
                with self.server.db() as db:data=leaders(db)
                self.reply(200,data)
            except Exception:self.reply(503,{'error':'unavailable'})
            return
        expected='Bearer '+self.server.admin_token
        supplied=self.headers.get('Authorization','')
        if self.path!='/v1/totals' or not self.server.admin_token or not hmac.compare_digest(supplied,expected):self.reply(404,{'error':'not_found'});return
        try:
            with self.server.db() as db:
                moderation.prune(db);privacy_cases.prune(db)
                rows=db.execute('SELECT day,event,count FROM totals ORDER BY day,event').fetchall()
            self.reply(200,{'schema':1,'totals':[{'day':d,'event':e,'count':n} for d,e,n in rows]})
        except Exception:self.reply(503,{'error':'unavailable'})

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--bind',default='127.0.0.1');p.add_argument('--port',type=int,default=8080);p.add_argument('--db',type=Path,required=True)
    a=p.parse_args();Collector((a.bind,a.port),a.db,os.environ.get('SCORER_STATS_ADMIN_TOKEN','')).serve_forever()
