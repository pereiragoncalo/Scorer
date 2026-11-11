import tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
from kivy.core.window import Window
from kivy.metrics import Metrics,dp
from kivy.tests.common import UnitTestTouch
from menu_ui import CreationTile
from update_ui import UpdateGate
from test_menus import isolated_game,settle
from tests.test_app_updates import policy

class UpdateGateTests(unittest.TestCase):
 def test_mandatory_overlay_blocks_actions_physics_and_back_and_fits_screens(self):
  old=Window.size;density=Metrics.density
  try:
   with tempfile.TemporaryDirectory() as directory,isolated_game() as g,patch('update_ui.installed_version',return_value=1030003):
    app=SimpleNamespace(root=g,stop=Mock());gate=UpdateGate(app,Path(directory)/'cache');g._update_gate=gate;gate.state.apply(policy());Metrics.density=1.6
    for size in ((1280,591),(640,360),(360,640)):
     Window.size=size;g.size=size;gate.render();settle();popup=gate.popup
     self.assertFalse(popup.auto_dismiss);self.assertTrue(gate.locked)
     before=(g.view,g.elapsed,g.career.rng.getstate());g._activate_ui('new_game');g.update(.1)
     self.assertEqual((g.view,g.elapsed,g.career.rng.getstate()),before);self.assertTrue(g._on_key_down(None,27,None,None,None))
     buttons=[w for w in popup.walk() if isinstance(w,CreationTile)];self.assertEqual(len(buttons),3)
     for button in buttons:
      self.assertGreaterEqual(button.height,dp(48));self.assertGreaterEqual(button.x,popup.x-1);self.assertLessEqual(button.right,popup.right+1)
     with patch('update_ui.open_store') as opened:
      button=next(w for w in buttons if w.text=='UPDATE');touch=UnitTestTouch(*button.center);touch.touch_down();touch.touch_up();settle();opened.assert_called_once()
    gate.state.installed=1030004;gate.render();self.assertFalse(gate.locked);self.assertIsNone(gate.popup);gate.close()
  finally:Window.size=old;Metrics.density=density
 def test_unknown_offline_does_not_present_mandatory_update(self):
  with tempfile.TemporaryDirectory() as directory,isolated_game() as g,patch('update_ui.installed_version',return_value=1030004):
   gate=UpdateGate(SimpleNamespace(root=g,stop=Mock()),Path(directory)/'cache');gate.render();self.assertFalse(gate.locked);self.assertIsNone(gate.popup);gate.close()
