import json,tempfile,unittest
from pathlib import Path
from tools.play.build_public_site import build,ROOT

class PublicSiteTests(unittest.TestCase):
 def test_public_only_english_final_html_with_site_relative_links(self):
  with tempfile.TemporaryDirectory() as directory:
   site=build(Path(directory)/'site')
   files={str(p.relative_to(site)) for p in site.rglob('*') if p.is_file()}
   self.assertEqual(files,{'.nojekyll','index.html','privacy/index.html','terms/index.html','delete/index.html'})
   for name in ('privacy','terms','delete'):
    text=(site/name/'index.html').read_text()
    self.assertIn('lang="en"',text)
    self.assertIn('Gonçalo Pereira',text)
    self.assertIn('goncalo@clemir.com',text)
    self.assertIn('href="/Scorer/privacy/"',text)
    self.assertNotIn('href="/privacy"',text)
    self.assertNotIn('<script',text.lower())
    self.assertNotIn('DRAFT UNDER REVIEW',text)
   privacy=(site/'privacy/index.html').read_text()
   for expected in ('off by default','Career category','GitHub Pages','github-general-privacy-statement'):
    self.assertIn(expected,privacy)
 def test_draft_cannot_be_deployed(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);config=json.loads((ROOT/'server/public.world.policy.json').read_text());config['publication_status']='draft'
   file=root/'draft.json';file.write_text(json.dumps(config))
   with self.assertRaises(ValueError):build(root/'site',file)
   self.assertFalse((root/'site').exists())
