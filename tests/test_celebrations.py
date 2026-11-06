import unittest,random,math
from types import SimpleNamespace
from celebrations import crowd_jump,decisive_now,GoalCelebration
class Celebrations(unittest.TestCase):
 def test_people_have_independent_jump_traces_and_never_consume_rng(self):
  before=random.getstate();seeds=[(i*2654435761)&0xffffffff for i in range(100)]
  heights=[crowd_jump(.4,s) for s in seeds]
  self.assertGreater(len(set(round(h,3) for h in heights)),20)
  self.assertTrue(any(h==0 for h in heights));self.assertTrue(any(h>1 for h in heights))
  traces={tuple(round(crowd_jump(t,s),2) for t in (.2,.4,.8,1.,1.4)) for s in seeds}
  self.assertGreater(len(traces),90);self.assertEqual(random.getstate(),before)
 def test_only_observed_late_goahead_goals_are_decisive(self):
  g=SimpleNamespace(match_stakes={},match_home_score=1,match_away_score=0,match_minute=86,match_first_stoppage=1,match_half=2,_player_match_is_home=lambda:True)
  self.assertTrue(decisive_now(g));g.match_minute=30;self.assertFalse(decisive_now(g))
  g.match_minute=86;g.match_away_score=1;self.assertFalse(decisive_now(g))
  g.match_home_score=2;g.match_stakes={'late_allowed':False};self.assertFalse(decisive_now(g))
  g.match_stakes={'kind':'final'};g.match_minute=73;self.assertTrue(decisive_now(g))
 def test_run_slide_decelerates_then_rise_and_hugs_stay_at_own_crowd(self):
  c=GoalCelebration(0,'away',True,(0,10),(33,-1.9),(37,-5.5),4,(30.5,-1.))
  self.assertEqual(c.actor(2)[1],'RUN');self.assertEqual(c.actor(4.2)[1],'KNEE_SLIDE')
  self.assertGreater(math.dist(c.actor(4)[0],c.actor(4.3)[0]),math.dist(c.actor(4.7)[0],c.actor(5)[0]))
  self.assertEqual(c.actor(5.2)[1],'FALL');self.assertEqual(c.actor(6)[1],'HUG')
  for index in range(1,4):
   position,state,age=c.actor(c.duration-.1,index)
   self.assertEqual(state,'HUG');self.assertLess(math.dist(position,c.target),.6)
