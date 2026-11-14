import hashlib,unittest
from pathlib import Path
from types import SimpleNamespace
from PIL import Image
from club_profiles import ground,stadium_variant,stadium_capacity,profile

class CapacityArchitecture(unittest.TestCase):
 def test_roof_is_strictly_above_ten_thousand_and_variants_match_tiers(self):
  for capacity in (250,5000,10000,10001,25000,25001,40000,40001,80000,80001,150000):
   g=ground(capacity);self.assertEqual(g.has_roof,capacity>10000)
   self.assertEqual(g.portrait_variant,stadium_variant(capacity))
   self.assertEqual(g.tiers,2 if g.portrait_variant in ('double','major')else 1)
  self.assertEqual([stadium_variant(c)for c in (5000,10000,25000,40000,80000,150000)],['local','compact','covered','bowl','double','major'])
 def test_modelled_venues_do_not_invent_factual_capacity(self):
  club=SimpleNamespace(uid='unknown-stadium-fixture',rating=56)
  self.assertIsNone(profile(club)['capacity']);self.assertTrue(ground(stadium_capacity(club)).has_roof)
  self.assertIsNone(profile(club)['capacity'])
 def test_original_pixel_assets_are_distinct_small_rgba_and_include_both_club_colour_slots(self):
  root=Path('assets/sprites/scene');digests=set()
  for name in ('local','compact','covered','bowl','double','major'):
   path=root/('stadium_'+name+'.png');digests.add(hashlib.sha256(path.read_bytes()).digest())
   with Image.open(path)as im:
    self.assertEqual(im.mode,'RGBA');self.assertEqual(im.size,(320,180));self.assertIn(bytes((40,80,210,255)),im.tobytes())
  self.assertEqual(len(digests),6)
  for name,size in (('roof',(128,32)),('roof_fascia',(128,16)),('wall',(128,16))):
   with Image.open(root/('stadium_'+name+'.png'))as im:self.assertEqual(im.size,size);self.assertEqual(im.mode,'RGBA')
