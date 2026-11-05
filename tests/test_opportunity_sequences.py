import random,unittest,math
from opportunity_sequences import KINDS,plan_opportunities,make_delivery
from career import BALL_RADIUS,HEADER_BALL_HEIGHT
class Deliveries(unittest.TestCase):
    def test_deterministic_plan_preserves_count_slots_and_rng(self):
        before=random.getstate()
        for count in range(4):
            plan=plan_opportunities(count,0,1,'fixture')
            self.assertEqual(len(plan),count)
            self.assertEqual(plan,plan_opportunities(count,0,1,'fixture'))
            if count:self.assertEqual(plan[0],'through_ball')
            if count>1:self.assertEqual(plan[1],'penalty')
        self.assertEqual(random.getstate(),before)
        self.assertEqual(plan_opportunities(1,0,0,13),('penalty',))
    def test_all_five_kinds_appear_without_duplicate_normal_slots(self):
        found=set()
        for seed in range(50):
            plan=plan_opportunities(3,-1,-1,seed)
            self.assertEqual(len(set(plan)),3);found.update(plan)
        self.assertEqual(found,set(KINDS))
    def test_path_is_continuous_above_ground_and_ends_at_exact_contact(self):
        for kind in (*KINDS,'through_ball','penalty'):
            for seed in range(20):
                d=make_delivery(kind,seed)
                self.assertEqual(d.position(0),d.points[0]);self.assertEqual(d.position(1),d.contact)
                self.assertEqual(d.position(10),d.contact);self.assertEqual(d.position(-1),d.points[0])
                self.assertEqual(d.mirrored().mirrored(),d)
                self.assertAlmostEqual(d.contact[2],HEADER_BALL_HEIGHT if d.shot_type=='header' else BALL_RADIUS)
                for i in range(101):
                    p=d.position(i/100)
                    self.assertTrue(all(math.isfinite(x) for x in p));self.assertGreaterEqual(p[2],BALL_RADIUS-1e-9)
                    if i:self.assertLess(math.dist(p,d.position((i-1)/100)),1.)
                if kind=='free_kick':self.assertGreater(d.contact[1],16.5)
                if kind=='penalty':self.assertEqual(d.duration,0)
    def test_cross_rises_and_cutback_moves_away_from_byline(self):
        cross=make_delivery('cross',7);self.assertGreater(cross.position(.5)[2],2.5)
        cut=make_delivery('cutback',7);self.assertLess(cut.position(.5)[1],cut.contact[1])
        rebound=make_delivery('rebound',7);self.assertLess(rebound.position(.5)[1],rebound.contact[1])
