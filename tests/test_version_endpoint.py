import json,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
from server.usage_collector import Collector
from server.version_updates import write
from tests.test_app_updates import policy

class VersionEndpointTests(unittest.TestCase):
 def test_public_version_policy_changes_without_stats_or_restart(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);public=root/'public.json';public.write_text('{}');target=root/'version-policy.json';write(target,policy())
   server=Collector(('127.0.0.1',0),root/'data.sqlite',public_config=str(public));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
   client=urllib.request.build_opener(urllib.request.ProxyHandler({}));url='http://127.0.0.1:'+str(server.server_port)+'/v1/app-version'
   try:
    with client.open(url,timeout=2) as r:self.assertEqual(json.load(r),policy());self.assertEqual(r.headers['Cache-Control'],'no-store')
    write(target,policy(0))
    with client.open(url,timeout=2) as r:self.assertEqual(json.load(r)['minimum_version_code'],0)
    with server.db() as db:self.assertEqual(db.execute('SELECT COUNT(*) FROM totals').fetchone()[0],0)
    target.write_text('{broken')
    with self.assertRaises(urllib.error.HTTPError) as failed:client.open(url,timeout=2)
    self.assertEqual(failed.exception.code,503)
   finally:server.shutdown();server.server_close();thread.join()
 def test_operator_rejects_invalid_or_symlink_policy(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);path=root/'policy.json';write(path,policy());before=path.read_bytes()
   with self.assertRaises(ValueError):write(path,policy(1030005,1030004))
   self.assertEqual(path.read_bytes(),before)
   link=root/'link';link.symlink_to(path)
   with self.assertRaises(ValueError):write(link,policy(0))
