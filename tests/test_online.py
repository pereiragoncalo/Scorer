import http.client,json,sqlite3,tempfile,threading,unittest
from pathlib import Path
from unittest.mock import patch
from server.usage_collector import Collector
from server.leaderboard import initialize,submit,leaders,withdraw
from online_leaderboard import Leaderboard,valid_origin

class OnlineTests(unittest.TestCase):
    def payload(self,**kw):
        d=dict(token='a'*64,alias='Striker-1',edition='free',season=2026,matches=3,goals=4);d.update(kw);return d
    def test_validation_ownership_monotonicity_and_withdrawal(self):
        with sqlite3.connect(':memory:') as db:
            initialize(db);submit(db,self.payload());submit(db,self.payload(matches=4,goals=5))
            for changes in ({'goals':999},{'matches':True},{'alias':'<script>'},{'matches':2},{'goals':6},{'token':'x'}):
                with self.assertRaises(ValueError):submit(db,self.payload(**changes))
            self.assertEqual(leaders(db)['entries'][0]['goals'],5)
            withdraw(db,'b'*64);self.assertEqual(len(leaders(db)['entries']),1)
            withdraw(db,'a'*64);self.assertEqual(leaders(db)['entries'],[])
    def test_no_raw_token_in_database_or_public_scores(self):
        with sqlite3.connect(':memory:') as db:
            initialize(db);submit(db,self.payload())
            self.assertNotIn('a'*64,'\n'.join(db.iterdump()))
            self.assertNotIn('token',json.dumps(leaders(db)))
    def test_real_http_submit_get_dashboard_private_totals_and_delete(self):
        with tempfile.TemporaryDirectory() as t:
            server=Collector(('127.0.0.1',0),Path(t)/'test.sqlite','private-admin')
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            def req(method,path,data=None,headers=None):
                c=http.client.HTTPConnection(*server.server_address,timeout=3)
                h={'Content-Type':'application/json'};h.update(headers or {})
                c.request(method,path,None if data is None else json.dumps(data),h);r=c.getresponse();body=r.read();status=r.status;c.close();return status,body
            try:
                self.assertEqual(req('POST','/v1/leaderboard',self.payload())[0],204)
                self.assertIn(b'Striker-1',req('GET','/v1/leaderboard')[1])
                self.assertEqual(req('GET','/v1/totals')[0],404)
                self.assertEqual(req('GET','/v1/totals',headers={'Authorization':'Bearer private-admin'})[0],200)
                self.assertIn(b'type="password"',req('GET','/admin')[1])
                self.assertEqual(req('POST','/v1/leaderboard',{'alias':'x'})[0],400)
                self.assertEqual(req('POST','/v1/leaderboard/withdraw',{'token':'a'*64})[0],204)
                self.assertEqual(json.loads(req('GET','/v1/leaderboard')[1])['entries'],[])
            finally:server.shutdown();server.server_close();thread.join()
    def test_client_consent_origin_reset_pseudonym_and_https_only(self):
        for invalid in ('http://host','https://x/path','https://user:pass@x','https://x:8787','https://x?token=x'):
            self.assertFalse(valid_origin(invalid))
        self.assertTrue(valid_origin('https://stats.example.com'))
        with tempfile.TemporaryDirectory() as t:
            b=Leaderboard(t,'https://stats.example.com');self.assertFalse(b.enabled)
            b.enabled=True;b.save();self.assertTrue(Leaderboard(t,b.origin).enabled)
            self.assertFalse(Leaderboard(t,'https://different.example.com').enabled)
            self.assertNotIn('Alex',b.alias)
            with self.assertRaises(ValueError):Leaderboard(t,'').request('/v1/leaderboard')
    def test_client_offline_keeps_withdrawal_and_never_posts_without_opt_in(self):
        from types import SimpleNamespace
        c=SimpleNamespace(season=2026,matches=3,goals=4)
        with tempfile.TemporaryDirectory() as t:
            b=Leaderboard(t,'https://stats.example.com');done=threading.Event()
            with patch.object(b,'request',return_value={'schema':2,'entries':[]}) as req:
                b.sync(c,False,done.set);self.assertTrue(done.wait(3))
                self.assertEqual(req.call_args_list[0].args,('/v2/records?edition=free&country=Scorer&division=1',))
            b.pending_withdrawal=True;b.save();done.clear()
            with patch.object(b,'request',side_effect=OSError):
                b.sync(c,False,done.set,withdraw=True);self.assertTrue(done.wait(3))
                self.assertTrue(b.pending_withdrawal)

    def test_android_fallback_has_public_roots_and_requires_valid_https(self):
        import ssl,sys
        from network_tls import verified_context
        with patch.dict(sys.modules,{'certifi':None}):
            context=verified_context()
        self.assertEqual(context.verify_mode,ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname);self.assertGreater(len(context.get_ca_certs()),100)
        for certificate in context.get_ca_certs():
            self.assertNotIn('mitm',str(certificate.get('subject')).lower())
