import unittest
from finishing_balance import finishing_balance,NEUTRAL,PENALTY,ONE_ON_ONE,OPEN_PLAY,HEADER
class FinishingBalanceTests(unittest.TestCase):
 def test_penalties_receive_the_largest_help_without_double_counting_duel(self):
  self.assertEqual(finishing_balance('penalty',True,11),PENALTY)
  self.assertGreater(PENALTY.decision_time,ONE_ON_ONE.decision_time);self.assertLess(PENALTY.aim_speed,ONE_ON_ONE.aim_speed);self.assertGreater(PENALTY.reaction_delay,ONE_ON_ONE.reaction_delay)
 def test_headers_fade_to_header_base_and_normal_shots_use_open_play_aid(self):
  close=finishing_balance('header',False,7);middle=finishing_balance('header',False,8.5)
  self.assertTrue(HEADER.decision_time<middle.decision_time<close.decision_time<=HEADER.decision_time*1.12);self.assertTrue(close.aim_speed<middle.aim_speed<HEADER.aim_speed)
  for kind in ('kick','free_kick'):
   for distance in (5,10,25):self.assertIs(finishing_balance(kind,False,distance),OPEN_PLAY)
  for distance in (10,12,25):self.assertIs(finishing_balance('header',False,distance),HEADER)

 def test_corner_help_is_symmetric_progressive_and_leaves_other_shots_alone(self):
  from finishing_balance import placed_keeper_balance
  centre=placed_keeper_balance('kick',0,3.66);self.assertEqual(centre,(0.,1.,0.))
  left=placed_keeper_balance('kick',-3.2,3.66);right=placed_keeper_balance('kick',3.2,3.66)
  self.assertEqual(left[:2],right[:2]);self.assertEqual(left[2],-right[2])
  self.assertTrue(0<right[0]<=.06);self.assertTrue(1<right[1]<=1.35);self.assertLess(right[2],0)
  self.assertLess(placed_keeper_balance('kick',2.0,3.66)[0],right[0])
  for kind in ('penalty','header'):
   self.assertEqual(placed_keeper_balance(kind,3.2,3.66),centre)
  self.assertEqual(placed_keeper_balance('kick',4,3.66),centre)
