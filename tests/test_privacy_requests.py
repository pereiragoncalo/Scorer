import http.client,json,sqlite3,tempfile,threading,unittest
from pathlib import Path
from unittest.mock import patch
from privacy_requests import PrivacyRequest,reference
from anonymous_stats import create_statistics
from server.usage_collector import Collector
from server import privacy_cases
from server.maintenance import backup

class PrivacyClientTests(unittest.TestCase):
    def test_normal_usage_has_no_case_identifier_and_no_normal_off_switch(self):
        with tempfile.TemporaryDirectory() as t:
            u=create_statistics(True,t,endpoint='');u.begin_session()
            self.assertTrue(u.enabled);self.assertFalse(u.set_enabled(False));self.assertFalse(PrivacyRequest(t).active)
            self.assertFalse((Path(t)/'scorer_privacy_request.json').exists())
            self.assertEqual(u.counts,{'sessions':1})
    def test_reject_notice_discards_counts_and_never_retries_on_stop(self):
        with tempfile.TemporaryDirectory() as t:
            u=create_statistics(True,t,endpoint='https://stats.example.com/v1/usage');u.begin_session()
            with patch.object(u,'_sender') as sender:
                u.reject_notice();self.assertEqual(u.counts,{})
                self.assertFalse(u.record('goals_scored'));self.assertFalse(u.flush_async())
                self.assertFalse(u.delivery_ready);sender.assert_not_called()
            again=create_statistics(True,t,endpoint='');self.assertFalse(again.delivery_ready)
    def test_old_case_file_does_not_restore_removed_client_workflow(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t)/'scorer_privacy_request.json').write_text('{broken')
            u=create_statistics(True,t,endpoint='');u.begin_session()
            self.assertEqual(u.counts,{'sessions':1});self.assertFalse(u.delivery_ready)

    def test_offline_and_failed_withdrawal_keep_hold(self):
        with tempfile.TemporaryDirectory() as t:
            r=PrivacyRequest(t,'https://stats.example.com');r.object();done=threading.Event()
            with patch('online_leaderboard.Leaderboard.request',side_effect=OSError('offline')):
                self.assertTrue(r.sync(done.set,withdraw=True,force=True));self.assertTrue(done.wait(3))
            self.assertTrue(r.active);self.assertTrue(PrivacyRequest(t).active)
    def test_failed_withdrawal_persistence_never_exposes_closed_state(self):
        with tempfile.TemporaryDirectory() as t:
            r=PrivacyRequest(t,'https://stats.example.com');r.object();done=threading.Event();observed=[]
            def fail_save(*args,**kwargs):
                observed.append(r.active);raise OSError('disk')
            with patch('online_leaderboard.Leaderboard.request',return_value=dict(schema=1,reference=r.case_reference,status='closed')),patch.object(r,'save',side_effect=fail_save):
                r.sync(done.set,withdraw=True,force=True);self.assertTrue(done.wait(3))
            self.assertEqual(observed,[True]);self.assertTrue(r.active);self.assertTrue(PrivacyRequest(t).active)

    def test_only_valid_persisted_withdrawal_releases_request(self):
        with tempfile.TemporaryDirectory() as t:
            r=PrivacyRequest(t,'https://stats.example.com');r.object();done=threading.Event()
            with patch('online_leaderboard.Leaderboard.request',return_value=dict(schema=1,reference=r.case_reference,status='closed')):
                r.sync(done.set,withdraw=True,force=True);self.assertTrue(done.wait(3))
            self.assertFalse(PrivacyRequest(t).active)

class PrivacyServiceTests(unittest.TestCase):
    def test_real_http_case_private_admin_and_unlinked_aggregate_backup(self):
        with tempfile.TemporaryDirectory() as t:
            dbpath=Path(t)/'data.sqlite';service=Collector(('127.0.0.1',0),dbpath,'test-admin')
            thread=threading.Thread(target=service.serve_forever,daemon=True);thread.start()
            def call(path,data=None,admin=False):
                c=http.client.HTTPConnection(*service.server_address,timeout=3);h={'Content-Type':'application/json'}
                if admin:h['Authorization']='Bearer test-admin'
                c.request('POST' if data is not None else 'GET',path,json.dumps(data) if data is not None else None,h);r=c.getresponse();body=r.read();c.close();return r.status,json.loads(body) if body else None
            token='a'*64
            try:
                status,d=call('/v1/privacy/request',dict(token=token,action='object'));self.assertEqual(status,200);self.assertEqual(d['status'],'pending');ref=d['reference']
                self.assertEqual(call('/v1/privacy/admin')[0],404)
                self.assertEqual(call('/v1/privacy/admin',dict(reference=ref,action='grant'))[0],404)
                status,q=call('/v1/privacy/admin',admin=True);self.assertEqual(status,200);self.assertEqual(q['total'],1);self.assertNotIn(token,json.dumps(q))
                self.assertEqual(call('/v1/privacy/admin',dict(reference=ref,action='grant'),True)[0],204)
                self.assertEqual(call('/v1/privacy/request',dict(token=token,action='object'))[1]['status'],'granted')
                self.assertEqual(call('/v1/privacy/request',dict(token='b'*64,action='withdraw'))[1]['status'],'closed')
                self.assertEqual(call('/v1/privacy/request',dict(token=token,action='object'))[1]['status'],'granted')
                self.assertEqual(call('/v1/privacy/request',dict(token=token,action='withdraw'))[1]['status'],'closed')
                self.assertEqual(call('/v1/privacy/request',dict(reference=ref,action='withdraw'))[0],400)
                with service.db() as db:
                    self.assertEqual(db.execute('SELECT COUNT(*) FROM totals').fetchone()[0],0)
                    self.assertNotIn(token,str(db.execute('SELECT * FROM privacy_cases').fetchall()))
                    db.execute("UPDATE privacy_cases SET updated='2000-01-01'");privacy_cases.prune(db);self.assertEqual(privacy_cases.queue(db)['total'],0)
                    privacy_cases.request(db,dict(token=token,action='object'));db.execute("UPDATE privacy_cases SET updated='2000-01-01'");privacy_cases.prune(db);self.assertEqual(privacy_cases.queue(db)['total'],1)
                b=Path(t)/'backup.sqlite';backup(dbpath,b)
                with sqlite3.connect(b) as db:self.assertEqual(db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall(),[('totals',)])
            finally:service.shutdown();service.server_close();thread.join()
