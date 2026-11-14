import copy,os,tempfile,unittest
from unittest.mock import patch
from career import CareerMode
from career_life import sync,clean
import contract_negotiation as contracts

class Contracts(unittest.TestCase):
 def setUp(self):
  directory=tempfile.TemporaryDirectory();self.addCleanup(directory.cleanup)
  env=patch.dict(os.environ,STRIKER_SAVE_DIR=directory.name);env.start();self.addCleanup(env.stop)
  self.c=CareerMode(autoload=False)
 def initial(self):return contracts.open_meeting(self.c,self.c.offers[0],self.c.league_key,True)
 def signed(self):
  row=self.initial();self.assertTrue(contracts.sign(self.c,row['club_uid']));return self.c
 def test_hearing_and_proposing_do_not_sign_or_award_anything(self):
  c=self.c;state=c.rng.getstate();owned=copy.deepcopy(c.life['owned']);balance=c.life['balance']
  row=self.initial();uid=row['club_uid'];contracts.change(c,uid,'premium');contracts.propose(c,uid)
  self.assertFalse(c.club_name);self.assertEqual(c.life['owned'],owned);self.assertEqual(c.life['balance'],balance);self.assertEqual(c.rng.getstate(),state)
  self.assertTrue(contracts.sign(c,uid));self.assertEqual(c.life['salary'],row['offer']['salary'])
  self.assertFalse(contracts.sign(c,uid))
 def test_draft_cannot_be_signed_and_rounds_cannot_be_reset_by_reopening(self):
  row=self.initial();uid=row['club_uid'];contracts.change(self.c,uid,'years')
  self.assertFalse(contracts.sign(self.c,uid))
  for _ in range(3):self.assertTrue(contracts.propose(self.c,uid))
  reopened=self.initial();self.assertEqual(reopened['round'],3)
  self.assertFalse(contracts.propose(self.c,uid));self.assertFalse(contracts.change(self.c,uid,'home'))
 def test_unaffordable_package_gets_a_real_counter_offer(self):
  row=self.initial();uid=row['club_uid']
  for key in ('home','car','squad'):contracts.change(self.c,uid,key)
  for _ in range(4):contracts.change(self.c,uid,'premium')
  self.assertIn('beyond',contracts.advice(self.c,uid));contracts.propose(self.c,uid)
  self.assertEqual(row['status'],'counter');self.assertNotEqual(row['offer'],contracts.package(row));self.assertEqual(self.c.life['owned'],{})
 def test_accepted_benefits_apply_only_once_and_persist_with_locked_salary(self):
  c=self.c
  with patch('career_life.quote',return_value=50000):row=self.initial()
  uid=row['club_uid'];row['request'].update(years=5,home=True,car=True)
  contracts.propose(c,uid);self.assertEqual(row['status'],'accepted')
  self.assertTrue(contracts.sign(c,uid));self.assertEqual(c.life['owned'][row['offer']['home']],1);self.assertEqual(c.life['owned'][row['offer']['car']],1)
  record=copy.deepcopy(c.life['contract']);wage=c.life['salary'];c.goals=100;c.save()
  self.assertEqual(c.life['salary'],wage);self.assertTrue(c.load());self.assertEqual(c.life['contract'],record)
 def test_squad_investment_is_fulfilled_at_signature_and_rolled_back_on_save_failure(self):
  c=self.c;row=self.initial();row['request'].update(years=5,squad=True);contracts.propose(c,row['club_uid'])
  team=next(t for t in c.current_league.clubs if t.name==row['club']);rating=team.rating;before=copy.deepcopy(c.life);state=c.rng.getstate()
  with patch.object(c,'save',return_value=False):self.assertFalse(contracts.sign(c,row['club_uid']))
  self.assertFalse(c.club_name);self.assertEqual(c.life,before);self.assertEqual(team.rating,rating);self.assertEqual(c.rng.getstate(),state)
  self.assertTrue(contracts.sign(c,row['club_uid']));self.assertEqual(team.rating,min(99.,rating+2.))
  improved=team.rating;self.assertTrue(c.load());self.assertEqual(c.club.rating,improved)
 def test_transfer_hears_multiple_clubs_without_switching_and_restores_meetings_on_load(self):
  c=self.signed();c.generate_agent_offers(guaranteed=True);club=c.club_name;meetings=[]
  for name,key in c.agent_offers[:2]:
   row=contracts.open_meeting(c,name,key);contracts.change(c,row['club_uid'],'premium');contracts.propose(c,row['club_uid']);meetings.append(copy.deepcopy(row))
  self.assertEqual(c.club_name,club);self.assertTrue(c.load())
  for row in meetings:self.assertEqual(contracts.current(c,row['club_uid']),row)
 def test_failed_transfer_preserves_contract_assets_and_current_club(self):
  c=self.signed();c.generate_agent_offers(guaranteed=True);name,key=c.agent_offers[0];row=contracts.open_meeting(c,name,key);row['request'].update(years=5,squad=True);contracts.propose(c,row['club_uid'])
  before=(c.club_name,c.league_key,copy.deepcopy(c.life),copy.deepcopy(c.development));team=next(t for t in c.leagues[key].clubs if t.name==name);rating=team.rating
  with patch.object(c,'save',return_value=False):self.assertFalse(contracts.sign(c,row['club_uid']))
  self.assertEqual((c.club_name,c.league_key,c.life,c.development),before);self.assertEqual(team.rating,rating)
 def test_renewal_extends_years_without_transfer_or_cup_reset(self):
  c=self.signed();c.season=c.life['contract']['end_season']-1;c.cup_active=True;count=c.development['transfers'];coach=copy.deepcopy(c.coach_appearance)
  row=contracts.open_meeting(c,c.club_name,c.league_key);self.assertIsNotNone(row)
  self.assertTrue(contracts.sign(c,row['club_uid']));self.assertEqual(c.life['contract']['start_season'],c.season);self.assertGreater(contracts.remaining(c),1)
  self.assertEqual(c.development['transfers'],count);self.assertEqual(c.coach_appearance,coach);self.assertTrue(c.cup_active)
 def test_expiry_stops_salary_and_allows_renewal(self):
  c=self.signed();wage=c.life['salary'];record=c.life['contract'];c.life['paid_month']=record['end_season']*12+6;balance=c.life['balance'];c.season=record['end_season'];c.week=0
  sync(c);self.assertEqual(c.life['balance'],balance+wage);self.assertEqual(c.life['salary'],0);self.assertTrue(contracts.expired(c))
  self.assertTrue(contracts.sign(c,contracts.open_meeting(c,c.club_name,c.league_key)['club_uid']));self.assertFalse(contracts.expired(c))
 def test_expired_player_can_hear_offers_outside_a_transfer_window(self):
  c=self.signed();c.season=c.life['contract']['end_season'];c.week=38
  self.assertNotIn(c.current_date.month,(1,2,7,8));self.assertTrue(contracts.expired(c));self.assertTrue(c.transfer_window_open)
  c.generate_agent_offers(guaranteed=True);self.assertTrue(c.agent_offers)
  name,key=c.agent_offers[0];self.assertIsNotNone(contracts.open_meeting(c,name,key))
 def test_midseason_transfer_preserves_full_contract_years(self):
  c=self.signed();c.week=28;c.generate_agent_offers(guaranteed=True);name,key=c.agent_offers[0]
  row=contracts.open_meeting(c,name,key);signed_on=c.current_date
  self.assertTrue(contracts.sign(c,row['club_uid']))
  self.assertEqual(c.life['contract']['end_date'],contracts.expiry_date(signed_on,row['offer']['years']).isoformat())
  self.assertEqual(contracts.remaining(c),row['offer']['years'])
 def test_legacy_migration_keeps_salary_assets_and_gives_two_remaining_seasons(self):
  c=self.signed();raw=copy.deepcopy(c.life);raw.pop('contract');raw.pop('negotiations');c.life=clean(raw,c)
  self.assertEqual(contracts.remaining(c),2);self.assertEqual(c.life['salary'],raw['salary']);self.assertEqual(c.life['owned'],raw['owned'])
 def test_export_import_keeps_contract_and_pending_club_meetings(self):
  from career_transfer import export_career,validated_import
  c=self.signed();c.generate_agent_offers(guaranteed=True);name,key=c.agent_offers[0]
  row=contracts.open_meeting(c,name,key);contracts.change(c,row['club_uid'],'home');contracts.propose(c,row['club_uid'])
  candidate=validated_import(c,export_career(c))
  self.assertEqual(candidate.life['contract'],c.life['contract']);self.assertEqual(candidate.life['negotiations'],c.life['negotiations'])
 def test_older_player_gets_shorter_counter_offer(self):
  c=self.signed();c.season=c.life['start_season']+18;row=contracts.open_meeting(c,c.club_name,c.league_key);row['request']['years']=5
  self.assertIn('many years',contracts.advice(c,row['club_uid']));contracts.propose(c,row['club_uid']);self.assertEqual(row['offer']['years'],2)
 def test_malformed_nested_terms_are_bounded_and_discarded(self):
  c=self.signed();raw=copy.deepcopy(c.life);raw['contract']['years']=999;raw['negotiations']={'bad':{'request':'x'*10000}}
  d=clean(raw,c);self.assertIsNone(d['contract']);self.assertEqual(d['negotiations'],{})

class ExactYears(unittest.TestCase):
 def test_january_contract_preserves_full_years_and_leap_day(self):
  from datetime import date
  self.assertEqual(contracts.expiry_date(date(2027,1,15),2),date(2029,1,15))
  self.assertEqual(contracts.expiry_date(date(2028,2,29),1),date(2029,2,28))
