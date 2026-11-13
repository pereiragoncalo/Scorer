"""Development experiment only: no APK build or production net changes."""
import math,unittest
from tools.net_lab.rolling_contact import RollingReplay

class RollingExperiment(unittest.TestCase):
 def test_side_then_corner_roll_and_material_difference(self):
  simulations=[]
  initial=[]
  for kind in ('tight','slack'):
   r=RollingReplay(kind);initial.append((r.ball,r.velocity[:]))
   for _ in range(600):
    previous=r.ball;r.one_step()
    self.assertTrue(all(math.isfinite(x) for x in (*r.ball,*r.velocity)))
    self.assertLess(math.dist(previous,r.ball),.085)
    self.assertEqual(r.ball[2],r.radius)
    for index in r.ground_anchors:
     self.assertTrue(r.cloth.pinned[index])
     self.assertEqual(r.cloth.positions[index],r.cloth.rest[index])
     self.assertEqual(r.cloth.previous[index],r.cloth.rest[index])
   self.assertLess(r.first_contacts['left'],r.first_contacts['back'])
   self.assertLess(math.hypot(*r.velocity[:2]),.01)
   self.assertLess(r.ball[1],0)
   simulations.append(r)
  self.assertEqual(initial[0],initial[1])
  tight,slack=simulations
  self.assertGreater(slack.peak,tight.peak)
  self.assertLess(slack.peak_ball[1],-slack.geometry.depth+.2)
  self.assertLess(slack.ball[1],tight.ball[1]-.6)
 def test_fixed_step_repeats_at_different_capture_rates(self):
  states=[]
  for fps in (30,60):
   r=RollingReplay('slack')
   for _ in range(fps*2):r.advance(1/fps)
   states.append((r.ball,r.velocity,r.cloth.positions))
  self.assertEqual(states[0],states[1])
 def test_airborne_matrix_contacts_and_fixed_ground(self):
  for height in (.22,1.1,2.05):
   for speed in (4.,9.,18.):
    with self.subTest(height=height,speed=speed):
     r=RollingReplay('sagged',speed,height);contact_height=None
     for _ in range(240):
      r.one_step()
      self.assertTrue(all(math.isfinite(x) for x in (*r.ball,*r.velocity)))
      for i in r.ground_anchors:
       self.assertEqual(r.cloth.positions[i],r.cloth.rest[i])
       self.assertEqual(r.cloth.previous[i],r.cloth.rest[i])
      if 'back' in r.contacts and contact_height is None:contact_height=r.ball[2]
     self.assertIsNotNone(contact_height)
     self.assertLess(abs(contact_height-height),.20)
 def test_soft_ties_have_fixed_pole_ends_and_bounded_net_end_yield(self):
  r=RollingReplay('sagged',18.,2.05);c=r.cloth
  endpoints=tuple(tie[1] for tie in c.tethers)
  for _ in range(240):
   r.one_step()
   self.assertEqual(tuple(tie[1] for tie in c.tethers),endpoints)
   for index,endpoint,length in c.tethers:
    self.assertFalse(c.pinned[index])
    self.assertLessEqual(math.dist(c.positions[index],c.rest[index]),c.TIE_YIELD+1e-9)
    self.assertLessEqual(math.dist(c.positions[index],endpoint),length+c.TIE_YIELD+1e-9)
  self.assertGreater(c.tie_peak,.001)
  # The suspended cloth can form a deep pocket while ties give only slightly.
  self.assertGreater(r.peak,c.tie_peak*5)
 def test_reference_moves_a_broad_patch_instead_of_a_local_spike(self):
  involved=[]
  for variant in ('sagged','reference'):
   r=RollingReplay(variant,18.,1.1);largest=0
   for _ in range(240):
    r.one_step()
    largest=max(largest,sum(math.dist(p,q)>.15 for p,q in zip(r.cloth.positions,r.cloth.rest)))
   involved.append(largest)
  self.assertGreater(involved[1],involved[0]*1.8)
 def test_reference_matrix_preserves_ground_and_tie_anchors(self):
  for height in (.22,1.1,2.05):
   for speed in (4.,9.,18.):
    with self.subTest(height=height,speed=speed):
     r=RollingReplay('reference',speed,height);c=r.cloth
     fixed={i:c.rest[i][:] for i,pinned in enumerate(c.pinned) if pinned}
     ends=tuple(tie[1] for tie in c.tethers)
     for _ in range(360):
      r.one_step()
      self.assertTrue(all(math.isfinite(x) for x in (*r.ball,*r.velocity)))
      for i,point in fixed.items():
       self.assertEqual(c.positions[i],point)
       self.assertEqual(c.previous[i],point)
      self.assertEqual(tuple(tie[1] for tie in c.tethers),ends)
      for i,endpoint,length in c.tethers:
       self.assertLessEqual(math.dist(c.positions[i],c.rest[i]),c.TIE_YIELD+1e-9)
     self.assertIn('back',r.first_contacts)
 def test_reference_load_is_shared_across_the_side_back_seam(self):
  r=RollingReplay('reference',12.,1.1);c=r.cloth
  u,v=r.geometry.uv_at('back',(-3.,-r.geometry.depth,1.1))
  support=c.load_weights(c.weights('back',u,v))
  self.assertAlmostEqual(sum(w for _,w in support),1.)
  self.assertTrue(all(w>0 and not c.pinned[i] for i,w in support))
  side={i for row in c.grids['left'][2] for i in row}
  back={i for row in c.grids['back'][2] for i in row}
  participating={i for i,_ in support}
  self.assertTrue(participating & (side-back))
  self.assertTrue(participating & (back-side))
