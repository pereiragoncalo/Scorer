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
