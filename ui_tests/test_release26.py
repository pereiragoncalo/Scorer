import unittest
from unittest.mock import patch
from test_menus import isolated_game
from goal_nets import ROUNDED_STYLE
from net_presentation import ensure,start,ball_position
from game_timing import GAME_SPEED

class FasterPlayRoundedNet(unittest.TestCase):
 def test_aiming_and_player_motion_use_the_same_faster_clock(self):
  with isolated_game()as g:
   g.draw=lambda:None;g.shot_context='match';g._start_opportunity('long_shot',17)
   g.view='shot';g.state=g.STATE_AIMING;g.buildup_progress=1.;g.shot_time_left=4.
   age=g.elapsed;g.update(.1)
   self.assertAlmostEqual(g.elapsed-age,.105);self.assertAlmostEqual(g.shot_time_left,4.-.105)
   g.view='hub';g._career_started=False;age=g.elapsed;g.update(.1);self.assertAlmostEqual(g.elapsed-age,.1)
 def test_rounded_style_uses_rounded_material_and_matching_shared_projection(self):
  with isolated_game()as g:
   g._goal_net_style_override=ROUNDED_STYLE;c=ensure(g)
   self.assertEqual(c.geometry.structure,'rounded');self.assertEqual(c.config.net_slack,.95)
   for v in (0,.25,.5,.75,1):
    self.assertEqual(g._net_point('back',.5,v),g.project(*c.sample('back',.5,v)))
   g.result_text='GOAL!';g.ball.reset(0.,-.02,1.);g.ball.vy=-25.;start(g)
   self.assertEqual(g._net_replay.material.config,c.config)
   g.ball.y=1.;g._net_replay.ball=(0.,-2.,.115)
   self.assertTrue(g._ball_behind_keeper())
