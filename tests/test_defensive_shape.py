import math,unittest,random
from defensive_shape import block,shift
from opportunity_sequences import make_delivery
class DefensiveShape(unittest.TestCase):
 def test_four_defenders_three_midfielders_keep_width_depth_and_receiving_space(self):
  for x in (-7.,-2.,0.,3.,7.):
   for y in (6.5,9.6,14.,22.):
    shape=block(x,y);back=[p for p in shape if p[2]=='defence'];mid=[p for p in shape if p[2]=='midfield']
    self.assertEqual((len(back),len(mid)),(4,3));self.assertLess(max(p[1]for p in back)-min(p[1]for p in back),.3)
    self.assertGreater(min(p[1]for p in mid)-max(p[1]for p in back),4.)
    self.assertTrue(all(b[0]-a[0]>=6.9 for a,b in zip(back,back[1:])))
    self.assertGreaterEqual(min(math.hypot(px-x,py-y)for px,py,_ in shape),1.8)
 def test_collective_shift_has_no_rng_or_shape_distortion(self):
  before=random.getstate();delivery=make_delivery('long_cross',12);shape=block(*delivery.contact[:2]);dx,dy=shift(delivery,.3)
  shifted=[(x+dx,y+dy)for x,y,_ in shape]
  self.assertEqual(random.getstate(),before);self.assertEqual(shift(delivery,1.),(0.,0.))
  self.assertAlmostEqual(math.dist(shifted[0],shifted[6]),math.dist(shape[0][:2],shape[6][:2]))
