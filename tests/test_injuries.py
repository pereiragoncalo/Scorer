import copy,os,tempfile,unittest
from unittest.mock import patch
from career import CareerMode
import injuries
from career_life import clean
class Access:
 def has_world_access(self):return True
class InjuryTests(unittest.TestCase):
 def setUp(self):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);p=patch.dict(os.environ,STRIKER_SAVE_DIR=t.name);p.start();self.addCleanup(p.stop)
  self.c=CareerMode(autoload=False);self.c.accept_starting_offer(self.c.offers[0]);self.c.attend_coach_meeting()
 def test_probability_bounds_and_distribution(self):
  c=self.c;c.stamina=20;self.assertAlmostEqual(injuries.probability(c),.01);c.stamina=0;self.assertAlmostEqual(injuries.probability(c),.03);c.stamina=10
  count=0;durations=set();names=set();state=c.rng.getstate()
  for i in range(10000):
   c.life['injury_games']=0;c.fixture_history=[dict(date=str(i),competition='test',home='home',away='away')];injuries.complete(c,False)
   if injuries.active(c):count+=1;durations.add(c.life['injury_games']);names.add(c.life['injury_name'])
  self.assertTrue(150<count<250,count);self.assertEqual(durations,{1,2,3});self.assertGreater(len(names),3);self.assertEqual(c.rng.getstate(),state)
 def test_saved_absence_blocks_practice_and_recovers_per_fixture(self):
  c=self.c;c.life.update(injury_name='Calf strain',injury_games=2);self.assertTrue(c.save());self.assertTrue(c.load());self.assertFalse(c.begin_training());self.assertEqual(c.complete_training(3),0);self.assertEqual(c.chance_count(),0)
  stats=(c.matches,c.goals,c.morale,c.stamina,c.coach_trust,list(c.form_goals));negative=c.press_state['negative_run']
  for left in (1,0):
   token,h,a=c.next_match();c.finish_match(h,a,0,0,forced_score=(1,0),competition=token)
   self.assertEqual(c.life['injury_games'],left);self.assertFalse(c.fixture_history[-1]['played']);self.assertIn('absence',c.fixture_history[-1]);self.assertEqual((c.matches,c.goals,c.morale,c.stamina,c.coach_trust,c.form_goals),stats);self.assertEqual(c.press_state['negative_run'],negative);self.assertEqual(c.press_state['report']['negative_run'],0)
   before=copy.deepcopy(c.life);c.next_match();self.assertEqual(c.life,before);self.assertTrue(c.load());self.assertEqual(c.life['injury_games'],left)
  self.assertFalse(injuries.active(c))
 def test_world_absence_records_fixture_without_personal_credit(self):
  c=CareerMode(Access(),autoload=False);c.configure_new_player('Alex','Portugal','Portugal');c.accept_starting_offer(c.offers[0]);c.life.update(injury_name='Ankle sprain',injury_games=3)
  token,h,a=c.next_match();before=c.matches+c.international_caps;c.finish_match(h,a,0,0,competition=token)
  self.assertEqual(c.matches+c.international_caps,before);self.assertEqual(c.life['injury_games'],2);self.assertTrue(c.load());self.assertFalse(c.fixture_history[-1]['played'])
 def test_no_double_recovery_and_clean_legacy_data(self):
  c=self.c;c.fixture_history=[dict(date='x',competition='x',home='h',away='a')];c.life.update(injury_name='Calf strain',injury_games=2)
  injuries.complete(c,True);injuries.complete(c,True);self.assertEqual(c.life['injury_games'],1)
  d=clean({'version':1},c);self.assertEqual(d['injury_games'],0)
  d=clean({'version':1,'injury_name':'fake','injury_games':999},c);self.assertEqual(d['injury_games'],0)
