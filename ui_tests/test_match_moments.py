"""Native integration: real scoreboard, stable touch notice and save history."""
import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.uix.label import Label
from menu_ui import MatchNotice
from test_menus import isolated_game, settle


class MatchMomentUI(unittest.TestCase):
    def start(self,g):
        g.career.load();g.career.last_training_week=g.career.week;g.career.attend_coach_meeting();g.start_career_match()

    def test_timing_does_not_change_ai_goals_career_rng_or_easy_index(self):
        with isolated_game(saved=True) as g:
            g.career.load();g.career.last_training_week=g.career.week;g.career.attend_coach_meeting()
            state=g.career.rng.getstate()
            with patch('main.late_opportunity',side_effect=lambda minutes,*a:list(minutes)):
                g.start_career_match()
            baseline=(list(g.match_goal_events),g.match_easy_chance_index,g.career.rng.getstate(),len(g.match_chance_minutes))
            g.career.rng.setstate(state);g.start_career_match()
            self.assertEqual((g.match_goal_events,g.match_easy_chance_index,g.career.rng.getstate(),len(g.match_chance_minutes)),baseline)

    def test_late_clock_score_goal_counted_once_and_history_survives_reload(self):
        with isolated_game(saved=True) as g:
            self.start(g)
            g.match_first_stoppage=4;g.match_half=2;g.match_minute=88
            g.match_chance_minutes=[89];g.match_chance_index=0;g.match_goal_events=[]
            g.match_home_score,g.match_away_score=(0,1) if g._player_match_is_home() else (1,0)
            g.match_stakes={};g._update_career_match(1)
            self.assertEqual(g.match_moment,'equaliser');self.assertEqual(g.match_clock_text,'85:00')
            g._begin_pending_chance();g._record_player_match_goal();g._record_player_match_goal()
            self.assertEqual(g.match_player_goals,1)
            self.assertEqual(g.match_moments,[dict(kind='equaliser',minute=85,outcome='goal')])
            g._finish_career_match()
            self.assertEqual(g.career.fixture_history[-1]['moments'],g.match_moments)
            g.career.load();self.assertEqual(g.career.fixture_history[-1]['moments'],g.match_moments)

    def test_miss_and_future_goal_do_not_rewrite_the_moment(self):
        with isolated_game(saved=True) as g:
            self.start(g);g.match_half=2;g.match_first_stoppage=2;g.match_minute=88
            g.match_chance_minutes=[89];g.match_chance_index=0;g.match_goal_events=[(90,'home')]
            g.match_home_score=g.match_away_score=0;g.match_stakes={};g._update_career_match(1)
            self.assertEqual(g.match_moment,'lead');self.assertEqual(g.match_goal_event_index,0)
            g._begin_pending_chance();g.result_text='SAVED';g._advance_after_shot()
            self.assertEqual(g.match_moments,[dict(kind='lead',minute=87,outcome='missed')])
            self.assertEqual(g.match_player_goals,0)

    def test_all_languages_small_phone_notice_stays_attached_and_button_reachable(self):
        old=Window.size
        try:
            Window.size=(320,240)
            with patch('edition.WORLD_BUILD',True),isolated_game(saved=True) as g:
                g.career.accept_starting_offer(g.career.offers[0]);g.career.attend_coach_meeting();g.career.last_training_week=g.career.week;g.career.attend_coach_meeting();g.start_career_match()
                g.size=(320,240);g.awaiting_chance=True;g.match_moment='equaliser'
                for lang in ('en','pt','es','de','it','ko','ja','zh','vi'):
                    g.i18n.choose(lang);g.draw();settle()
                    notice=next(w for w in g.walk() if isinstance(w,MatchNotice))
                    g.draw();self.assertIn(notice,list(g.walk()))
                    self.assertGreaterEqual(notice.button.height,48)
                    self.assertGreaterEqual(notice.button.y,0)
                    self.assertLessEqual(notice.button.top,g.height)
                    self.assertTrue(any(w.text==g.i18n.tr('LATE EQUALISER') for w in notice.body.walk() if isinstance(w,Label)), (lang, [w.text for w in notice.body.walk() if isinstance(w,Label)]))
        finally:
            Window.size=old
