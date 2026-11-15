import unittest
from net_drape import RollingReplay
from net_cloth import NetGeometry
class ContactRefit(unittest.TestCase):
 def test_partial_refit_matches_full_refit_through_fast_impacts(self):
  for shape in ('box','veil','rounded'):
   with self.subTest(shape=shape):
    args=dict(variant='rounded' if shape=='rounded' else 'reference',height=1.,coarse=True,geometry=NetGeometry(shape,depth=3.5))
    fast,full=RollingReplay(**args),RollingReplay(**args)
    full.mesh.refresh_contacts=lambda nodes:full.mesh.refresh()
    for r in (fast,full):r.position=[2.9,.03,1.];r.velocity=[2.,-30.,0.]
    for _ in range(120):
     fast.one_step();full.one_step()
     self.assertEqual((fast.ball,fast.velocity,fast.contacts),(full.ball,full.velocity,full.contacts))
     self.assertEqual(fast.cloth.positions,full.cloth.positions)
