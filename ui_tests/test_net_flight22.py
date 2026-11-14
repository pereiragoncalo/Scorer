import copy,unittest
from test_menus import isolated_game
from net_presentation import ball_position,advance
class ContinuousPostGoalFlight(unittest.TestCase):
 def test_goal_starts_at_unmodified_ball_and_does_not_double_advance_first_step(self):
  with isolated_game() as g:
   g.draw=lambda:None;g.shot_context='training';g.ball.reset(0,-.03,1.);g.ball.vx,g.ball.vy,g.ball.vz=0,-20.,1.
   before=copy.deepcopy(vars(g.ball));g.outcome_registered=False;g._register_goal()
   self.assertEqual(ball_position(g),(0,-.03,1.));advance(g,1/120)
   self.assertEqual(ball_position(g),(0,-.03,1.));advance(g,1/120)
   self.assertLess(ball_position(g)[1],-.03);self.assertEqual(vars(g.ball),before)
   self.assertEqual(g.goals,1);self.assertFalse(g._net_replay.contacts)
