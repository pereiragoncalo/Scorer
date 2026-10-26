import unittest
from domestic_rules import table_zones

class StandingZoneTests(unittest.TestCase):
    def test_priority_pyramid_boundaries_and_legacy_playoff_places(self):
        z=table_zones(4,18,{1,2,3,4},simplified=False)
        self.assertEqual(z.promotion,(1,2,3));self.assertEqual(z.playoff,(4,5,6,7));self.assertFalse(z.relegation)
        middle=table_zones(2,18,{1,2,3,4},simplified=False)
        self.assertEqual(middle.relegation,(17,18));self.assertEqual(middle.at(7),'playoff');self.assertEqual(middle.at(8),'')
        top=table_zones(1,18,{1,2,3,4},simplified=False)
        self.assertFalse(top.promotion);self.assertFalse(top.playoff);self.assertEqual(top.relegation,(17,18))
        self.assertTrue(z.provisional)
    def test_two_tier_fallback_has_three_places_and_no_playoffs(self):
        for tier in (1,2):
            z=table_zones(tier,12,{1,2},simplified=True)
            self.assertFalse(z.playoff);self.assertFalse(z.provisional)
            self.assertEqual(z.promotion,(1,2,3) if tier==2 else ())
            self.assertEqual(z.relegation,(10,11,12) if tier==1 else ())
        archived=table_zones(4,12,{1,2},simplified=True)
        self.assertTrue(archived.archived);self.assertFalse(any(archived.at(p) for p in range(1,13)))
    def test_ranges_do_not_overlap_or_mutate_active_tiers(self):
        for count in (6,8,12,18,20,24):
            for tier in (1,2,3,4):
                active={1,2,3,4};z=table_zones(tier,count,active,simplified=False)
                places=z.promotion+z.playoff+z.relegation
                self.assertEqual(len(places),len(set(places)));self.assertTrue(all(1<=p<=count for p in places))
                self.assertEqual(active,{1,2,3,4});self.assertEqual(z.at(0),'');self.assertEqual(z.at(count+1),'')
        z=table_zones(1,18,{1},simplified=False)
        self.assertFalse(z.promotion+z.playoff+z.relegation)
