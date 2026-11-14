import math,unittest
from net_cloth import NetGeometry
from net_drape import RollingReplay
class FiniteNetContacts(unittest.TestCase):
 def test_triangle_retains_fast_low_medium_high_shots_without_energy_gain(self):
  for depth in (2.65,3.5):
   for speed in (8.,35.):
    for height in (.115,1.,2.05):
     with self.subTest(depth=depth,speed=speed,height=height):
      r=RollingReplay('reference',speed,height,geometry=NetGeometry('veil',depth=depth),coarse=True)
      r.position=[2.9,.05,height];r.velocity=[2.5,-speed,0.];r.ball=tuple(r.position)
      entered=False
      for _ in range(240):
       before=sum(v*v for v in r.velocity)+2*9.81*r.ball[2]
       r.one_step();after=sum(v*v for v in r.velocity)+2*9.81*r.ball[2]
       self.assertLessEqual(after,before+1e-6)
       entered|=r.ball[1]<-.15
       if entered:self.assertLess(r.ball[1],.01)
       self.assertTrue(all(math.isfinite(v)for v in (*r.ball,*r.velocity)))
      self.assertTrue(r.hit)
 def test_no_phantom_roof_on_ground_hem_or_side_above_triangular_mesh(self):
  r=RollingReplay('reference',height=.8,geometry=NetGeometry('veil'),coarse=True)
  r.position=[0.,-2.45,.8];r.velocity=[0.,-5.,0.]
  self.assertIsNone(r._contact('back'))
  r.position=[r.geometry.width/2-.02,-2.,2.];r.velocity=[5.,0.,0.]
  self.assertIsNone(r._contact('right'))
 def test_free_flight_has_no_sheet_contact_or_impulse_until_visible_mesh(self):
  r=RollingReplay('reference',height=1.,geometry=NetGeometry('veil'),coarse=True)
  r.position=[0.,.05,1.];r.velocity=[0.,-12.,0.]
  for _ in range(5):
   r.one_step();self.assertFalse(r.contacts);self.assertEqual(r.cloth.displacement,0.)
