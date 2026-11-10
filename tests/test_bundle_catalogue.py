import io,json,os,tarfile,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
from tools.play.verify import verify_catalogue
from tools.play.fictional_clubs import shipping_data,stage_fictional_clubs,verify_fictional_data
ROOT=Path(__file__).resolve().parents[1]

class BundleCatalogueTests(unittest.TestCase):
 def test_real_overlay_is_rejected_even_when_identical_to_source(self):
  path=ROOT/'assets/data/world_clubs.json'
  with self.assertRaisesRegex(ValueError,'Non-fictional'):verify_catalogue(path.read_bytes(),path)
 def test_every_shipped_name_is_canonical_and_all_uids_colours_survive(self):
  source=json.loads((ROOT/'assets/data/world_clubs.json').read_text());data=shipping_data(ROOT/'assets/data')
  clubs=data['world_clubs']['clubs'];self.assertTrue(set(source['clubs']).issubset(clubs))
  local=json.loads((ROOT/'assets/data/fictional_names.json').read_text())['clubs']
  for uid,row in clubs.items():
   self.assertEqual(row['name'],local[uid]['name']);self.assertEqual(row['canonical'],source['clubs'].get(uid,local[uid])['canonical'])
   self.assertEqual(row.get('colours'),source['clubs'].get(uid,{}).get('colours'))
  self.assertEqual(verify_catalogue(json.dumps(data['world_clubs']).encode(),ROOT/'assets/data/world_clubs.json'),len(local))
  for row in data['club_profiles']['clubs'].values():
   self.assertEqual(set(row),{'club','capacity','shirt_pattern'})
  for row in data['league_status']['clubs'].values():
   self.assertTrue(all('name' not in season for season in row['seasons']))
 def test_real_profile_or_rating_name_is_rejected(self):
  for name in ('club_profiles','league_status'):
   with self.assertRaisesRegex(ValueError,'Non-fictional'):
    verify_fictional_data(name,(ROOT/'assets/data'/(name+'.json')).read_bytes(),ROOT/'assets/data')
 def test_staging_is_idempotent_and_preserves_capacities_patterns_and_ratings(self):
  import shutil
  with tempfile.TemporaryDirectory() as directory:
   target=Path(directory)
   for name in ('world_clubs','club_profiles','league_status','fictional_names'):shutil.copyfile(ROOT/'assets/data'/(name+'.json'),target/(name+'.json'))
   before=json.loads((target/'club_profiles.json').read_text());status=json.loads((target/'league_status.json').read_text())
   stage_fictional_clubs(target);first={p.name:p.read_bytes() for p in target.glob('*.json')};stage_fictional_clubs(target)
   self.assertEqual(first,{p.name:p.read_bytes() for p in target.glob('*.json')})
   profiles=json.loads((target/'club_profiles.json').read_text())['clubs']
   for uid,row in before['clubs'].items():
    if uid in profiles:self.assertEqual(row.get('capacity'),profiles[uid]['capacity'])
   from club_kits import shirt_pattern
   from types import SimpleNamespace
   with patch('club_profiles.catalogue',return_value=profiles):
    for uid,row in before['clubs'].items():
     expected='plain' if row['club']=='Benfica' else None
     if expected and uid in profiles:self.assertEqual(shirt_pattern(SimpleNamespace(uid=uid)),expected)
   for uid,row in json.loads((target/'league_status.json').read_text())['clubs'].items():
    self.assertEqual(row['rating'],status['clubs'][uid]['rating']);self.assertEqual(len(row['seasons']),len(status['clubs'][uid]['seasons']))
 def test_released_1030000_bundle_fails_new_name_gate(self):
  artifact=ROOT.parent/'Scorer-World-1.0-unsigned.aab'
  if not artifact.exists():artifact=Path('/tmp/scorer-signing-archives/Scorer-World-1.0-unsigned.aab')
  if not artifact.exists():self.skipTest('Old artifact not available')
  with zipfile.ZipFile(artifact) as z:
   with tarfile.open(fileobj=io.BytesIO(z.read(next(n for n in z.namelist() if n.endswith('assets/private.tar'))))) as payload:
    member=next(m for m in payload if m.name.endswith('assets/data/world_clubs.json'))
    with self.assertRaisesRegex(ValueError,'Non-fictional'):verify_catalogue(payload.extractfile(member).read(),ROOT/'assets/data/world_clubs.json')
