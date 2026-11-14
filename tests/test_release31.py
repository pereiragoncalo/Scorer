import math,unittest
from net_cloth import NetGeometry
from net_drape import RollingReplay

class ReturnToOriginalWithBallInside(unittest.TestCase):
 def test_restoration_completes_before_collection_for_low_high_and_both_sides(self):
  for height,speed,vx,x in ((.115,25,0,0),(1.,25,0,0),(2.,35,0,0),(1.,25,-4,-2.8),(1.,25,4,2.8),(2.1,20,-6,-2.8),(2.1,20,6,2.8)):
   with self.subTest(height=height,vx=vx):
    r=RollingReplay('rounded',height=height,geometry=NetGeometry('rounded',depth=3.5),coarse=True)
    r.position=[x,-.02,height];r.velocity=[vx,-speed,0.];r.ball=tuple(r.position)
    original=[p[:]for p in r.cloth.rest]
    for _ in range(960):
     energy=sum(v*v for v in r.velocity)+19.62*r.ball[2];r.one_step()
     self.assertLessEqual(sum(v*v for v in r.velocity)+19.62*r.ball[2],energy+1e-6)
     if r.sleeping:self.assertLessEqual(r.cloth.displacement,1e-6)
     if r.ball[1]<-.02:self.assertTrue(r.mesh.inside(r.ball))
    self.assertTrue(r.hit);self.assertGreater(r.peak,.1)
    self.assertTrue(r.cloth.retain_pocket) # caught-ball friction; no collection yet
    self.assertFalse(getattr(r,'collected',False))
    self.assertTrue(r.sleeping);self.assertEqual(r.cloth.positions,original)
    self.assertLess(r.ball[1],-1.);self.assertAlmostEqual(r.ball[2],r.radius)
    self.assertLess(math.sqrt(sum(v*v for v in r.velocity)),.05)
