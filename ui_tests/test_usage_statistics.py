import json,unittest
from unittest.mock import patch
from kivy.uix.label import Label
from main import StrikerApp
from test_menus import isolated_game,settle

class UsageStatisticsUITests(unittest.TestCase):
    def test_automatic_stats_are_disclosed_and_have_no_disable_control(self):
        from anonymous_stats import create_statistics
        with isolated_game(saved=True) as g:
            with patch('anonymous_stats.APP_STATS_MANDATORY',True):
                g.usage=create_statistics(False,g.career.save_path.parent,endpoint='')
            before=g.career.save_path.read_bytes();self.assertTrue(g.usage.enabled)
            g._activate_ui('splash_continue');g._activate_ui('privacy');g.draw();settle()
            labels={w.text for w in g.walk() if isinstance(w,Label)}
            self.assertIn('Automatic usage statistics',labels)
            self.assertNotIn('ALLOW USAGE STATS',labels);self.assertNotIn('DISABLE AND ERASE STATS',labels)
            self.assertEqual(g.usage.counts,{'sessions':1})
            g._activate_ui('disable_usage_stats');self.assertTrue(g.usage.enabled)
            self.assertFalse(g.usage.set_enabled(False));self.assertTrue(g.usage.enabled)
            self.assertEqual(g.career.save_path.read_bytes(),before)
    def test_real_game_hooks_count_once_without_names_or_ids(self):
        with isolated_game() as g:
            g.usage.set_enabled(True);g._activate_ui('splash_continue');g._activate_ui('new_game');g._activate_ui('save_profile','Private Example')
            g._activate_ui('accept_offer',g.career.offers[0]);g._activate_ui('accept_offer',g.career.offers[0])
            g._activate_ui('training');g._activate_ui('training_start')
            for _ in range(3):g.result_text='GOAL!';g._advance_after_shot()
            g.view='hub';g.start_career_match();g._record_player_match_goal();g._finish_career_match();g._finish_career_match()
            counts=g.usage.counts
            for key in ('sessions','new_careers','trainings_completed','matches_completed','goals_scored'):self.assertEqual(counts[key],1,key)
            data=g.usage.path.read_text();self.assertNotIn('Private Example',data);self.assertNotIn(g.career.club_name,data)
            self.assertEqual(set(json.loads(data)['counts']),set(counts))
    def test_world_is_automatic_but_public_name_sharing_stays_optional(self):
        from anonymous_stats import create_statistics
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            with patch('anonymous_stats.APP_STATS_MANDATORY',True):
                g.usage=create_statistics(True,g.career.save_path.parent,endpoint='')
            g._activate_ui('splash_continue');self.assertEqual(g.usage.counts['sessions'],1)
            self.assertTrue(g.usage.enabled);self.assertFalse(g.leaderboard.enabled)
            g.view='privacy';g.draw();settle()
            self.assertNotIn('DISABLE AND ERASE STATS',{w.text for w in g.walk() if isinstance(w,Label)})
    def test_known_save_load_failures_use_fixed_numeric_events_only(self):
        with isolated_game(corrupt=True) as g:
            g.usage.set_enabled(True);g._activate_ui('splash_continue');g._activate_ui('load_game');self.assertEqual(g.usage.counts['load_failures'],1)
            g._career_started=True
            with patch.object(g.career,'save',return_value=False):StrikerApp.on_pause(type('App',(),{'root':g})())
            self.assertEqual(g.usage.counts['save_failures'],1)
            g.usage.set_enabled(False)
            with patch.object(g.career,'save',return_value=False):StrikerApp.on_stop(type('App',(),{'root':g})())
            self.assertEqual(g.usage.counts,{})

    def test_background_does_not_end_session_normal_stop_counts_once(self):
        with isolated_game() as g:
            g.usage.set_enabled(True);g._activate_ui('splash_continue')
            app=type('App',(),{'root':g})()
            StrikerApp.on_pause(app);self.assertNotIn('sessions_ended',g.usage.counts)
            StrikerApp.on_stop(app);StrikerApp.on_stop(app)
            self.assertEqual(g.usage.counts['sessions'],1);self.assertEqual(g.usage.counts['sessions_ended'],1)

    def test_confirmed_exit_records_and_flushes_end_before_app_stop(self):
        with isolated_game(saved=True) as g:
            g.usage.set_enabled(True);g._activate_ui('splash_continue')
            calls=[]
            app=type('App',(),{'stop':lambda _:calls.append(('stop',dict(g.usage.counts)))})()
            with patch('main.App.get_running_app',return_value=app),patch.object(g.usage,'flush_async',side_effect=lambda:calls.append(('flush',dict(g.usage.counts)))):
                with patch.object(g.career,'save',return_value=False):g._confirm_exit()
                self.assertEqual(calls,[]);self.assertNotIn('sessions_ended',g.usage.counts)
                g._confirm_exit()
                self.assertEqual([c[0] for c in calls],['flush','stop'])
                self.assertTrue(all(c[1]['sessions_ended']==1 for c in calls))
                StrikerApp.on_stop(type('App',(),{'root':g})())
                self.assertEqual(g.usage.counts['sessions_ended'],1)

    def test_open_before_splash_then_background_reopen_counts_two(self):
        with isolated_game() as g:
            g.usage.set_enabled(True);app=type('App',(),{'root':g})()
            StrikerApp.on_start(app)
            try:
                self.assertEqual(g.view,'splash');self.assertEqual(g.usage.counts['sessions'],1)
                g._activate_ui('splash_continue');self.assertEqual(g.usage.counts['sessions'],1)
                StrikerApp.on_pause(app);StrikerApp.on_resume(app)
                self.assertEqual(g.usage.counts['sessions'],2)
                StrikerApp.on_resume(app);self.assertEqual(g.usage.counts['sessions'],2)
                with patch.object(g.usage,'flush_async') as send:
                    StrikerApp._flush_usage(app);send.assert_called_once()
            finally:StrikerApp.on_stop(app)
            self.assertTrue(app._usage_flush_event.is_triggered==0)
