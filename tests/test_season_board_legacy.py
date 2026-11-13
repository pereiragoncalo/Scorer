"""Known initial bastion maintenance must upgrade without loosening source pins."""
import hashlib,json,sqlite3,tempfile,unittest
from pathlib import Path
from server.install_season_board import apply,sources
ROOT=Path(__file__).resolve().parents[1]

class LegacyMaintenanceUpgrade(unittest.TestCase):
 def prepare(self,root):
  (root/'server').mkdir();payload=sources()
  for name,raw in payload.items():(root/name).write_bytes(raw)
  legacy=(ROOT/'tests/fixtures/maintenance-initial.txt').read_bytes()
  (root/'server/maintenance.py').write_bytes(legacy)
  baseline=json.loads((ROOT/'docs/data/season_board_baseline.json').read_text())
  self.assertIn(hashlib.sha256(legacy).hexdigest(),baseline['server/maintenance.py'])
  return payload,legacy,baseline
 def test_known_initial_file_upgrades_backups_and_preserves_database_and_credentials(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)/'service';root.mkdir();payload,legacy,baseline=self.prepare(root)
   (root/'token').write_text('private-fixture');(root/'data.sqlite').write_bytes(b'untouched fixture database');calls=[]
   backup=apply(root,payload,lambda:calls.append('stop'),lambda:calls.append('start'),lambda:calls.append('check'),baseline)
   self.assertEqual(calls,['stop','start','check']);self.assertEqual((backup/'server/maintenance.py').read_bytes(),legacy)
   self.assertEqual((root/'server/maintenance.py').read_bytes(),payload['server/maintenance.py'])
   self.assertEqual((root/'data.sqlite').read_bytes(),b'untouched fixture database');self.assertEqual((root/'token').read_text(),'private-fixture')
   from server.maintenance import backup as aggregate_backup
   db=Path(temp)/'fixture.sqlite';out=Path(temp)/'backup.sqlite'
   with sqlite3.connect(db) as conn:
    conn.executescript("CREATE TABLE totals(day TEXT,event TEXT,count INTEGER);INSERT INTO totals VALUES('2026-11-13','sessions',7);CREATE TABLE division_records(player TEXT);INSERT INTO division_records VALUES('Not for backup');")
   aggregate_backup(db,out)
   with sqlite3.connect(out) as conn:
    self.assertEqual(conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall(),[('totals',)])
    self.assertEqual(conn.execute('SELECT count FROM totals').fetchone()[0],7)
 def test_unrecognized_file_still_stops_before_any_service_change(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);payload,legacy,baseline=self.prepare(root);calls=[]
   (root/'server/maintenance.py').write_bytes(legacy+b'\n# custom\n')
   with self.assertRaisesRegex(ValueError,'maintenance.py.*SHA256'):
    apply(root,payload,lambda:calls.append('stop'),lambda:calls.append('start'),lambda:None,baseline)
   self.assertEqual(calls,[]);self.assertEqual((root/'server/maintenance.py').read_bytes(),legacy+b'\n# custom\n')
 def test_legacy_maintenance_is_restored_if_health_check_fails(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);payload,legacy,baseline=self.prepare(root);calls=[]
   def fail():raise RuntimeError('failed health')
   with self.assertRaises(RuntimeError):apply(root,payload,lambda:calls.append('stop'),lambda:calls.append('start'),fail,baseline)
   self.assertEqual((root/'server/maintenance.py').read_bytes(),legacy);self.assertEqual(calls,['stop','start','stop','start'])

class ObservedBastionUpgrade(unittest.TestCase):
 def test_complete_released_statistics_backend_with_initial_maintenance_upgrades_over_real_http(self):
  self.rehearse(False)
 def test_installed_1030020_pending_season_becomes_visible_without_resending(self):
  self.rehearse(True)
 def rehearse(self,existing_v5):
  import runpy,subprocess,os,selectors
  from urllib.request import urlopen
  from urllib.error import HTTPError
  from server.install_season_board import verify
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);old=runpy.run_path(str(ROOT/'docs/data/server/Scorer-Statistics-Agreement-Backend-Repair-1.py'),run_name='old_fixture')['sources']()
   observed='e5f1d1c0f5203ad7efa90ebe8afca4ad0787f8f32cd2345c916507c023c305a3'
   self.assertEqual(hashlib.sha256(old['server/usage_collector.py']).hexdigest(),observed)
   old['server/maintenance.py']=(ROOT/'tests/fixtures/maintenance-initial.txt').read_bytes()
   if existing_v5:old.update(runpy.run_path(str(ROOT/'docs/data/server/Scorer-Season-Leaderboard-Backend-Repair-2.py'),run_name='v5_fixture')['sources']())
   for name,raw in old.items():
    path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
   process=None;port=None
   def stop():
    nonlocal process
    if process:
     process.terminate();process.wait(timeout=5);process.stdout.close();process.stderr.close();process=None
   def start():
    nonlocal process,port
    code="from server.usage_collector import Collector;s=Collector(('127.0.0.1',0),'fixture.sqlite','fixture-admin','public.json');print(s.server_port,flush=True);s.serve_forever()"
    process=subprocess.Popen([__import__('sys').executable,'-B','-u','-c',code],cwd=root,env=dict(os.environ,PYTHONPATH=str(root)),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    with selectors.DefaultSelector() as select:
     select.register(process.stdout,selectors.EVENT_READ)
     if not select.select(8):raise RuntimeError('Fixture startup timed out')
    line=process.stdout.readline().strip()
    if not line.isdigit():raise RuntimeError(process.stderr.read())
    port=int(line)
   def get(path):
    with urlopen(f'http://127.0.0.1:{port}'+path,timeout=3) as r:return json.load(r)
   try:
    start();self.assertTrue(get('/health')['ok'])
    if existing_v5:self.assertEqual(get('/v5/records?division=2')['entries'],[])
    else:
     with self.assertRaises(HTTPError):get('/v5/records?division=1')
    with sqlite3.connect(root/'fixture.sqlite') as db:db.execute("INSERT INTO totals VALUES(date('now'),'sessions',17)")
    if existing_v5:
     with sqlite3.connect(root/'fixture.sqlite') as db:db.execute("INSERT INTO division_records VALUES(?,2,2027,'Published fixture',40,'pending',1,datetime('now'))",('a'*64,))
     self.assertEqual(get('/v5/records?division=2')['entries'],[])
    policy=(root/'version-policy.json').read_bytes();config=(root/'public.json').read_bytes()
    apply(root,sources(),stop,start,lambda:verify(port),json.loads((ROOT/'docs/data/season_board_baseline.json').read_text()))
    self.assertEqual(get('/v5/records?division=1')['schema'],5);self.assertEqual(get('/v5/records?division=2')['schema'],5)
    self.assertEqual(get('/v3/records?edition=world&country=England&division=1')['schema'],3)
    if existing_v5:self.assertEqual(get('/v5/records?division=2')['entries'][0]['player'],'Published fixture')
    with sqlite3.connect(root/'fixture.sqlite') as db:self.assertEqual(db.execute("SELECT count FROM totals WHERE event='sessions'").fetchone()[0],17)
    self.assertEqual((root/'version-policy.json').read_bytes(),policy);self.assertEqual((root/'public.json').read_bytes(),config)
   finally:stop()
