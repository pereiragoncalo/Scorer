import json,tempfile,unittest
from pathlib import Path
from unittest.mock import Mock
from server.install_play_candidate import apply,sources

class PlayPolicyInstallerTests(unittest.TestCase):
 def test_combined_deployment_rolls_back_files_when_verification_fails(self):
  with tempfile.TemporaryDirectory() as directory:
   target=Path(directory);(target/'server').mkdir()
   original={name:b'# existing test source' for name in sources() if name.endswith('.py')}
   original['public.json']=b'{"publication_status":"published","support_email":"goncalo@clemir.com"}'
   for name,raw in original.items():(target/name).write_bytes(raw)
   stop=Mock();start=Mock()
   with self.assertRaisesRegex(RuntimeError,'test failure'):
    apply(target,sources(),stop,start,Mock(side_effect=RuntimeError('test failure')))
   self.assertEqual(stop.call_count,2);self.assertEqual(start.call_count,2)
   for name,raw in original.items():self.assertEqual((target/name).read_bytes(),raw)
 def test_symlink_is_rejected_before_service_stop(self):
  with tempfile.TemporaryDirectory() as directory:
   target=Path(directory);(target/'server').mkdir()
   (target/'server/usage_collector.py').write_text('# existing')
   (target/'server/moderation.py').write_text('# existing')
   (target/'private').write_text('keep')
   (target/'public.json').symlink_to(target/'private')
   stop=Mock()
   with self.assertRaises(ValueError):apply(target,sources(),stop,Mock(),Mock())
   stop.assert_not_called();self.assertEqual((target/'private').read_text(),'keep')
 def test_payload_is_complete_and_optional_policy_is_published(self):
  payload=sources();config=json.loads(payload['public.json'])
  self.assertEqual(config['publication_status'],'published')
  self.assertIn('voluntary',config['legal_basis'])
  self.assertIn(b'Career category',payload['server/public_pages.py'])
