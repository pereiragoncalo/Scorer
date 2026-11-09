import math,random,unittest
from unittest.mock import patch
from kivy.clock import Clock
from test_menus import isolated_game
import test_retro_attendance_titles as retro
from finishing_balance import NEUTRAL
class FinishingControlsTests(unittest.TestCase):
 def test_situation_controls_add_help_and_keep_earned_bonus_in_full(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=retro.RetroSceneTests().prepare(g);Clock.unschedule(g.update);normal=g._finishing_balance
   for kind in ('penalty','through_ball','cross','first_time'):
    values=[]
    for tuned in (False,True):
     g._finishing_balance=normal if tuned else lambda:NEUTRAL
     g.shot_time_limit=8.;g.current_aim_speed=4.
     with patch.object(c,'finishing_controls',return_value=(.7,1.)):g._start_opportunity(kind,17)
     values.append((g.shot_time_limit,g.current_aim_speed))
    if kind=='first_time':self.assertEqual(values[0],values[1])
    else:
     self.assertGreater(values[1][0],values[0][0]);self.assertLess(values[1][1],values[0][1])
     balance=normal();self.assertAlmostEqual(values[1][0]-.7,(values[0][0]-.7)*balance.decision_time)
   g._finishing_balance=normal
 def test_keeper_help_does_not_change_ballistic_launch_or_distant_headers(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   retro.RetroSceneTests().prepare(g);Clock.unschedule(g.update);normal=g._finishing_balance
   for kind in ('penalty','through_ball','cross','first_time'):
    values=[]
    for tuned in (False,True):
     random.seed(400);g.career.rng.seed(600);g._finishing_balance=normal if tuned else lambda:NEUTRAL;g.current_chance_difficulty='hard';g._prepare_next_shot();g.shot_time_limit=8.;g.current_aim_speed=4.;g._start_opportunity(kind,17);g._update_buildup(g.current_opportunity.duration) if g.current_opportunity.duration else None;g.power=.85
     with patch.object(g,'_play_goal_crowd_sound'):g.shoot(2.8,.5)
     values.append(((g.ball.vx,g.ball.vy,g.ball.vz),g.goalkeeper_reaction))
    self.assertEqual(values[0][0],values[1][0])
    if kind=='first_time':self.assertEqual(values[0][1],values[1][1])
    else:self.assertGreater(values[1][1],values[0][1])
   g._finishing_balance=normal;g.shot_type='header';g.one_on_one=False;g.shot_origin_x=0;g.shot_origin_y=12;self.assertIs(g._finishing_balance(),NEUTRAL)
