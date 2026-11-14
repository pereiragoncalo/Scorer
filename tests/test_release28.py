import unittest
from shot_trajectory import delivery_ball_progress,OPPORTUNITY_BALL_SPEED
from opportunity_sequences import make_delivery,KINDS

class WholeOpportunityBallSpeed(unittest.TestCase):
 def test_delivery_progress_is_five_percent_faster_and_clamps_at_reception(self):
  self.assertEqual(OPPORTUNITY_BALL_SPEED,1.05)
  for p in (0.,.1,.25,.5,.9):self.assertAlmostEqual(delivery_ball_progress(p),p*1.05)
  for p in (1/1.05,1.,2.):self.assertEqual(delivery_ball_progress(p),1.)
  self.assertEqual(delivery_ball_progress(-1),0.)
 def test_every_delivery_keeps_original_endpoint_and_path(self):
  for kind in (*KINDS,'through_ball'):
   d=make_delivery(kind,17)
   self.assertEqual(d.position(delivery_ball_progress(1/1.05)),d.contact)
   self.assertEqual(d.position(delivery_ball_progress(.5)),d.position(.525))
