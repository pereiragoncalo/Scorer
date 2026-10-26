import json,unittest
from unittest.mock import patch
from kivy.uix.label import Label
from main import StrikerApp
from test_menus import isolated_game,settle

class UsageStatisticsUITests(unittest.TestCase):
    def test_privacy_choice_is_explicit_and_separate_from_career(self):
        with isolated_game(saved=True) as g:
            before=g.career.save_path.read_bytes();self.assertFalse(g.usage.enabled)
            g._activate_ui('splash_continue');g._activate_ui('privacy');g.draw();settle()
            labels={w.text for w in g.walk() if isinstance(w,Label)}
            self.assertIn('ALLOW USAGE STATS',labels);self.assertTrue(any('nothing is sent' in t for t in labels))
            g._activate_ui('enable_usage_stats');g.draw();settle();self.assertTrue(g.usage.enabled)
            self.assertEqual(g.usage.counts,{'sessions':1});self.assertEqual(g.career.save_path.read_bytes(),before)
            g._activate_ui('disable_usage_stats');self.assertFalse(g.usage.enabled);self.assertEqual(g.usage.counts,{})
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
    def test_default_off_and_world_never_collect_or_expose_toggle(self):
        with isolated_game(saved=True) as g:
            g._activate_ui('splash_continue');g._activate_ui('load_game');StrikerApp.on_pause(type('App',(),{'root':g})())
            self.assertFalse(g.usage.path.exists())
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            g.view='privacy';g.draw();settle();g._activate_ui('enable_usage_stats')
            self.assertFalse(g.usage.enabled)
            self.assertNotIn('ALLOW USAGE STATS',{w.text for w in g.walk() if isinstance(w,Label)})
            self.assertFalse((g.career.save_path.parent/'scorer_usage.json').exists())
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
