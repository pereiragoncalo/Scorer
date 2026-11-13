import json,os,sqlite3,tempfile,time,unittest
from collections import Counter
from unittest.mock import patch
from server import moderation,season_records
from server import division_records as dbrecords
from online_leaderboard import Leaderboard
from season_sharing import approve,decline
from goal_timing import spaced_minutes,goal_events
import random

class ServerDivisionBoard(unittest.TestCase):
 def setUp(self):
  self.db=sqlite3.connect(':memory:');self.db.execute('CREATE TABLE totals(day TEXT,event TEXT,count INT)');self.db.execute('CREATE TABLE leaderboard(id TEXT,alias TEXT,score INT)');season_records.initialize(self.db);moderation.initialize(self.db)
 def tearDown(self):self.db.close()
 def submit(self,token,division=1,season=2026,player='Public name',goals=10):
  dbrecords.submit(self.db,dict(token=token,record=dict(division=division,season=season,player=player,goals=goals),consent_version=1))
 def approve(self,token):
  publisher=moderation.public_id(season_records.identity(token));moderation.moderate(self.db,dict(publisher=publisher,action='approve'));return publisher
 def test_two_global_divisions_are_separate_and_public_fields_are_minimal(self):
  self.submit('a'*64,1,player='Ana',goals=12);self.submit('b'*64,1,player='Bruno',goals=15);self.submit('c'*64,2,player='Carlos',goals=30)
  self.assertEqual(len(dbrecords.leaders(self.db,1)['entries']),2)
  one=dbrecords.leaders(self.db,1)['entries'];two=dbrecords.leaders(self.db,2)['entries']
  self.assertEqual([(r['player'],r['goals'])for r in one],[('Bruno',15),('Ana',12)])
  self.assertEqual([(r['player'],r['goals'])for r in two],[('Carlos',30)])
  self.assertEqual(set(one[0]),{'player','goals','publisher'})
 def test_consent_exactness_idempotence_best_season_and_withdraw(self):
  self.submit('a'*64);self.approve('a'*64);self.submit('a'*64)
  self.assertEqual(len(dbrecords.leaders(self.db,1)['entries']),1)
  self.submit('a'*64,season=2027,player='Other approved name',goals=5);self.approve('a'*64)
  self.assertEqual(dbrecords.leaders(self.db,1)['entries'][0]['player'],'Public name')
  self.assertEqual(moderation.queue(self.db)['total'],2)
  moderation.withdraw(self.db,'a'*64);self.assertEqual(dbrecords.leaders(self.db,1)['entries'],[])
  with self.assertRaises(ValueError):dbrecords.submit(self.db,dict(token='a'*64,record=dict(division=1,season=2026,player='Name',goals=1)))
 def test_pending_choices_become_public_but_rejected_and_banned_records_stay_hidden(self):
  for token in ('a','b','c'):self.submit(token*64)
  self.db.execute("UPDATE division_records SET state='pending'")
  self.db.execute("UPDATE division_records SET state='rejected' WHERE owner=?",(season_records.identity('b'*64),))
  self.db.execute("UPDATE division_records SET consent=0 WHERE owner=?",(season_records.identity('c'*64),))
  dbrecords.initialize(self.db)
  self.assertEqual(len(dbrecords.leaders(self.db,1)['entries']),1)
  publisher=moderation.public_id(season_records.identity('a'*64))
  moderation.moderate(self.db,dict(publisher=publisher,action='ban'))
  self.assertEqual(dbrecords.leaders(self.db,1)['entries'],[])
  with self.assertRaises(PermissionError):self.submit('b'*64)
 def test_reports_ban_and_erase_include_new_records(self):
  self.submit('a'*64);publisher=self.approve('a'*64)
  moderation.report(self.db,dict(token='b'*64,publisher=publisher,reason='abuse'))
  moderation.moderate(self.db,dict(publisher=publisher,action='ban'));self.assertEqual(dbrecords.leaders(self.db,1)['entries'],[])
  with self.assertRaises(PermissionError):self.submit('a'*64,season=2027)
  moderation.moderate(self.db,dict(publisher=publisher,action='erase'));self.assertEqual(self.db.execute('SELECT COUNT(*) FROM division_records').fetchone()[0],0)

class ClientConsent(unittest.TestCase):
 def wait(self,b):
  for _ in range(100):
   if not b.busy:return
   time.sleep(.01)
  self.fail('Worker did not complete')
 def test_open_is_read_only_and_no_legacy_bulk_optin_publishes(self):
  with tempfile.TemporaryDirectory() as tmp:
   b=Leaderboard(tmp,'https://example.test');calls=[]
   def request(path,payload=None):
    calls.append((path,payload));return dict(schema=5,division=2,entries=[])
   b.request=request;b.refresh_division(2);self.wait(b)
   self.assertEqual(calls,[('/v5/records?division=2',None)])
   b.enabled=True;b.career_enabled=True;b.save();restored=Leaderboard(tmp,'https://example.test');self.assertFalse(restored.enabled)
   self.assertFalse(restored.approved_seasons)
 def test_explicit_name_and_one_season_queue_survive_offline(self):
  with tempfile.TemporaryDirectory() as tmp:
   b=Leaderboard(tmp,'https://example.test');r=dict(division=1,season=2026,player='Career name',goals=9)
   with self.assertRaises(ValueError):b.enqueue_season([r],'')
   b.enqueue_season([r],'Chosen name');self.assertEqual(r['player'],'Career name')
   b.request=lambda *args:(_ for _ in ()).throw(OSError('offline'));b.flush_approved();self.wait(b)
   restored=Leaderboard(tmp,'https://example.test');self.assertEqual(restored.approved_seasons[0]['record']['player'],'Chosen name')
   calls=[];restored.request=lambda p,payload=None:calls.append((p,payload)) or {}
   restored.flush_approved();self.wait(restored)
   self.assertEqual(len(calls),1);self.assertEqual(calls[0][0],'/v5/records');self.assertEqual(set(calls[0][1]),{'token','record','consent_version'})
   self.assertEqual(restored.approved_seasons,[])

