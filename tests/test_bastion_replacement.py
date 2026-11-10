import hashlib,io,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from tools.play import bastion_bundle_1030001 as helper

class BastionReplacementTests(unittest.TestCase):
 def test_corrupt_download_is_rejected_before_signing(self):
  with tempfile.TemporaryDirectory() as directory,patch.object(helper.urllib.request,'urlopen',return_value=io.BytesIO(b'wrong')):
   with self.assertRaisesRegex(ValueError,'checksum'):helper.download('fixture',Path(directory)/'bundle','0'*64)
 def test_existing_output_is_never_overwritten_or_downloaded(self):
  with tempfile.TemporaryDirectory() as directory:
   output=Path(directory)/'signed.aab';output.write_bytes(b'previous')
   with patch.object(helper,'OUTPUT',output),patch.object(helper,'download') as download:
    with self.assertRaisesRegex(ValueError,'already exists'):helper.main()
    download.assert_not_called();self.assertEqual(output.read_bytes(),b'previous')
 def test_signing_reuses_pinned_owner_certificate_and_existing_key(self):
  with tempfile.TemporaryDirectory() as directory:
   key=Path(directory)/'existing.p12';key.write_bytes(b'fixture only')
   output=Path(directory)/'signed.aab'
   with patch.object(helper,'KEY',key),patch.object(helper,'OUTPUT',output),patch.object(helper,'download'),patch.object(helper.subprocess,'run') as run:
    helper.main();argv=run.call_args.args[0]
    self.assertEqual(argv[argv.index('--keystore')+1],str(key));self.assertEqual(argv[argv.index('--certificate-sha256')+1],helper.CERT)
    self.assertEqual(argv[argv.index('--input-sha256')+1],helper.BUNDLE_SHA)
