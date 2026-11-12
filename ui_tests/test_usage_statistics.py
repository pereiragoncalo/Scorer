import json,unittest
from unittest.mock import patch
from kivy.uix.label import Label
from main import StrikerApp
from test_menus import isolated_game,settle

class UsageStatisticsUITests(unittest.TestCase):
    def test_opt_in_is_separate_pin_guarded_and_stop_requires_no_pin(self):
        with isolated_game(saved=True) as g:
            before=g.career.save_path.read_bytes()
            g._activate_ui('splash_continue');g._activate_ui('privacy');g.draw();settle()
            self.assertFalse(g.usage.enabled);self.assertEqual(g.usage.counts,{})
            self.assertIn('Optional usage statistics',{w.text for w in g.walk() if isinstance(w,Label)})
            g._activate_ui('enable_usage_stats');self.assertEqual(g.view,'family')
            g._safety_draft=dict(birth='1980-01-01',pin='123456',confirm='123456')
            g._activate_ui('adult_setup');g._activate_ui('safety_back')
            g._safety_draft['analytics_pin']='000000';g._activate_ui('enable_usage_stats')
            self.assertFalse(g.usage.enabled)
            g._safety_draft['analytics_pin']='123456';g._activate_ui('enable_usage_stats')
            self.assertTrue(g.usage.enabled);self.assertEqual(g.usage.counts,{'sessions':1})
            self.assertFalse(g.leaderboard.enabled)
            g._safety_draft={};g._activate_ui('disable_usage_stats')
            self.assertFalse(g.usage.enabled);self.assertEqual(g.usage.counts,{})
            self.assertEqual(g.career.save_path.read_bytes(),before)
    def test_real_game_hooks_count_once_without_names_or_ids(self):
        with isolated_game() as g:
            g.usage.set_enabled(True);g._activate_ui('splash_continue');g._activate_ui('new_game');g._activate_ui('save_profile','Private Example')
            g._activate_ui('accept_offer',g.career.offers[0]);g._activate_ui('accept_offer',g.career.offers[0])
            g._activate_ui('coach');g._activate_ui('coach_focus',g.career.coach_focus_options()[0]);g._activate_ui('coach_complete')
            g._activate_ui('training');g._activate_ui('training_start')
            for _ in range(3):g.result_text='GOAL!';g._advance_after_shot()
            g.view='hub';g.start_career_match();g._record_player_match_goal();g._finish_career_match();g._finish_career_match()
            counts=g.usage.counts
            for key in ('sessions','new_careers','trainings_completed','matches_completed','goals_scored'):self.assertEqual(counts[key],1,key)
            data=g.usage.path.read_text();self.assertNotIn('Private Example',data);self.assertNotIn(g.career.club_name,data)
            self.assertEqual(set(json.loads(data)['counts']),set(counts))
    def test_world_startup_agreement_enables_statistics_but_not_sharing(self):
        from anonymous_stats import create_statistics
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            with patch('anonymous_stats.APP_NOTICE_REQUIRED',True):
                g.usage=create_statistics(True,g.career.save_path.parent,endpoint='')
            g._activate_ui('splash_continue');self.assertEqual(g.view,'data_notice')
            g._activate_ui('notice_continue');self.assertEqual(g.view,'start')
            self.assertTrue(g.usage.enabled);self.assertFalse(g.leaderboard.enabled)
            self.assertEqual(g.usage.counts,{'sessions':1})
    def test_known_save_load_failures_use_fixed_numeric_events_only(self):
        with isolated_game(corrupt=True) as g:
            g.usage.set_enabled(True);g._activate_ui('splash_continue');g._activate_ui('load_game');self.assertEqual(g.usage.counts['load_failures'],1)
            g._career_started=True
            with patch.object(g.career,'save',return_value=False):StrikerApp.on_pause(type('App',(),{'root':g,'_check_app_update':lambda _:None})())
            self.assertEqual(g.usage.counts['save_failures'],1)
            g.usage.set_enabled(False)
            with patch.object(g.career,'save',return_value=False):StrikerApp.on_stop(type('App',(),{'root':g,'_check_app_update':lambda _:None})())
            self.assertEqual(g.usage.counts,{})

    def test_background_does_not_end_session_normal_stop_counts_once(self):
        with isolated_game() as g:
            g.usage.set_enabled(True);g._activate_ui('splash_continue')
            app=type('App',(),{'root':g,'_check_app_update':lambda _:None})()
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
                StrikerApp.on_stop(type('App',(),{'root':g,'_check_app_update':lambda _:None})())
                self.assertEqual(g.usage.counts['sessions_ended'],1)

    def test_open_before_splash_then_background_reopen_counts_two(self):
        with isolated_game() as g:
            g.usage.set_enabled(True);app=type('App',(),{'root':g,'_check_app_update':lambda _:None})()
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
