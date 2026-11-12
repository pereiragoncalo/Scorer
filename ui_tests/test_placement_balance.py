import random,unittest
from unittest.mock import patch
from kivy.clock import Clock
from test_menus import isolated_game
from test_retro_attendance_titles import RetroSceneTests

class PlacementBalance(unittest.TestCase):
 def test_placed_keeper_tuning_preserves_launch_and_central_reads(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   RetroSceneTests().prepare(g);Clock.unschedule(g.update)
   for x in (0.,-3.2,3.2):
    results=[]
    for tuned in (False,True):
     random.seed(315);g.career.rng.seed(415);g.current_chance_difficulty='hard';g._prepare_next_shot()
     g.shot_type='kick';g.one_on_one=False;g.shot_origin_x=0.;g.shot_origin_y=24.;g.power=.85
     if tuned:g.shoot(x,.5)
     else:
      with patch('finishing_balance.placed_keeper_balance',return_value=(0.,1.,0.)):g.shoot(x,.5)
     results.append(((g.ball.vx,g.ball.vy,g.ball.vz),g.goalkeeper_reaction,g.goalkeeper_read_error))
    self.assertEqual(results[0][0],results[1][0])
    if x==0:self.assertEqual(results[0],results[1])
    else:self.assertGreater(results[1][1],results[0][1])
