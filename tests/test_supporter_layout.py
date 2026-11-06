import unittest
from supporter_layout import AwaySector,FIRST_GOAL_STAIR_X,STAIR_HALF_WIDTH
class SupporterLayout(unittest.TestCase):
    def test_small_visitors_only_corner_large_visitors_until_first_stair(self):
        small=AwaySector(5000);large=AwaySector(60000)
        self.assertTrue(small.contains(40,0,'corner'));self.assertFalse(small.contains(30))
        self.assertTrue(large.contains(40,0,'corner'));self.assertTrue(large.contains(30))
        self.assertFalse(large.contains(FIRST_GOAL_STAIR_X));self.assertFalse(large.contains(20))
        self.assertFalse(small.contains(40,1,'corner'));self.assertFalse(large.contains(40,0,'side'))
        self.assertFalse(AwaySector(20000).extended);self.assertTrue(AwaySector(20001).extended)
    def test_two_files_on_both_flanking_stairs_and_no_training_stewards(self):
        for size in (5000,60000):
            sector=AwaySector(size);posts=sector.stewards(40,-8,1.4)
            self.assertEqual({(p[3],p[4]) for p in posts},{('goal',0),('goal',1),('side',0),('side',1)})
            for x,y,z,flank,file in posts:
                self.assertTrue(sector.stair(x,y,0,flank));self.assertFalse(sector.stair(x,y,1,flank))
            self.assertEqual({p[2] for p in posts},{1.4})
        self.assertEqual(AwaySector(5000,False).stewards(40,-8,1.4),())
        self.assertFalse(AwaySector(5000,False).contains(40,0,'corner'))
