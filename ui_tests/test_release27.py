import unittest
from unittest.mock import patch
from test_menus import isolated_game
from shot_trajectory import launch_velocity
from goal_nets import COIMBRA_PRETO_UID,ROUNDED_STYLE,stadium_style

class OpportunityLaunch(unittest.TestCase):
 def test_training_and_match_launch_only_ball_faster(self):
  for context in ('training','match'):
   for kind in ('penalty','long_shot','cross'):
    with self.subTest(context=context,kind=kind),isolated_game()as g:
     g.draw=lambda:None;g.shot_context=context;g._start_opportunity(kind,17)
     g.view='shot';g.state=g.STATE_AIMING;g.buildup_progress=1.;g.shot_time_left=4.
     with patch('shot_trajectory.launch_velocity',wraps=launch_velocity)as solver,patch.object(g,'_shot_flight_time',return_value=.9),patch.object(g.career,'low_finish_speed',return_value=1.):
      g.shoot(1.,1.)
     self.assertTrue(solver.called);self.assertAlmostEqual(solver.call_args.args[2],.9/1.05)
     self.assertEqual(g.state,g.STATE_SHOT)
