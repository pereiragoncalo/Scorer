import unittest
from unittest.mock import patch
from test_menus import isolated_game
from opportunity_sequences import KINDS

class FasterDeliveryBall(unittest.TestCase):
 def test_every_opportunity_moves_ball_faster_without_accelerating_receiver_or_keeper(self):
  for context in ('training','match'):
   for kind in (*KINDS,'through_ball'):
    with self.subTest(context=context,kind=kind),isolated_game()as g:
     g.draw=lambda:None;g.shot_context=context;g._start_opportunity(kind,17)
     d=g.current_opportunity;dt=d.duration*.25
     with patch.object(g,'_update_goalkeeper_idle')as keeper:g._update_buildup(dt)
     self.assertEqual(g.state,g.STATE_BUILDUP)
     self.assertAlmostEqual(g.buildup_progress,.25)
     self.assertEqual((g.ball.x,g.ball.y,g.ball.z),d.position(.25*1.05))
     keeper.assert_called_once_with(dt)
     if g.onside_defender is not None and (g._pressure is None or g._pressure.actor is not g.onside_defender):self.assertEqual(g._field_player_position(g.onside_defender),d.chasing_defender(.25))
     g._update_buildup(d.duration*(1/1.05-.25))
     for actual,expected in zip((g.ball.x,g.ball.y,g.ball.z),d.contact):self.assertAlmostEqual(actual,expected)
     self.assertEqual(g.state,g.STATE_BUILDUP)
     g._update_buildup(d.duration*.1)
     self.assertEqual(g.state,g.STATE_AIMING)
     for actual,expected in zip((g.ball.x,g.ball.y,g.ball.z),d.contact):self.assertAlmostEqual(actual,expected)
