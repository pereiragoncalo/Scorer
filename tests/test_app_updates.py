import json,tempfile,threading,time,unittest
from pathlib import Path
from unittest.mock import patch
from app_updates import UpdateState
from version_policy import validate,PACKAGE,STORE_URL

def policy(minimum=1030004,latest=1030004):return dict(schema=1,package=PACKAGE,minimum_version_code=minimum,latest_version_code=latest,latest_version_name='1.0')
class UpdateTests(unittest.TestCase):
 def test_codes_not_version_names_determine_mandatory_update(self):
  with tempfile.TemporaryDirectory() as d:
   state=UpdateState(1030003,Path(d)/'cache');state.apply(policy());self.assertTrue(state.required)
   state.installed=1030004;self.assertFalse(state.required);state.installed=1030005;self.assertFalse(state.required)
 def test_offline_unknown_allows_but_known_minimum_survives_restart(self):
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'cache';state=UpdateState(1030003,path);self.assertFalse(state.required)
   state.apply(policy());reloaded=UpdateState(1030003,path);self.assertTrue(reloaded.required)
   done=threading.Event();reloaded.check_async(lambda:done.set() if not reloaded.checking else None,lambda f:f(),fetcher=lambda:(_ for _ in ()).throw(OSError()))
   self.assertTrue(done.wait(1));self.assertTrue(reloaded.required)
 def test_valid_policy_can_revoke_an_accidental_block(self):
  with tempfile.TemporaryDirectory() as d:
   state=UpdateState(1030003,Path(d)/'cache');state.apply(policy());state.apply(policy(0));self.assertFalse(state.required)
 def test_bad_policy_cannot_clear_known_block_or_choose_store_url(self):
  with tempfile.TemporaryDirectory() as d:
   state=UpdateState(1030003,Path(d)/'cache');state.apply(policy())
   for bad in [dict(policy(),package='another.app'),dict(policy(),minimum_version_code=True),dict(policy(),minimum_version_code=1030005),dict(policy(),url='https://evil.example')]:
    with self.assertRaises(ValueError):state.apply(bad)
    self.assertTrue(state.required)
   self.assertEqual(STORE_URL,'https://play.google.com/store/apps/details?id='+PACKAGE)
 def test_slow_dns_deadline_allows_unknown_and_ignores_late_response(self):
  with tempfile.TemporaryDirectory() as d:
   release=threading.Event();done=threading.Event();state=UpdateState(1030003,Path(d)/'cache')
   def slow():release.wait(1);return policy()
   state.check_async(lambda:done.set() if not state.checking else None,lambda f:f(),fetcher=slow,timeout=.03)
   self.assertTrue(done.wait(1));self.assertFalse(state.locked);release.set();time.sleep(.03);self.assertIsNone(state.policy)
 def test_cache_write_failure_does_not_bypass_current_block(self):
  with tempfile.TemporaryDirectory() as d:
   state=UpdateState(1030003,Path(d)/'cache')
   with patch('app_updates.tempfile.mkstemp',side_effect=OSError('disk full')):state.apply(policy())
   self.assertTrue(state.required)

class FetchTests(unittest.TestCase):
 def test_request_uses_verified_tls_no_player_identifiers_and_bounded_response(self):
  from unittest.mock import MagicMock
  import app_updates
  response=MagicMock();response.__enter__.return_value=response;response.read.return_value=json.dumps(policy()).encode();opener=MagicMock();opener.open.return_value=response
  with patch('network_tls.verified_context') as tls,patch('app_updates.build_opener',return_value=opener):
   self.assertEqual(app_updates.fetch(),policy());tls.assert_called_once()
  request=opener.open.call_args.args[0];self.assertEqual(request.full_url,app_updates.ENDPOINT);self.assertIsNone(request.data)
  self.assertEqual(opener.open.call_args.kwargs['timeout'],4);response.read.assert_called_once_with(4097)
  self.assertIsNone(app_updates.NoRedirect().redirect_request(None,None,302,'Moved',{},'https://evil.example'))
