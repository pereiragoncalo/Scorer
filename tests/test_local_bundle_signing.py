"""Disposable cryptographic fixture, not a runnable Android bundle."""
import shutil,tempfile,unittest,zipfile
from pathlib import Path
from tools.play.create_upload_key import create_key
from tools.play.sign_local_bundle import sign_bundle,digest

class LocalBundleSigningTests(unittest.TestCase):
 def test_existing_output_is_never_changed(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);out=root/'signed.aab';out.write_text('preserve')
   with self.assertRaises(FileExistsError):sign_bundle(root/'input',out,root/'key','never-used','a'*64,'b'*64)
   self.assertEqual(out.read_text(),'preserve')
 @unittest.skipUnless(shutil.which('jarsigner') and shutil.which('keytool'),'Full JDK needed')
 def test_real_signature_expected_certificate_and_input_hash(self):
  import subprocess
  from unittest.mock import patch
  run=subprocess.run;password='disposable-signing-only-123'
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);source=root/'input.aab'
   with zipfile.ZipFile(source,'w') as archive:
    archive.writestr('BundleConfig.pb',b'fixture');archive.writestr('base/manifest/AndroidManifest.xml',b'fixture')
   key,cert,sha=create_key(root/'private'/'fixture.p12',password,owner='Disposable Signing Test')
   with self.assertRaisesRegex(ValueError,'bundle SHA256'):sign_bundle(source,root/'bad-input.aab',key,password,'0'*64,sha)
   with self.assertRaisesRegex(ValueError,'certificate'):sign_bundle(source,root/'bad-cert.aab',key,password,digest(source),'0'*64)
   with patch('tools.play.sign_local_bundle.subprocess.run',wraps=run) as calls:
    result=sign_bundle(source,root/'signed.aab',key,password,digest(source),sha)
   self.assertEqual(result,digest(root/'signed.aab'))
   for call in calls.call_args_list:self.assertNotIn(password,str(call.args))
   self.assertFalse(list(root.glob('.scorer-sign-*')))
   self.assertFalse((root/'bad-input.aab').exists());self.assertFalse((root/'bad-cert.aab').exists())
   with self.assertRaisesRegex(ValueError,'already signed'):sign_bundle(root/'signed.aab',root/'again.aab',key,password,result,sha)
