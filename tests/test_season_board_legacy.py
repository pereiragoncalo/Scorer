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
