import json,unittest
from pathlib import Path
from tools.play.local_club_names import norm,COUNTRY_FAMILY
from tools.play.city_colour_names import build
from tools.play.fictional_clubs import shipping_data,verify_fictional_data
ROOT=Path(__file__).resolve().parents[1]

class LocalClubNameTests(unittest.TestCase):
 def test_all_countries_covered_reproducibly_with_unique_country_appropriate_names(self):
  local=json.loads((ROOT/'assets/data/fictional_names.json').read_text())
  self.assertEqual(build(ROOT)[0],local)
  self.assertEqual(len({r['country'] for r in local['clubs'].values()}),212)
  used={}
  for row in local['clubs'].values():
   self.assertEqual(row['family'],COUNTRY_FAMILY[row['country']]);self.assertTrue(2<=len(row['name'])<=56)
   keys=used.setdefault(row['country'],set());self.assertNotIn(norm(row['name']),keys);keys.add(norm(row['name']))
   if row['country']=='Portugal':
    self.assertNotIn('Valedouro',row['name'])
    self.assertFalse(any(word in row['name'] for word in ('Wanderers','United','Town','Rovers','Athletic','City')))
 def test_old_english_fallback_fails_shipping_gate(self):
  expected=shipping_data(ROOT/'assets/data')['world_clubs'];uid=next(iter(expected['clubs']));expected['clubs'][uid]['name']=expected['clubs'][uid]['canonical']
  with self.assertRaisesRegex(ValueError,'Non-fictional'):verify_fictional_data('world_clubs',json.dumps(expected),ROOT/'assets/data')
 def test_real_reference_labels_are_not_used_and_core_keys_stay_stable(self):
  data=shipping_data(ROOT/'assets/data');original=json.loads((ROOT/'assets/data/world_clubs.json').read_text())['clubs'];source=json.loads((ROOT/'docs/data/world_club_provenance.json').read_text())['clubs']
  banned={norm(r['reference']) for r in source.values() if r.get('reference')}|{norm(r['name']) for r in original.values()}
  for uid,row in data['world_clubs']['clubs'].items():
   self.assertEqual(row['canonical'],data['fictional_names']['clubs'][uid]['canonical']);self.assertNotIn(norm(row['name']),banned)

 def test_every_current_club_and_legacy_uid_has_local_display_name(self):
  import tempfile,os
  from unittest.mock import patch
  from career import CareerMode
  class Access:
   def has_world_access(self):return True
  rows=shipping_data(ROOT/'assets/data')['world_clubs']['clubs']
  with tempfile.TemporaryDirectory() as directory,patch.dict(os.environ,STRIKER_SAVE_DIR=directory):
   for real_formats in (True,False):
    career=CareerMode(Access(),autoload=False,save_slot='world',domestic_formats=real_formats)
    for league in career.leagues.values():
     for club in league.clubs:
      self.assertIn(club.uid,rows);self.assertEqual(rows[club.uid]['canonical'],club.name)
