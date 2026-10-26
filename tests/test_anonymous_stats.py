import io,json,os,tempfile,threading,time,unittest
from datetime import date,timedelta
from pathlib import Path
from unittest.mock import patch
from anonymous_stats import UsageStatistics,create_statistics,valid_endpoint,valid_payload,send_counts,EVENTS
from tools.prepare_editions import prepare_edition

class AnonymousStatsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
    def wait(self,s):
        end=time.monotonic()+3
        while s._sending and time.monotonic()<end:threading.Event().wait(.01)
        self.assertFalse(s._sending)
    def test_default_off_no_file_and_no_events_before_explicit_choice(self):
        s=UsageStatistics(self.root);s.begin_session();self.assertFalse(s.record('matches_completed'));self.assertFalse(s.flush_async());self.assertFalse(s.path.exists())
        self.assertTrue(s.set_enabled(True));self.assertEqual(s.counts,{'sessions':1});s.begin_session();self.assertEqual(s.counts,{'sessions':1})
    def test_world_has_no_preference_io_or_sender(self):
        with patch.object(Path,'stat',side_effect=AssertionError('World IO')),patch.object(Path,'read_text',side_effect=AssertionError('World IO')):
            s=create_statistics(True,self.root);s.begin_session();self.assertFalse(s.record('sessions'));self.assertFalse(s.set_enabled(True));self.assertFalse(s.flush_async())
    def test_allowlist_rejects_names_parameters_bool_and_invalid_counts(self):
        s=UsageStatistics(self.root);s.set_enabled(True)
        for event,amount in [('Alex Silva',1),('player_name',1),([],1),('sessions',True),('sessions',0),('sessions',-1),('sessions',10001),('sessions','1')]:self.assertFalse(s.record(event,amount))
        self.assertTrue(s.record('matches_completed'));data=json.loads(s.path.read_text());self.assertEqual(set(data),{'schema','enabled','scope','day','counts'});self.assertEqual(data['counts'],{'matches_completed':1});self.assertNotIn('Alex Silva',s.path.read_text())
    def test_disable_erases_unsent_counters_and_persists_without_touching_career(self):
        career=self.root/'striker_career.json';career.write_text('private player and career');before=career.read_bytes()
        s=UsageStatistics(self.root);s.set_enabled(True);s.record('matches_completed');s.set_enabled(False)
        self.assertFalse(UsageStatistics(self.root).enabled);self.assertEqual(json.loads(s.path.read_text())['counts'],{});self.assertEqual(career.read_bytes(),before)
    def test_scope_change_requires_new_consent_and_does_not_send_local_history(self):
        s=UsageStatistics(self.root);s.set_enabled(True);s.record('matches_completed')
        remote=UsageStatistics(self.root,'https://stats.example/v1/usage');self.assertFalse(remote.enabled);self.assertEqual(remote.counts,{});self.assertFalse(remote.flush_async())
    def test_invalid_or_oversized_state_fails_closed(self):
        for content in ('[]','null','{broken','x'*16385,'{"schema":true,"enabled":true}', '{"endpoint":"https://evil.example/v1/usage"}'):
            (self.root/'scorer_usage.json').write_text(content);s=UsageStatistics(self.root);self.assertFalse(s.enabled);self.assertEqual(s.counts,{})
    def test_expired_counters_discarded_on_next_open(self):
        s=UsageStatistics(self.root);s.set_enabled(True);s.record('sessions');data=json.loads(s.path.read_text());data['day']=(date.today()-timedelta(days=8)).isoformat();s.path.write_text(json.dumps(data))
        restored=UsageStatistics(self.root);self.assertTrue(restored.enabled);self.assertEqual(restored.counts,{})
    def test_atomic_setting_and_counter_failures_leave_previous_file_and_state(self):
        s=UsageStatistics(self.root);s.set_enabled(True);s.record('sessions');before=s.path.read_bytes()
        with patch('anonymous_stats.os.replace',side_effect=OSError('disk full')):
            self.assertFalse(s.set_enabled(True));self.assertTrue(s.enabled);self.assertFalse(s.record('matches_completed'))
        self.assertEqual(s.path.read_bytes(),before);self.assertEqual(s.counts,{'sessions':1});self.assertFalse(list(self.root.glob('.scorer-usage-*')))
    def test_withdrawal_stops_immediately_if_atomic_save_fails(self):
        s=UsageStatistics(self.root);s.set_enabled(True);s.record('sessions')
        with patch('anonymous_stats.os.replace',side_effect=OSError('disk full')):self.assertTrue(s.set_enabled(False))
        self.assertFalse(s.enabled);self.assertEqual(s.counts,{})
        self.assertFalse(UsageStatistics(self.root).enabled);self.assertFalse(s.record('sessions'))
    def test_successful_upload_contains_only_aggregate_counters(self):
        sent=[];s=UsageStatistics(self.root,'https://stats.example/v1/usage',lambda url,payload:sent.append((url,payload)) or True);s.set_enabled(True);s.record('sessions');s.record('goals_scored',2)
        self.assertTrue(s.flush_async());self.wait(s);self.assertEqual(s.counts,{})
        self.assertEqual(sent[0][1],{'schema':1,'app':'scorer_free','counts':{'sessions':1,'goals_scored':2}})
    def test_offline_failure_keeps_batch_and_new_events_survive_inflight_ack(self):
        s=UsageStatistics(self.root,'https://stats.example/v1/usage',lambda *_:False);s.set_enabled(True);s.record('matches_completed');s.flush_async();self.wait(s);self.assertEqual(s.counts,{'matches_completed':1})
        started=threading.Event();release=threading.Event()
        def sender(*_):started.set();release.wait(2);return True
        s._sender=sender;s.flush_async();self.assertTrue(started.wait(2));s.record('matches_completed');release.set();self.wait(s);self.assertEqual(s.counts,{'matches_completed':1})
    def test_revocation_during_send_cannot_restore_counters(self):
        started=threading.Event();release=threading.Event()
        def sender(*_):started.set();release.wait(2);return True
        s=UsageStatistics(self.root,'https://stats.example/v1/usage',sender);s.set_enabled(True);s.record('sessions');s.flush_async();self.assertTrue(started.wait(2));s.set_enabled(False);release.set();self.wait(s)
        self.assertFalse(s.enabled);self.assertEqual(s.counts,{});self.assertFalse(s.flush_async())
    def test_url_and_payload_validation_rejects_http_redirect_targets_and_pii(self):
        for url in ('http://stats.example/v1/usage','https://a:b@stats.example/v1/usage','https://stats.example/v1/usage?key=x','https://stats.example:444/v1/usage','https://stats.example/elsewhere','https://stats.example/v1/usage#x'):
            self.assertFalse(valid_endpoint(url));self.assertFalse(send_counts(url,{'schema':1,'app':'scorer_free','counts':{'sessions':1}}))
        good={'schema':1,'app':'scorer_free','counts':{'sessions':1}};self.assertTrue(valid_payload(good))
        for bad in [dict(good,player_name='private'),dict(good,app='scorerworld'),dict(good,schema=True),dict(good,counts={'sessions':True}),dict(good,counts={'email':1})]:self.assertFalse(valid_payload(bad))
    def test_world_staging_removes_transport_and_config_free_requires_explicit_endpoint(self):
        w=prepare_edition('world',self.root/'world');f=prepare_edition('free',self.root/'free')
        self.assertFalse((w/'analytics_config.py').exists());self.assertNotIn('urllib',(w/'anonymous_stats.py').read_text());self.assertEqual((f/'analytics_config.py').read_text(),"ENDPOINT = ''\n")
        self.assertFalse((f/'server').exists());self.assertNotIn('SMTP',(f/'anonymous_stats.py').read_text())
        with self.assertRaises(ValueError):prepare_edition('world',self.root/'bad',analytics_endpoint='https://stats.example/v1/usage')
        with self.assertRaises(ValueError):prepare_edition('free',self.root/'bad2',analytics_endpoint='http://stats.example/v1/usage')

    def test_session_end_once_only_after_start_never_on_default_off(self):
        s=UsageStatistics(self.root);self.assertFalse(s.end_session());s.begin_session();self.assertFalse(s.end_session())
        s.set_enabled(True);self.assertTrue(s.end_session());self.assertFalse(s.end_session())
        self.assertEqual(s.counts,{'sessions':1,'sessions_ended':1})
        s.set_enabled(False);self.assertFalse(s.end_session());self.assertEqual(s.counts,{})

    def test_end_flush_during_start_upload_is_not_silently_dropped(self):
        started=threading.Event();release=threading.Event();sent=[]
        def sender(_,payload):
            sent.append(payload);started.set();release.wait(2);return True
        s=UsageStatistics(self.root,'https://stats.example/v1/usage',sender);s.set_enabled(True);s.begin_session();s.flush_async();self.assertTrue(started.wait(2))
        s.end_session();s.flush_async();release.set()
        deadline=time.monotonic()+3
        while len(sent)<2 and time.monotonic()<deadline:threading.Event().wait(.01)
        self.wait(s);self.assertEqual(len(sent),2);self.assertEqual(sent[1]['counts'],{'sessions_ended':1});self.assertEqual(s.counts,{})
