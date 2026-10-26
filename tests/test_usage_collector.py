import contextlib,io,json,sqlite3,tempfile,threading,unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request,urlopen
from server.usage_collector import Collector
from server.usage_digest import summary,address

class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.db=Path(self.temp.name)/'usage.sqlite'
        self.server=Collector(('127.0.0.1',0),self.db,'test-owner-token');self.worker=threading.Thread(target=self.server.serve_forever,daemon=True);self.worker.start()
        self.addCleanup(self.server.server_close);self.addCleanup(self.server.shutdown);self.url='http://127.0.0.1:'+str(self.server.server_port)
    def post(self,data):
        r=Request(self.url+'/v1/usage',json.dumps(data).encode(),{'Content-Type':'application/json'},method='POST')
        with urlopen(r,timeout=2) as response:return response.status
    def test_real_http_aggregates_only_whitelist_counts_without_ip_or_raw_reports(self):
        log=io.StringIO()
        with contextlib.redirect_stderr(log):
            self.assertEqual(self.post({'schema':1,'app':'scorer_free','counts':{'sessions':2,'matches_completed':3}}),204)
            self.assertEqual(self.post({'schema':1,'app':'scorer_free','counts':{'sessions':1}}),204)
        with sqlite3.connect(self.db) as db:
            self.assertEqual({r[1] for r in db.execute('PRAGMA table_info(totals)')},{'day','event','count'})
            self.assertEqual(dict(db.execute('SELECT event,count FROM totals')),{'sessions':3,'matches_completed':3})
        self.assertEqual(log.getvalue(),'')
    def test_unknown_fields_identifiers_and_invalid_bodies_never_enter_database(self):
        for payload in ({'schema':1,'app':'scorer_free','counts':{'email':1}}, {'schema':1,'app':'scorer_free','counts':{'sessions':1},'player':'private'}, {'schema':1,'app':'scorerworld','counts':{'sessions':1}}, {'schema':1,'app':'scorer_free','counts':{'sessions':-1}}):
            with self.assertRaises(HTTPError) as error:self.post(payload)
            self.assertEqual(error.exception.code,400)
        with sqlite3.connect(self.db) as db:self.assertEqual(db.execute('SELECT COUNT(*) FROM totals').fetchone()[0],0)
    def test_owner_totals_require_server_only_bearer_token(self):
        for headers in ({},{'Authorization':'Bearer wrong'}):
            with self.assertRaises(HTTPError):urlopen(Request(self.url+'/v1/totals',headers=headers),timeout=2)
        with urlopen(Request(self.url+'/v1/totals',headers={'Authorization':'Bearer test-owner-token'}),timeout=2) as response:self.assertEqual(json.load(response),{'schema':1,'totals':[]})
    def test_email_preview_uses_aggregate_totals_only_and_no_message_is_sent(self):
        self.post({'schema':1,'app':'scorer_free','counts':{'sessions':3}})
        with sqlite3.connect(self.db) as db:day=db.execute('SELECT day FROM totals').fetchone()[0]
        text=summary(self.db,day);self.assertIn('Sessões iniciadas: 3',text);self.assertIn('não representam jogadores únicos',text)
        self.assertNotIn('127.0.0.1',text)
        for value in ('x@example.com\nBcc: bad@example.com','not-an-address'):
            with self.assertRaises(ValueError):address(value)
