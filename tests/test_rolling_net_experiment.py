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
