import copy,unittest
from test_menus import isolated_game
from goal_nets import ROUNDED_STYLE
from net_presentation import start,ensure,ball_position

class RestoredNetInGame(unittest.TestCase):
 def test_training_goal_returns_net_to_original_before_ball_collection(self):
  with isolated_game()as g:
   g._goal_net_style_override=ROUNDED_STYLE;g.view='shot';g.shot_context='training';g.state=g.STATE_RESULT;g.result_text='GOAL!'
   c=ensure(g);original=copy.deepcopy(c.positions)
   g.ball.reset(-2.8,-.02,1.);g.ball.vx=-4.;g.ball.vy=-25.;before=vars(g.ball).copy()
   start(g);r=g._net_replay
   for _ in range(100):g.update(.1)
   self.assertIs(g._net_replay,r);self.assertTrue(r.hit);self.assertGreater(r.peak,.1)
   self.assertFalse(getattr(r,'collected',False));self.assertTrue(r.sleeping)
   self.assertEqual(c.positions,original);self.assertTrue(r.mesh.inside(ball_position(g)))
   self.assertEqual(vars(g.ball),before);g.draw()
