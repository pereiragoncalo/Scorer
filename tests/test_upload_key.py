"""Disposable test identity only; never a real production key."""
import hashlib,os,shutil,ssl,stat,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from tools.play.create_upload_key import create_key

class UploadKeyTests(unittest.TestCase):
 def test_existing_key_or_public_certificate_is_never_overwritten(self):
  with tempfile.TemporaryDirectory() as directory:
   key=Path(directory)/'upload.p12';key.write_bytes(b'preserve')
   with self.assertRaises(FileExistsError):create_key(key,'test-password-123')
   self.assertEqual(key.read_bytes(),b'preserve');key.unlink()
   certificate=key.with_suffix('.certificate.pem');certificate.write_text('preserve cert')
   with self.assertRaises(FileExistsError):create_key(key,'test-password-123')
   self.assertFalse(key.exists());self.assertEqual(certificate.read_text(),'preserve cert')
 def test_invalid_password_does_not_create_a_key(self):
  with tempfile.TemporaryDirectory() as directory:
   key=Path(directory)/'upload.p12'
   for password in ('short','a long accented pássword'):
    with self.assertRaises(ValueError):create_key(key,password)
   self.assertFalse(key.exists())
 @unittest.skipUnless(shutil.which('keytool'),'JDK keytool needed')
 def test_real_disposable_pkcs12_public_fingerprint_and_private_permissions(self):
  import subprocess
  run=subprocess.run;password='disposable-test-only-123'
  with tempfile.TemporaryDirectory() as directory:
   key=Path(directory)/'private'/'test-upload.p12'
   with patch('tools.play.create_upload_key.subprocess.run',wraps=run) as calls:
    path,certificate,fingerprint=create_key(key,password,owner='Disposable Test Only')
   self.assertEqual(stat.S_IMODE(path.stat().st_mode),0o600)
   self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode),0o700)
   self.assertEqual(fingerprint,hashlib.sha256(ssl.PEM_cert_to_DER_cert(certificate.read_text())).hexdigest())
   self.assertNotIn('PRIVATE KEY',certificate.read_text())
   for call in calls.call_args_list:self.assertNotIn(password,str(call.args))
   self.assertFalse(list(path.parent.glob('.scorer-key-*')))
