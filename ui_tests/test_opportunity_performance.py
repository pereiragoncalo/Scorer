import unittest
from unittest.mock import patch
from test_menus import isolated_game
from net_presentation import ensure,start
from net_contact import ClothContacts

class OpportunityPerformance(unittest.TestCase):
 def test_static_stands_reuse_gpu_buffers_until_geometry_rebuilt(self):
  with isolated_game() as g:
   g.view='shot';g.size=(1280,720);g.draw();group=g._stand_draw_group
   for _ in range(4):g.draw();self.assertIs(g._stand_draw_group,group)
   self.assertEqual(g.canvas.children.count(group),1)
   g.size=(1200,600);g.draw();self.assertIsNot(g._stand_draw_group,group)
   self.assertNotIn(group,g.canvas.children)
 def test_goal_reuses_prepared_collision_topology_without_stale_contacts(self):
  with isolated_game() as g:
   cloth=ensure(g);mesh=cloth._contact_mesh;mesh.candidates={}
   with patch('net_contact.ClothContacts',side_effect=AssertionError('goal topology allocation')):
    start(g)
   self.assertIs(g._net_replay.mesh,mesh);self.assertIsNone(mesh.candidates)
 def test_goal_audio_only_plays_preloaded_sound(self):
  from unittest.mock import Mock
  with isolated_game() as g:
   g.shot_context='match';g._goal_crowd_sound=Mock()
   with patch('kivy.core.audio.SoundLoader.load',side_effect=AssertionError('goal audio IO')):
    g._play_goal_crowd_sound()
   g._goal_crowd_sound.play.assert_called_once()
 def test_audio_worker_finishes_file_before_loading_on_kivy_thread(self):
  from goal_audio import preload
  with isolated_game() as g:
   pending=[]
   with patch('goal_audio.Thread') as worker,patch('kivy.clock.Clock.schedule_once',side_effect=lambda callback,delay:pending.append(callback)),patch('kivy.core.audio.SoundLoader.load') as load:
    preload(g);worker.return_value.start.assert_called_once()
    worker.call_args.kwargs['target']();load.assert_not_called()
    self.assertEqual(len(pending),1);pending[0](0)
    load.assert_called_once();self.assertIs(g._goal_crowd_sound,load.return_value)
