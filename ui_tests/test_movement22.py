import unittest
from test_menus import isolated_game
from retro_sprites import Pose
class ActualMovement(unittest.TestCase):
 def test_stationary_run_is_idle_and_running_clock_tracks_distance(self):
  with isolated_game() as g:
   r=g._retro_renderer();g.elapsed=0.;pose=Pose('RUN',0.)
   self.assertEqual(r.motion_pose(g,'test',pose,(0.,0.,0.)).state,'IDLE')
   g.elapsed=.1;self.assertEqual(r.motion_pose(g,'test',Pose('RUN',.1),(0.,0.,0.)).state,'IDLE')
   g.elapsed=.2;moving=r.motion_pose(g,'test',Pose('RUN',.2),(0.,-.35,0.))
   self.assertEqual(moving.state,'RUN');self.assertAlmostEqual(moving.age,.1);self.assertEqual(moving.view,'back')
   g.elapsed=.3;self.assertEqual(r.motion_pose(g,'test',Pose('RUN',.3),(0.,-.35,0.)).state,'IDLE')
 def test_open_play_has_cohesive_back_four_and_three_midfielders(self):
  with isolated_game() as g:
   g.draw=lambda:None;g.shot_context='match';g._start_opportunity('long_shot',17)
   defenders=[p for p in g.field_players if p.team=='defender']
   self.assertEqual(sum(getattr(p,'formation_line',None)=='defence'for p in defenders),4)
   self.assertEqual(sum(getattr(p,'formation_line',None)=='midfield'for p in defenders),3)
   g.state=g.STATE_AIMING
   positions=[g._field_player_position(p)for p in defenders];g.elapsed+=.1
   self.assertEqual(positions,[g._field_player_position(p)for p in defenders])
