import unittest
from unittest.mock import patch
from kivy.clock import Clock
from kivy.tests.common import UnitTestTouch
from kivy.uix.label import Label
from opportunity_sequences import KINDS,TEXT
from test_menus import isolated_game,settle
class OpportunityScenes(unittest.TestCase):
    def sign(self,g):
        c=g.career;c.accept_starting_offer(c.offers[0]);c.last_training_week=c.week
        g.start_career_match();Clock.unschedule(g.update);g.view='shot';g.shot_context='match';g.current_chance_difficulty='hard'
        g._prepare_next_shot();g.shot_time_limit=g.shot_time_left=4.;return c
    def test_all_deliveries_freeze_on_arrival_before_timer_and_input(self):
        for kind in (*KINDS,'through_ball'):
            with self.subTest(kind=kind),isolated_game() as g:
                self.sign(g);g._start_opportunity(kind,70);g.draw();settle()
                score=(g.match_home_score,g.match_away_score,g.attempts,g.goals,g.match_player_misses)
                minute=g.match_minute;clock=g.shot_time_left;start=(g.ball.x,g.ball.y,g.ball.z)
                self.assertEqual(g.state,g.STATE_BUILDUP)
                self.assertLessEqual(sum(p.team=='defender' for p in g.field_players+g.buildup_actors),5)
                g.shoot(2.,1.)
                self.assertEqual(g.state,g.STATE_BUILDUP)
                g.on_touch_down(UnitTestTouch(*g.center));self.assertEqual(g.attempts,score[2])
                g._on_key_down(None,114,0,'r',[]);self.assertEqual(g.state,g.STATE_BUILDUP)
                g.update(.1);self.assertEqual(g.shot_time_left,clock)
                if kind!='free_kick':self.assertNotEqual((g.ball.x,g.ball.y,g.ball.z),start)
                while g.state==g.STATE_BUILDUP:g.update(.1)
                self.assertEqual((g.ball.x,g.ball.y,g.ball.z),g.current_opportunity.contact)
                self.assertEqual(g.shot_time_left,clock);self.assertFalse(g.ball.active)
                self.assertEqual((g.match_home_score,g.match_away_score,g.attempts,g.goals,g.match_player_misses),score)
                self.assertEqual(g.match_minute,minute)
                actor=g.field_players[0] if g.field_players else g.buildup_actors[0]
                pose=g._field_player_position(actor);keeper=g.goalkeeper_x
                g.update(.1);self.assertAlmostEqual(g.shot_time_left,clock-.1)
                self.assertEqual(g._field_player_position(actor),pose);self.assertEqual(g.goalkeeper_x,keeper)
                g.shoot(2.8,1.);self.assertEqual(g.state,g.STATE_SHOT);self.assertEqual(g.attempts,score[2]+1)
    def test_match_notice_announces_planned_move_and_clears_after_shot(self):
        with isolated_game() as g:
            self.sign(g);g.match_opportunities=('cutback',);g.match_chance_index=0
            g.match_penalty_chance_index=g.match_easy_chance_index=-1;g.awaiting_chance=True;g.view='match';g.draw();settle()
            self.assertTrue(any(isinstance(w,Label) and w.text==TEXT['cutback'][0] for w in g.walk()))
            g._begin_pending_chance();self.assertEqual(g.current_opportunity.kind,'cutback')
            self.assertEqual(g.state,g.STATE_BUILDUP)
            g.result_text='SAVED';g._advance_after_shot();self.assertEqual(g.view,'match')
            self.assertIsNone(g.current_opportunity);self.assertEqual(g.buildup_actors,[])
    def test_training_has_no_build_up_or_extra_players_and_penalty_is_preserved(self):
        with isolated_game() as g:
            self.sign(g);g._start_opportunity('penalty',8)
            self.assertEqual(g.state,g.STATE_AIMING);self.assertEqual((g.ball.x,g.ball.y),(0,11));self.assertEqual(g.field_players,[])
            g.shot_context='training';g._prepare_next_shot()
            self.assertEqual(g.state,g.STATE_AIMING);self.assertIsNone(g.current_opportunity)
            self.assertEqual(g.field_players,[]);self.assertEqual(g.buildup_actors,[])
    def test_onside_defender_is_visible_at_release_and_stays_behind_at_reception(self):
        with isolated_game() as g:
            self.sign(g)
            for seed in range(8):
                g._start_opportunity('through_ball',seed)
                defender=g.onside_defender
                self.assertIsNotNone(defender);self.assertIn(defender,g.field_players)
                self.assertEqual(defender.team,'defender')
                released=g._field_player_position(defender)
                self.assertLess(released[1],g.shot_origin_y+2)
                while g.state==g.STATE_BUILDUP:g.update(.1)
                chased=g._field_player_position(defender)
                self.assertGreater(chased[1],g.shot_origin_y+2)
                self.assertTrue(g.one_on_one)
                self.assertEqual(g.attempts,0)
            g._start_opportunity('penalty',9)
            self.assertIsNone(g.onside_defender);self.assertEqual(g.field_players,[])
