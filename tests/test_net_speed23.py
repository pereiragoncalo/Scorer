import math,unittest
from net_cloth import NetGeometry
from net_drape import RollingReplay

class NetTravelSpeed(unittest.TestCase):
 def test_glancing_side_contact_keeps_longitudinal_travel(self):
  for shape in ('box','veil'):
   for speed in (12.,18.,30.):
    with self.subTest(shape=shape,speed=speed):
     r=RollingReplay('reference',height=.6,coarse=True,geometry=NetGeometry(shape))
     r.position=[-r.geometry.width/2+.12,-.12,.6];r.velocity=[-1.,-speed,0.];r.ball=tuple(r.position)
     for _ in range(6):
      before=r.ball;expected=-r.velocity[1]*r.STEP;r.one_step()
      if r.contacts==['left']:
       self.assertGreater(before[1]-r.ball[1],expected*.85)
 def test_free_flight_keeps_speed_until_real_mesh_contact(self):
  r=RollingReplay('reference',height=1.,coarse=True,geometry=NetGeometry('box'))
  r.position=[0.,-.03,1.];r.velocity=[0.,-30.,0.];r.ball=tuple(r.position)
  for _ in range(6):
   y=r.ball[1];speed=-r.velocity[1];r.one_step()
   self.assertFalse(r.contacts);self.assertAlmostEqual(y-r.ball[1],speed*r.STEP)
