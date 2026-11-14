import math,unittest
from net_drape import RollingReplay
from net_cloth import NetGeometry
from ball_retrieval import Retrieval

ESCAPES=[('box',
  2.65,
  [2.6770968483847573, -0.02, 2.089466619232613],
  [-5.882612624423565, -38.42251622127269, -3.303895733447487]),
 ('veil',
  3.5,
  [-2.7410458827565414, -0.02, 1.536727553386048],
  [9.570275343163438, -35.851114428207566, 5.9197799332099095]),
 ('box',
  1.8,
  [3.221549607274159, -0.02, 0.39977327669802637],
  [0.17424804195761467, -41.91042044237677, 3.6500658859110704]),
 ('box',
  2.65,
  [0.38599772590603987, -0.02, 1.6124538089416163],
  [-14.413234190173156, -38.847936982759485, 3.937609650855121]),
 ('veil',
  3.5,
  [-1.7795721436342091, -0.02, 0.8207508412911482],
  [-8.409983088291622, -40.152085558477275, 1.5172101618876335]),
 ('veil',
  3.5,
  [-0.9215503717664784, -0.02, 0.6067188216999104],
  [10.16671441339431, -40.39244199242675, 1.0881161833341402]),
 ('box',
  1.8,
  [-2.5322936257315827, -0.02, 0.4616717224580625],
  [4.991022176429119, -22.35557419462418, -2.121820863765409])]

class FiniteContainment(unittest.TestCase):
 def test_moving_sheet_cannot_sweep_through_stationary_ball_unnoticed(self):
  from net_contact import ClothContacts
  from net_drape import ReferenceCloth,MATERIALS
  cloth=ReferenceCloth(NetGeometry('box'),MATERIALS['reference'].config,coarse=True)
  mesh=ClothContacts(cloth);previous=[p[:]for p in cloth.positions]
  for p in cloth.positions:
   if p[1]<-2.:p[1]+=1.2
  mesh.refresh(previous);hit=mesh.first((0.,-2.,1.),(0.,-2.,1.),.115)
  self.assertIsNotNone(hit);self.assertEqual(hit['surface'],'back');self.assertLess(hit['t'],1.)

 def test_previous_oblique_and_corner_escapes_remain_in_deformed_goal(self):
  for shape,depth,position,velocity in ESCAPES:
   with self.subTest(shape=shape,depth=depth,position=position):
    g=NetGeometry(shape,depth=depth);r=RollingReplay('reference',height=position[2],geometry=g,coarse=True)
    r.position=position[:];r.velocity=velocity[:];r.ball=tuple(position)
    for _ in range(180):
     before=sum(v*v for v in r.velocity)+19.62*r.ball[2]
     r.one_step()
     self.assertLessEqual(sum(v*v for v in r.velocity)+19.62*r.ball[2],before+1e-6)
     self.assertLessEqual(abs(r.ball[0]),g.width/2+1.4)
     self.assertGreaterEqual(r.ball[1],-g.depth-1.4)
     self.assertLessEqual(r.ball[2],g.height+1.4)
    self.assertTrue(r.hit)

class ActualBallRetrieval(unittest.TestCase):
 def test_follows_moving_ball_and_picks_up_only_at_its_stopped_position(self):
  r=Retrieval((0.,5.),(0.,-.2))
  for _ in range(30):r.advance(.1,(2.,-2.,.115),3.)
  self.assertFalse(r.secured);self.assertEqual(r.phase,'approach')
  for _ in range(20):
   r.advance(.1,(3.,-2.4,.115),0.)
   if r.secured:break
  self.assertEqual(r.position,(3.,-2.4));self.assertTrue(r.secured)
  r.advance(.1,(3.,-2.4,.115),0.);self.assertGreater(r.position[1],-2.4)
 def test_ball_moving_again_cancels_pickup(self):
  r=Retrieval((2.,-2.),(2.,-2.))
  for _ in range(3):r.advance(.1,(2.,-2.,.115),0.)
  self.assertEqual(r.phase,'pickup')
  r.advance(.1,(2.5,-2.,.115),2.)
  self.assertEqual(r.phase,'approach');self.assertFalse(r.secured)
