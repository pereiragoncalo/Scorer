import tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from test_menus import isolated_game,settle
from update_ui import UpdateGate
from tests.test_app_updates import policy

class RefinementsTests(unittest.TestCase):
 def test_update_check_is_nonblocking_white_splash_hint_and_only_requirement_opens_modal(self):
  with isolated_game() as g,tempfile.TemporaryDirectory() as directory,patch('update_ui.installed_version',return_value=1030005):
   gate=UpdateGate(SimpleNamespace(root=g,stop=Mock()),Path(directory)/'cache');g.view='splash';gate.state.checking=True;gate.render();settle()
   self.assertFalse(gate.locked);self.assertIsNone(gate.popup);self.assertIsNotNone(gate.hint);self.assertEqual(tuple(gate.hint.color),(1,1,1,1));self.assertLess(gate.hint.x,30);self.assertLess(gate.hint.y,30)
   g.view='hub';gate._hint();self.assertEqual(gate.hint.opacity,0)
   gate.state.apply(policy(1030006,1030006));gate.render();self.assertTrue(gate.locked);self.assertIsNotNone(gate.popup);self.assertIsNone(gate.hint);gate.close()
 def test_player_milestones_and_controls_fit_without_any_scroll(self):
  old=Window.size
  try:
   for size in ((1280,591),(640,360)):
    Window.size=size
    with isolated_game() as g:
     c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True;g._profile_return='hub';g.view='profile';g.size=size;g.draw();settle()
     panel=g._menu.body
     self.assertFalse(any(isinstance(w,ScrollView) for w in panel.walk()))
     for w in (panel.name,panel.actions,panel.objectives,panel.contract_info):
      self.assertGreaterEqual(w.y,-1);self.assertLessEqual(w.top,g.height+1)
     text=' '.join(w.text for w in panel.walk() if isinstance(w,Label));self.assertIn('CAREER STATS',text);self.assertIn('Monthly salary',text);self.assertNotIn('/',text)
  finally:Window.size=old
 def test_new_player_portrait_has_no_unowned_home_or_car(self):
  from estate_portrait import EstatePortrait
  with isolated_game() as g:
   self.assertEqual(g.career.life['owned'],{})
   portrait=EstatePortrait(g.career);self.assertIsNone(portrait.house);self.assertIsNone(portrait.car);portrait.size=(640,260);portrait.render()
