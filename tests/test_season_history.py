import sqlite3,tempfile,unittest,hashlib
from pathlib import Path
from tests.test_division_board import ServerDivisionBoard
from server import division_records,moderation,season_records
from server.install_season_history import apply,sources

class EverySeason(ServerDivisionBoard):
 def test_same_owner_multiple_seasons_and_identical_scores_are_not_collapsed(self):
  for season,goals in ((2026,12),(2027,18),(2028,12)):
   self.submit('a'*64,season=season,player='Alex',goals=goals)
  self.submit('a'*64,season=2027,player='Alex',goals=18)
  self.submit('b'*64,season=2026,player='Other',goals=15)
  entries=division_records.leaders(self.db,1)['entries']
  self.assertEqual([(r['player'],r['goals'])for r in entries],[('Alex',18),('Other',15),('Alex',12),('Alex',12)])
  self.assertEqual(self.db.execute('SELECT COUNT(*) FROM division_records').fetchone()[0],4)
  publisher=moderation.public_id(season_records.identity('a'*64));moderation.moderate(self.db,dict(publisher=publisher,action='ban'))
  self.assertEqual(len(division_records.leaders(self.db,1)['entries']),1)

class SingleFileRepair(unittest.TestCase):
 def test_repair_preserves_database_policy_and_restores_module_on_failure(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);(root/'server').mkdir();payload=sources();self.assertEqual(set(payload),{'server/division_records.py'})
   old=b'# trusted old fixture\n';path=root/'server/division_records.py';path.write_bytes(old)
   db=root/'statistics.sqlite3';db.write_bytes(b'published seasons and counters')
   policy=root/'app-version.json';policy.write_bytes(b'current minimum untouched')
   baseline={'server/division_records.py':[hashlib.sha256(old).hexdigest()]};calls=[]
   def fail():raise RuntimeError('fixture health failure')
   with self.assertRaises(RuntimeError):apply(root,payload,lambda:calls.append('stop'),lambda:calls.append('start'),fail,baseline)
   self.assertEqual(path.read_bytes(),old)
   apply(root,payload,lambda:None,lambda:None,lambda:None,baseline)
   self.assertEqual(path.read_bytes(),payload['server/division_records.py'])
   self.assertEqual(db.read_bytes(),b'published seasons and counters');self.assertEqual(policy.read_bytes(),b'current minimum untouched')

class SeasonHistoryHTTP(unittest.TestCase):
 def test_second_season_keeps_first_visible_through_public_http(self):
  import json
  from urllib.request import Request,urlopen
  from tests.test_usage_collector import CollectorTests
  fixture=CollectorTests();fixture.setUp()
  try:
   for season,goals in ((2026,14),(2027,20)):
    payload=dict(token='a'*64,record=dict(division=2,season=season,player='Alex',goals=goals),consent_version=1)
    with urlopen(Request(fixture.url+'/v5/records',json.dumps(payload).encode(),{'Content-Type':'application/json'}),timeout=2)as response:self.assertEqual(response.status,204)
   with urlopen(fixture.url+'/v5/records?division=2',timeout=2)as response:data=json.load(response)
   self.assertEqual([r['goals']for r in data['entries']],[20,14])
   from online_leaderboard import valid_division_entry
   self.assertTrue(all(valid_division_entry(r)for r in data['entries']))
  finally:fixture.doCleanups()
