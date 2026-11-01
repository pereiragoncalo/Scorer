import unittest
from defensive_difficulty import defensive_profile

class DefensiveDifficultyTests(unittest.TestCase):
    def test_every_promotion_improves_reaction_footwork_and_high_save(self):
        profiles=[defensive_profile(t) for t in (5,4,3,2,1)]
        for lower,higher in zip(profiles,profiles[1:]):
            self.assertLess(higher.reaction_low,lower.reaction_low);self.assertLess(higher.reaction_high,lower.reaction_high)
            self.assertLess(higher.reading_error,lower.reading_error);self.assertGreater(higher.step_speed,lower.step_speed)
            self.assertGreater(higher.acceleration,lower.acceleration);self.assertGreater(higher.jump_boost,lower.jump_boost)
            self.assertLess(higher.lane_jitter,lower.lane_jitter)
    def test_finite_bounded_ability_and_national_team_uses_top_level(self):
        self.assertEqual(defensive_profile(20),defensive_profile(5));self.assertEqual(defensive_profile(-1),defensive_profile(1))
        self.assertEqual(defensive_profile(5,True),defensive_profile(1))
        for tier in range(1,6):
            p=defensive_profile(tier);self.assertTrue(.10<=p.reaction_low<p.reaction_high<=.35)
            self.assertLessEqual(p.step_speed,4.5);self.assertLessEqual(p.defenders,5)
