import unittest
from unittest.mock import patch
import net_drape
from test_menus import isolated_game
from net_presentation import ensure,start
from net_render import NetRenderer

class NetSpeedIntegration(unittest.TestCase):
 def test_goal_handoff_reuses_existing_cloth_and_contact_mesh(self):
  with isolated_game() as g:
   cloth=ensure(g);g.ball.reset(0.,-.03,1.);g.ball.vy=-25.
   with patch('net_drape.ReferenceCloth',wraps=net_drape.ReferenceCloth) as construction:
    start(g)
   construction.assert_not_called()
   self.assertIs(g._net_replay.cloth,cloth)
   self.assertIs(g._net_replay.mesh.cloth,cloth)
   self.assertEqual(g._net_replay.velocity,[0.,-25.,0.])
 def test_moving_ball_overlay_does_not_reproject_unchanged_net(self):
  with isolated_game() as g:
   cloth=ensure(g);r=NetRenderer(cloth,'hexagon');calls=[]
   def project(*p):calls.append(p);return g.project(*p)
   camera=(g.pos,g.size,g.desktop_windows)
   r.sync(project,camera,(0.,-.1,1.));count=len(calls)
   r.sync(project,camera,(0.,-.4,1.));self.assertEqual(len(calls),count)
   cloth.contact={'normal':(-1.,0.,0.),'radius':.115}
   r.sync(project,camera,(-3.5,-.4,1.));r.sync(project,camera,(-3.5,-.7,1.))
   self.assertEqual(len(calls),count)