class TimingTests(unittest.TestCase):
 def test_events_keep_exact_score_and_avoid_duplicate_highlight_minutes(self):
  for seed in range(100):
   rng=random.Random(seed);chances=spaced_minutes(rng,range(3,94),3);events=goal_events(rng,3,2,95,chances)
   self.assertEqual(Counter(s for _,s in events),{'home':3,'away':2});self.assertEqual(len({t for t,_ in events}),5)
   self.assertFalse(set(chances)&{t for t,_ in events});self.assertTrue(all(2<=t<=95 for t,_ in events))
 def test_spacing_reduces_but_does_not_ban_close_goals(self):
  old=new=0
  for seed in range(3000):
   rng=random.Random(seed);before=sorted(rng.randint(2,95)for _ in range(4));old+=sum(b-a<=2 for a,b in zip(before,before[1:]))
   times=[t for t,_ in goal_events(random.Random(seed),2,2,95,())];new+=sum(b-a<=2 for a,b in zip(times,times[1:]))
  self.assertGreater(new,0);self.assertLess(new,old*.35)

class SeasonChoiceAndLedger(unittest.TestCase):
 def test_decline_and_failed_save_never_leave_authorized_jobs(self):
  from types import SimpleNamespace
  with tempfile.TemporaryDirectory() as tmp:
   board=Leaderboard(tmp,'https://example.test')
   c=SimpleNamespace(season_review=dict(pending=True,share_choice='unasked',public_records=[dict(division=1,season=2026,player='Local',goals=5)]),save=lambda:False)
   self.assertFalse(approve(c,board,'Public'));self.assertFalse(board.approved_seasons);self.assertTrue(c.season_review['pending'])
   c.save=lambda:True
   self.assertTrue(decline(c));self.assertEqual(c.season_review['share_choice'],'declined');self.assertFalse(board.approved_seasons)
 def test_queued_consent_is_bound_to_original_service(self):
  with tempfile.TemporaryDirectory() as tmp:
   board=Leaderboard(tmp,'https://example.test');board.enqueue_season([dict(division=1,season=2026,player='Local',goals=5)],'Public')
   self.assertFalse(Leaderboard(tmp,'https://other.test').approved_seasons)
 def test_league_goals_accumulate_across_countries_but_remain_separate_by_tier(self):
  from types import SimpleNamespace as Obj
  from division_records import record_match,snapshots,clean
  c=Obj(season=2026,world_unlocked=True,player_name='Local',division_stats=None,current_league=Obj(tier=2))
  record_match(c,4);c.current_league=Obj(tier=1);record_match(c,3);c.current_league=Obj(tier=2);record_match(c,2)
  self.assertEqual([(r['division'],r['goals'])for r in snapshots(c)],[(1,3),(2,6)])
  frozen=snapshots(c);c.season+=1;self.assertEqual(snapshots(c),[]);self.assertEqual(frozen[1]['goals'],6)

class RealHttpAndInstaller(unittest.TestCase):
 def test_real_http_requires_per_season_consent_and_pools_division(self):
  from tests.test_usage_collector import CollectorTests
  from urllib.request import Request,urlopen
  from urllib.error import HTTPError
  fixture=CollectorTests();fixture.setUp()
  try:
   record=dict(division=2,season=2026,player='Public',goals=12)
   def post(payload):
    return urlopen(Request(fixture.url+'/v5/records',json.dumps(payload).encode(),{'Content-Type':'application/json'}),timeout=2)
   with self.assertRaises(HTTPError):post(dict(token='a'*64,record=record))
   with post(dict(token='a'*64,record=record,consent_version=1)) as response:self.assertEqual(response.status,204)
   with sqlite3.connect(fixture.db) as db:moderation.moderate(db,dict(publisher=moderation.public_id(season_records.identity('a'*64)),action='approve'))
   with urlopen(fixture.url+'/v5/records?division=2',timeout=2) as response:self.assertEqual(json.load(response)['entries'][0]['goals'],12)
   with self.assertRaises(HTTPError):urlopen(fixture.url+'/v5/records?division=2&country=Portugal',timeout=2)
  finally:fixture.doCleanups()
 def test_installer_rejects_unknown_sources_and_rolls_back_on_health_failure(self):
  from pathlib import Path
  from server.install_season_board import apply,sources
  import hashlib
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/'service';(root/'server').mkdir(parents=True);payload=sources();prior={}
   for name in payload:
    prior[name]=b'# existing fixture\n';(root/name).write_bytes(prior[name])
   calls=[]
   with self.assertRaises(ValueError):apply(root,payload,lambda:calls.append('stop'),lambda:None,lambda:None,{})
   self.assertEqual(calls,[])
   baseline={name:[hashlib.sha256(raw).hexdigest()]for name,raw in prior.items()}
   def fail():raise RuntimeError('Failed health check')
   with self.assertRaises(RuntimeError):apply(root,payload,lambda:calls.append('stop'),lambda:calls.append('start'),fail,baseline)
   self.assertEqual({name:(root/name).read_bytes()for name in payload},prior)
   self.assertEqual(calls,['stop','start','stop','start'])
