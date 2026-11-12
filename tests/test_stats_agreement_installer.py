import json,tempfile,unittest
from pathlib import Path
from server.install_stats_agreement import sources,preflight,apply
from tests.test_app_updates import policy

class StatsInstallerTests(unittest.TestCase):
 def target(self,root,payload):
  (root/'server').mkdir()
  for name,raw in payload.items():(root/name).write_bytes(raw)
  (root/'version-policy.json').write_text(json.dumps(policy(1030006,1030006)))
  (root/'private-token').write_text('fixture-private-token')
  config=json.loads((root/'public.json').read_text());config['legal_basis']='old startup acknowledgment does not enable statistics';(root/'public.json').write_text(json.dumps(config))
 def test_full_dependency_closure_and_existing_operator_minimum_preserved(self):
  payload=sources();preflight(payload)
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);self.target(root,payload);events=[]
   apply(root,payload,lambda:events.append('stop'),lambda:events.append('start'),lambda:events.append('check'))
   self.assertEqual(events,['stop','start','check']);self.assertEqual(json.loads((root/'version-policy.json').read_text())['minimum_version_code'],1030006)
   self.assertEqual((root/'private-token').read_text(),'fixture-private-token')
   self.assertIn('1030005',json.loads((root/'public.json').read_text())['legal_basis'])
 def test_failed_restart_rolls_back_every_delivered_file(self):
  payload=sources()
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);self.target(root,payload);before={name:(root/name).read_bytes() for name in payload};starts=[]
   def start():
    starts.append(1)
    if len(starts)==1:raise RuntimeError('fixture startup failed')
   with self.assertRaisesRegex(RuntimeError,'startup failed'):apply(root,payload,lambda:None,start,lambda:None)
   self.assertEqual({name:(root/name).read_bytes() for name in payload},before)
   self.assertEqual((root/'private-token').read_text(),'fixture-private-token')
 def test_complete_install_and_real_http_validation_from_source_and_shipped_bundle(self):
  import runpy,subprocess,sys,time,sqlite3
  from server import install_stats_agreement as installer
  for api in (vars(installer),runpy.run_path(str(Path(__file__).resolve().parents[1]/'docs/data/server/Scorer-Statistics-Agreement-Backend-Repair-1.py'))):
   with self.subTest(shipped=api.get('PAYLOAD') is not None),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);payload=api['sources']();self.target(root,payload);process=None
    # Persist an existing aggregate and check that a real restart/HTTP check keeps it.
    from server.usage_collector import Collector
    seed=Collector(('127.0.0.1',0),root/'data.sqlite');seed.server_close()
    with sqlite3.connect(root/'data.sqlite') as db:db.execute("INSERT INTO totals VALUES('2026-11-09','sessions',17)")
    code="import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from server.usage_collector import Collector;r=Path(sys.argv[1]);s=Collector(('127.0.0.1',0),r/'data.sqlite','fixture-admin',str(r/'public.json'));(r/'port').write_text(str(s.server_port));s.serve_forever()"
    def stop():
     nonlocal process
     if process is not None:process.terminate();process.wait(timeout=5);process.stderr.close();process=None
    def start():
     nonlocal process
     (root/'port').unlink(missing_ok=True)
     process=subprocess.Popen([sys.executable,'-I','-B','-c',code,str(root)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
     deadline=time.monotonic()+5
     while not (root/'port').exists():
      if process.poll() is not None:self.fail(process.stderr.read().decode())
      if time.monotonic()>deadline:self.fail('Server failed to start')
      time.sleep(.01)
    try:
     api['apply'](root,payload,stop,start,lambda:api['verify'](int((root/'port').read_text())))
     self.assertEqual(json.loads((root/'version-policy.json').read_text())['minimum_version_code'],1030006)
     with sqlite3.connect(root/'data.sqlite') as db:self.assertEqual(db.execute('SELECT count FROM totals').fetchone()[0],17)
     self.assertEqual((root/'private-token').read_text(),'fixture-private-token')
    finally:
     stop()
