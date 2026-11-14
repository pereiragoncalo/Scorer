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
  # Softness is measured at peak contact, not a prescribed resting position.
  self.assertLess(slack.peak_ball[1],tight.peak_ball[1])
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
     # A slow high shot can touch the finite sagged roof before the rear.
     self.assertGreaterEqual(contact_height,r.radius)
     self.assertLessEqual(contact_height,r.geometry.height)
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
 def test_strong_hex_demo_shot_touches_side_before_rear_and_stays_inside(self):
  r=RollingReplay.strong_side_shot();height_at_side=None
  for _ in range(600):
   r.one_step()
   if 'left' in r.contacts and height_at_side is None:height_at_side=r.ball[2]
   for i in r.ground_anchors:self.assertEqual(r.cloth.positions[i],r.cloth.rest[i])
  self.assertLess(r.first_contacts['left'],r.first_contacts['back'])
  self.assertGreater(height_at_side,1.)
  self.assertLess(height_at_side,1.4)
  self.assertLess(r.ball[1],-2.)
  self.assertEqual(r.ball[2],r.radius)
  self.assertLess(math.hypot(*r.velocity[:2]),.03)
 def test_unloaded_reference_hangs_down_without_outward_pockets(self):
  from net_drape import ReferenceCloth,MATERIALS
  from net_cloth import NetGeometry
  for shape in ('box','veil'):
   for coarse in (False,True):
    c=ReferenceCloth(NetGeometry(shape),MATERIALS['reference'].config,coarse)
    sag_peak=0.
    for surface,(us,vs,grid) in c.grids.items():
     for j,v in enumerate(vs):
      for i,u in enumerate(us):
       base=c.geometry.point(surface,u,v);rest=c.rest[grid[j][i]]
       self.assertAlmostEqual(rest[0],base[0],places=6)
       self.assertAlmostEqual(rest[1],base[1],places=6)
       self.assertLessEqual(rest[2],base[2]+1e-6)
       sag_peak=max(sag_peak,base[2]-rest[2])
    self.assertGreater(sag_peak,.1)
    self.assertEqual(c.displacement,0.)
    self.assertFalse(c.active)

 def test_stationary_penetration_does_not_inflate_the_net(self):
  r=RollingReplay('reference',height=.115);r.position=[-r.geometry.width/2-.025,-1.,r.radius];r.velocity=[0.,0.,0.]
  before=[p[:] for p in r.cloth.positions]
  self.assertIsNotNone(r._contact('left'))
  self.assertEqual(r.cloth.positions,before)
  self.assertEqual(r.cloth.previous,before)
 def test_free_flight_does_not_move_cloth_before_real_contact(self):
  r=RollingReplay.strong_side_shot()
  for _ in range(600):
   r.one_step()
   if not r.hit:self.assertEqual(r.cloth.displacement,0.)
  self.assertLess(r.first_contacts['left'],r.first_contacts['back'])
 def test_ball_pushes_only_the_strands_in_direct_contact(self):
  r=RollingReplay('reference',height=1.)
  r.position=[-r.geometry.width/2+.08,-1.,1.];r.velocity=[-6.,-10.,0.]
  u,v=r.geometry.uv_at('left',r.position)
  touched={i for i,w in r.cloth.weights('left',u,v) if w and not r.cloth.pinned[i]}
  before=[p[:] for p in r.cloth.positions]
  self.assertIsNotNone(r._contact('left'))
  moved={i for i,(a,b) in enumerate(zip(before,r.cloth.positions)) if a!=b}
  self.assertTrue(moved);self.assertLessEqual(moved,touched)
