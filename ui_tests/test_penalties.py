import unittest
from unittest.mock import patch
from kivy.uix.label import Label
from menu_ui import MatchNotice
from test_menus import isolated_game,settle
class Penalties(unittest.TestCase):
    def test_penalties_are_chosen_and_announced_before_playing_the_chance(self):
        with isolated_game() as g:
            c=g.career;c.accept_starting_offer(c.offers[0]);c.last_training_week=c.week;found=0
            with patch.object(c,'chance_count',return_value=3):
                for seed in range(80):
                    c.rng.seed(80000+seed);g.start_career_match();idx=g.match_penalty_chance_index
                    if idx<0:continue
                    found+=1;self.assertNotEqual(idx,g.match_easy_chance_index)
                    g.match_chance_index=idx;g.awaiting_chance=True;g.view='match';g.draw();settle()
                    self.assertTrue(any(isinstance(w,Label) and w.text=='You have been chosen to take the penalty.' for w in g.walk()))
                    g._begin_pending_chance();self.assertEqual(g.shot_type,'penalty')
                    self.assertEqual((g.shot_origin_x,g.shot_origin_y),(0,11));self.assertEqual(g.field_players,[])
            self.assertGreater(found,5)
