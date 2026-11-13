import unittest
from unittest.mock import patch
from kivy.tests.common import UnitTestTouch
from kivy.clock import Clock
from test_menus import isolated_game,settle
import test_retro_attendance_titles as retro
class TrainingTouchTests(unittest.TestCase):
 def prepare(self,g):
  c=retro.RetroSceneTests().prepare(g);Clock.unschedule(g.update);g.view='training';g.draw();settle();g.start_training();return c
 def test_first_result_tap_bypasses_stale_menu_and_redraws_without_new_shot(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=self.prepare(g);self.assertIsNotNone(g._menu);g._register_miss('MISS!');g.state=g.STATE_RESULT
   touch=UnitTestTouch(*g.center);g.on_touch_down(touch);g.on_touch_up(touch)
   self.assertEqual(c.training_shots_taken,1);self.assertEqual(g.view,'shot');self.assertIn(g.state,(g.STATE_AIMING,g.STATE_BUILDUP));self.assertFalse(g.outcome_registered);self.assertIsNone(g._menu);self.assertEqual(g.attempts,0)
 def test_training_waits_for_tap_and_third_tap_shows_summary_immediately(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=self.prepare(g);g.draw();real_draw=g.draw
   for i in range(3):
    g._register_miss('MISS!');g.state=g.STATE_RESULT;g.ball.active=False;g.draw=lambda:None
    for _ in range(60):g.update(.1)
    g.draw=real_draw;self.assertEqual(c.training_shots_taken,i);self.assertEqual(g.state,g.STATE_RESULT)
    g.on_touch_down(UnitTestTouch(*g.center));self.assertEqual(c.training_shots_taken,i+1)
   self.assertEqual(g.view,'training');self.assertIsNotNone(g._menu);self.assertTrue(c.trained_this_week)
