import copy,unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.metrics import Metrics,dp
from kivy.tests.common import UnitTestTouch
from kivy.uix.scrollview import ScrollView
from kivy.core.text import Label as CoreLabel
from test_menus import isolated_game,settle
from training_ui import TrainingScreen

class TrainingLocker(unittest.TestCase):
 def test_responsive_localized_room_keeps_controls_and_career_state(self):
  old=Window.size;density=Metrics.density
  try:
   with patch('edition.WORLD_BUILD',True),isolated_game(saved=True) as g:
    c=g.career
    if c.club is None:c.accept_starting_offer(c.offers[0])
    c.attend_coach_meeting();g._career_started=True
    g.view='training';before=copy.deepcopy(g.career.development);rng=g.career.rng.getstate()
    for lang in ('en','pt','de','ja'):
     g.i18n.choose(lang)
     for w,h,d in ((1280,591,1.6),(960,540,1.6),(640,360,1.)):
      Metrics.density=d;Window.size=(w,h);g.size=(w,h);g.draw();settle();p=g._menu.body
      self.assertIsInstance(p,TrainingScreen);self.assertTrue(p.player.canvas.shader.success)
      self.assertTrue(p.room.texture);self.assertTrue(p.player.texture)
      self.assertFalse(any(isinstance(v,ScrollView) for v in p.walk()))
      for v in (p.start,p.help,p.back):
       self.assertGreaterEqual(v.height,dp(48));self.assertGreaterEqual(v.y,p.y-1);self.assertLessEqual(v.top,p.top+1);self.assertGreaterEqual(v.x,p.x-1);self.assertLessEqual(v.right,p.right+1)
      for v in (p.focus,p.progress,p.skill,p.energy):
       self.assertGreaterEqual(v.y,p.y-1);self.assertLessEqual(v.top,p.top+1)
       measured=CoreLabel(text=v.text,text_size=(v.width,None),font_name=v.font_name,font_size=v.font_size);measured.refresh()
       self.assertLessEqual(measured.texture.size[1],v.height+2,v.text)
    self.assertEqual(g.career.development,before);self.assertEqual(g.career.rng.getstate(),rng)
  finally:Window.size=old;Metrics.density=density
 def test_start_and_resume_use_the_existing_reserved_training_session(self):
  with patch('edition.WORLD_BUILD',True),isolated_game(saved=True) as g:
   c=g.career
   if c.club is None:c.accept_starting_offer(c.offers[0])
   c.attend_coach_meeting();g._career_started=True
   g.view='training';g.draw();settle();p=g._menu.body
   t=UnitTestTouch(*p.start.center);t.touch_down();t.touch_up();settle()
   self.assertEqual(g.view,'shot');self.assertEqual(g.shot_context,'training');self.assertEqual(g.career.training_session_week,g.career.week)
   g.career.record_training_shot(False,False);g.view='training';g.draw();settle();p=g._menu.body
   self.assertEqual(p.shots_bar.value,1);self.assertIn('RESUME',p.start.text)
   p.start.dispatch('on_release');self.assertEqual(g.career.training_shots_taken,1)

 def test_save_failure_stays_in_locker_without_consuming_training(self):
  with patch('edition.WORLD_BUILD',True),isolated_game(saved=True) as g:
   c=g.career
   if c.club is None:c.accept_starting_offer(c.offers[0])
   c.attend_coach_meeting();g._career_started=True;g.view='training';g.draw();settle()
   before=(c.training_session_week,c.training_shots_taken,c.stamina)
   with patch.object(c,'save',return_value=False):g._menu.body.start.dispatch('on_release')
   settle();self.assertEqual(g.view,'training');self.assertEqual((c.training_session_week,c.training_shots_taken,c.stamina),before)
   p=g._menu.body;self.assertTrue(p.error_label);self.assertGreaterEqual(p.start.y,p.y)
