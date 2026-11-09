import unittest
from finishing_balance import finishing_balance,NEUTRAL,PENALTY,ONE_ON_ONE
class FinishingBalanceTests(unittest.TestCase):
 def test_penalties_receive_the_largest_help_without_double_counting_duel(self):
  self.assertEqual(finishing_balance('penalty',True,11),PENALTY)
  self.assertGreater(PENALTY.decision_time,ONE_ON_ONE.decision_time);self.assertLess(PENALTY.aim_speed,ONE_ON_ONE.aim_speed);self.assertGreater(PENALTY.reaction_delay,ONE_ON_ONE.reaction_delay)
 def test_headers_fade_smoothly_to_neutral_and_normal_shots_stay_identical(self):
  close=finishing_balance('header',False,7);middle=finishing_balance('header',False,8.5)
  self.assertTrue(1<middle.decision_time<close.decision_time<=1.12);self.assertTrue(close.aim_speed<middle.aim_speed<1)
  for kind in ('kick','free_kick'):
   for distance in (5,10,25):self.assertIs(finishing_balance(kind,False,distance),NEUTRAL)
  for distance in (10,12,25):self.assertIs(finishing_balance('header',False,distance),NEUTRAL)
