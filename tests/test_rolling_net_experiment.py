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
   self.assertLess(r.first_contacts['left'],r.first_contacts['back'])
   self.assertLess(math.hypot(*r.velocity[:2]),.01)
   self.assertLess(r.ball[1],0)
   simulations.append(r)
  self.assertEqual(initial[0],initial[1])
  tight,slack=simulations
  self.assertGreater(slack.peak,tight.peak*4)
  self.assertLess(slack.peak_ball[1],-slack.geometry.depth+.2)
  self.assertLess(slack.ball[1],tight.ball[1]-.6)
 def test_fixed_step_repeats_at_different_capture_rates(self):
  states=[]
  for fps in (30,60):
   r=RollingReplay('slack')
   for _ in range(fps*2):r.advance(1/fps)
   states.append((r.ball,r.velocity,r.cloth.positions))
  self.assertEqual(states[0],states[1])
