import json,tempfile,unittest
from pathlib import Path
from tools.play.verify import verify_catalogue

class BundleCatalogueTests(unittest.TestCase):
 def test_catalogue_size_is_defined_by_exact_reviewed_source(self):
  with tempfile.TemporaryDirectory() as directory:
   reference=Path(directory)/'catalogue.json';raw=json.dumps(dict(version=1,clubs={'one':{'name':'Fixture'}})).encode();reference.write_bytes(raw)
   self.assertEqual(verify_catalogue(raw,reference),1)
   changed=json.dumps(dict(version=1,clubs={'one':{'name':'Changed'}})).encode()
   with self.assertRaisesRegex(ValueError,'differs'):verify_catalogue(changed,reference)
 def test_invalid_catalogue_is_not_accepted_even_if_source_matches(self):
  with tempfile.TemporaryDirectory() as directory:
   reference=Path(directory)/'catalogue.json';raw=b'{"version":1,"clubs":{}}';reference.write_bytes(raw)
   with self.assertRaises(ValueError):verify_catalogue(raw,reference)
