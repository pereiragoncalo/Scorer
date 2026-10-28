import unittest
from career import GOAL_WIDTH,GOAL_HEIGHT,VEIL_PATH_LENGTH,VEIL_SLOPE_LENGTH
from shot_geometry import GoalGeometry
from world_promotion import campaign_message,WINDOWS_MESSAGES

class GoalGeometryTests(unittest.TestCase):
    def test_original_dimensions_and_net_path_remain_exact(self):
        g=GoalGeometry.for_profile(False)
        self.assertEqual((g.width,g.height),(GOAL_WIDTH,GOAL_HEIGHT))
        self.assertEqual((g.veil_path_length,g.veil_slope_length),(VEIL_PATH_LENGTH,VEIL_SLOPE_LENGTH))
    def test_windows_profile_is_moderately_larger_without_mutating_shared_constants(self):
        g=GoalGeometry.for_profile(True)
        self.assertAlmostEqual(g.width/GOAL_WIDTH,1.12);self.assertAlmostEqual(g.height/GOAL_HEIGHT,1.1)
        self.assertGreater(g.veil_path_length,VEIL_PATH_LENGTH)
        self.assertEqual((GOAL_WIDTH,GOAL_HEIGHT),(7.32,2.44))
    def test_windows_placeholder_rotation_stays_local_bounded_and_retains_world(self):
        self.assertEqual(len(WINDOWS_MESSAGES),4);self.assertIn('YOUR COMPANY HERE',WINDOWS_MESSAGES);self.assertIn('SCORER WORLD',WINDOWS_MESSAGES)
        self.assertEqual({campaign_message(0,i,desktop=True) for i in range(11)},set(WINDOWS_MESSAGES))
        self.assertEqual(campaign_message(0,desktop=True),campaign_message(100,desktop=True))
        self.assertNotEqual(campaign_message(0),campaign_message(0,desktop=True))
