import os,tempfile,copy,unittest,random,sqlite3
from unittest.mock import patch
from career import CareerMode
from career_life import age,decline,purchase,retirement,retirement_due,ITEMS
from unpredictable_aim import Aim
from league_status import league_status,league_band,standout
class LifeTests(unittest.TestCase):
 def setUp(self):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);p=patch.dict(os.environ,STRIKER_SAVE_DIR=t.name);p.start();self.addCleanup(p.stop)
  self.c=CareerMode(autoload=False);self.c.accept_starting_offer(self.c.offers[0]);self.c.attend_coach_meeting()
 def test_contract_wage_one_payment_per_week_and_reload(self):
  c=self.c;self.assertGreater(c.life['salary'],0);w=c.life['salary'];c.week+=1;c.save();self.assertEqual(c.life['balance'],w)
  for _ in range(3):c.save()
  self.assertEqual(c.life['balance'],w);self.assertTrue(c.load());self.assertEqual(c.life['balance'],w);c.save();self.assertEqual(c.life['balance'],w)
 def test_purchases_price_inventory_repetition_and_failed_save(self):
  c=self.c;c.life['balance']=100000;self.assertTrue(purchase(c,'studio'));self.assertEqual(c.life['balance'],20000);self.assertFalse(purchase(c,'studio'));self.assertFalse(purchase(c,'mansion'))
  before=copy.deepcopy(c.life)
  with patch.object(c,'save',return_value=False):self.assertFalse(purchase(c,'utility'))
  self.assertEqual(c.life,before);self.assertTrue(purchase(c,'rose'));self.assertTrue(purchase(c,'rose'));self.assertEqual(c.life['owned']['rose'],2);self.assertTrue(c.load());self.assertIn('studio',c.life['owned'])
 def test_age_retirement_and_progressive_difficulty(self):
  c=self.c;self.assertEqual(age(c),18);c.season+=20;self.assertEqual(age(c),38);self.assertTrue(retirement_due(c));self.assertTrue(retirement(c,False));self.assertFalse(retirement_due(c));a=decline(c);c.season+=1;self.assertTrue(retirement_due(c));self.assertGreater(decline(c),a);self.assertTrue(retirement(c,True));self.assertIsNone(c.next_match());self.assertFalse(c.begin_training());self.assertTrue(c.load());self.assertTrue(c.life['retired'])
 def test_five_game_drought_and_hat_trick_feedback(self):
  c=self.c
  for _ in range(4):c.record_coach_performance(0,2,[],False)
  self.assertEqual(c.life['private_meeting'],'');c.record_coach_performance(0,2,[],False);self.assertEqual(c.life['private_meeting'],'drought')
  c.record_coach_performance(3,0,[],True);self.assertIn(c.coach_individual_feedback(),__import__('coach_feedback').HAT_TRICK)
 def test_feedback_rotates_without_consuming_match_rng(self):
  c=self.c;rng=c.rng.getstate();texts=[]
  for _ in range(9):c.week+=1;c.coach_state['games']+=1;texts.append(c.coach_team_feedback())
  self.assertGreaterEqual(len(set(texts)),6);self.assertEqual(c.rng.getstate(),rng)
 def test_uefa_and_fifa_provenance_and_league_tiers(self):
  from league_status import data
  self.assertEqual(data()['countries']['England']['uefa_rank'],1);self.assertLess(league_status('England',2),league_status('England',1));self.assertGreater(league_status('England'),league_status('Afghanistan'))
 def test_standout_favourite_offer_respects_prestige(self):
  c=self.c;c.matches=20;c.goals=15;other=next(t for t in c.current_league.clubs if t.uid!=c.club.uid);c.life['favourite']=other.uid;c.week=0
  offers=c.generate_agent_offers(True);self.assertIn((other.name,c.league_key),offers)
  self.assertTrue(all(league_band(c.leagues[key].country,c.leagues[key].tier)>=league_band(c.current_league.country,c.current_league.tier) for _,key in offers))
class AimTests(unittest.TestCase):
 def test_bounded_unpredictable_and_nonperiodic(self):
  a=Aim(1);b=Aim(2);path=[];other=[]
  for _ in range(600):
   x,z=a.advance(1/60,2.7,3.66,2.44,.2);self.assertLessEqual(abs(x),4.01);self.assertTrue(.2<=z<=2.24);path.append((round(x,3),round(z,3)));other.append(b.advance(1/60,2.7,3.66,2.44,.2))
  self.assertGreater(max(x for x,z in path)-min(x for x,z in path),5);self.assertNotEqual(path[60:120],path[120:180]);self.assertNotEqual(path,other)
class CareerBoardTests(unittest.TestCase):
 def test_career_moderation_categories_and_withdrawal(self):
  from server.season_records import initialize
  from server import moderation
  from server import career_records as records
  db=sqlite3.connect(':memory:');__import__('server.leaderboard',fromlist=['initialize']).initialize(db);initialize(db);moderation.initialize(db);token='a'*64;r=dict(edition='world',country='England',division=1,season=2032,player='Player',team='Club',matches=300,goals=120)
  records.submit(db,dict(token=token,record=r,terms_version=1));self.assertEqual(records.leaders(db,'world','England',1)['entries'],[]);self.assertEqual(len(moderation.queue(db)['entries']),1)
  owner=moderation.public_id(__import__('server.season_records',fromlist=['identity']).identity(token));moderation.moderate(db,dict(publisher=owner,action='approve'))
  self.assertEqual(records.leaders(db,'world','England',1)['entries'][0]['goals'],120);self.assertEqual(moderation.leaders(db,'world','England',1)['entries'],[]);moderation.withdraw(db,token);self.assertEqual(records.leaders(db,'world','England',1)['entries'],[])
class InstallerTests(unittest.TestCase):
 def test_rollback_restores_files_and_keeps_other_data(self):
  from server.install_career_board import apply,FILES
  from pathlib import Path
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'server').mkdir();old={name:b'# original\n' for name in FILES}
   for name,raw in old.items():(root/name).write_bytes(raw)
   (root/'private.db').write_bytes(b'preserve');calls=[]
   with self.assertRaises(RuntimeError):apply(root,{k:b'# new\n' for k in FILES},lambda:calls.append('stop'),lambda:calls.append('start'),lambda:(_ for _ in ()).throw(RuntimeError('offline')))
   self.assertEqual(calls,['stop','start','stop','start']);self.assertTrue(all((root/k).read_bytes()==v for k,v in old.items()));self.assertEqual((root/'private.db').read_bytes(),b'preserve')
 def test_real_local_v4_endpoint_starts_and_preserves_season_board(self):
  import threading,json,urllib.request
  from server.usage_collector import Collector
  with tempfile.TemporaryDirectory() as d:
   server=Collector(('127.0.0.1',0),d+'/stats.db');thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
   try:
    base='http://127.0.0.1:'+str(server.server_port)
    for version in (3,4):
     with urllib.request.urlopen(base+f'/v{version}/records?edition=world&country=England&division=1') as response:self.assertEqual(json.load(response)['schema'],version)
   finally:server.shutdown();server.server_close();thread.join()
