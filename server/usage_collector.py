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

class Collector(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,address,database,admin_token=''):
        self.database=str(database);self.admin_token=admin_token
        self._rate_lock=threading.Lock();self._second=0;self._requests=0;self._slots=threading.BoundedSemaphore(16)
        Path(self.database).parent.mkdir(parents=True,exist_ok=True)
        with self.db() as db:
            db.execute('CREATE TABLE IF NOT EXISTS totals(day TEXT NOT NULL,event TEXT NOT NULL,count INTEGER NOT NULL,PRIMARY KEY(day,event))')
            initialize(db)
        super().__init__(address,Handler)
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
    def do_POST(self):
        if self.path not in ('/v1/usage','/v1/leaderboard','/v1/leaderboard/withdraw'):self.reply(404,{'error':'not_found'});return
        if not self.server.allow():self.reply(429,{'error':'busy'});return
        try:length=int(self.headers.get('Content-Length','0'))
        except ValueError:self.reply(400,{'error':'invalid'});return
        if not 0<length<=4096 or self.headers.get('Transfer-Encoding') or self.headers.get_content_type()!='application/json':self.reply(400,{'error':'invalid'});return
        self.connection.settimeout(5)
        try:
            data=json.loads(self.rfile.read(length))
            if self.path!='/v1/usage':
                with self.server.db() as db:
                    if self.path.endswith('/withdraw'):
                        if not isinstance(data,dict) or set(data)!={'token'}:raise ValueError('invalid')
                        withdraw(db,data['token'])
                    else:submit(db,data)
                self.reply(204,{});return
            if not valid_payload(data):self.reply(400,{'error':'invalid'});return
            today=datetime.now(timezone.utc).date()
            with self.server.db() as db:
                for event,count in data['counts'].items():
                    db.execute('INSERT INTO totals(day,event,count) VALUES(?,?,?) ON CONFLICT(day,event) DO UPDATE SET count=count+excluded.count',(today.isoformat(),event,count))
                db.execute('DELETE FROM totals WHERE day < ?',((today-timedelta(days=90)).isoformat(),))
            self.reply(204,{})
        except (ValueError,UnicodeError,TimeoutError,OSError):self.reply(400,{'error':'invalid'})
        except Exception:self.reply(503,{'error':'unavailable'})
    def do_GET(self):
        if self.path=='/admin':
            body=(Path(__file__).parent/'dashboard.html').read_bytes()
            self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Cache-Control','no-store');self.send_header('X-Frame-Options','DENY')
            self.send_header('Content-Security-Policy',"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
            self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
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
            with self.server.db() as db:rows=db.execute('SELECT day,event,count FROM totals ORDER BY day,event').fetchall()
            self.reply(200,{'schema':1,'totals':[{'day':d,'event':e,'count':n} for d,e,n in rows]})
        except Exception:self.reply(503,{'error':'unavailable'})

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--bind',default='127.0.0.1');p.add_argument('--port',type=int,default=8080);p.add_argument('--db',type=Path,required=True)
    a=p.parse_args();Collector((a.bind,a.port),a.db,os.environ.get('SCORER_STATS_ADMIN_TOKEN','')).serve_forever()
