import tempfile,unittest
from pathlib import Path
from kivy.clock import Clock
from kivy.core.window import Window
from test_menus import settle
from tools.net_lab.main import Lab

class LabControls(unittest.TestCase):
 def test_real_controls_repeat_parameters_ab_json_pause_step_and_debug(self):
  app=Lab();root=app.build();Window.add_widget(root)
  try:
   settle();app.sliders['force'].value=22;app.sliders['net_slack'].value=.31;app.fire()
   self.assertEqual(app.replay.cloth.config.net_slack,.31);self.assertEqual(app.replay.force,22)
   app.store('a');app.sliders['net_stiffness'].value=70;app.fire();app.store('b')
   app.recall('a');self.assertEqual(app.replay.cloth.config.net_slack,.31);self.assertEqual(app.replay.cloth.config.net_stiffness,24)
   app.recall('b');self.assertEqual(app.replay.cloth.config.net_stiffness,70)
   app.replay.paused=True;tick=app.replay.tick;app.replay.advance(.1);self.assertEqual(app.replay.tick,tick)
   app.replay.one_step();self.assertEqual(app.replay.tick,tick+1)
   app.scene.debug_mesh=True;app.scene.draw();app.scene.mesh='hexagon';app.scene.draw()
   with tempfile.TemporaryDirectory() as directory:
    app.path.text=str(Path(directory)/'reference.json');app.save();self.assertTrue(Path(app.path.text).is_file())
    app.sliders['force'].value=35;app.load();self.assertEqual(app.replay.force,22)
   app.reset_net();self.assertTrue(app.replay.paused);self.assertEqual(app.replay.cloth.displacement,0)
   app.scene.draw();self.assertIs(app.scene.renderer.cloth,app.scene.replay.cloth)
  finally:Clock.unschedule(app.update);Window.remove_widget(root)
