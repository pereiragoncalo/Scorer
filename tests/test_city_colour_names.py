import json,unittest
from pathlib import Path
from tools.play.city_colour_names import build,colour
ROOT=Path(__file__).resolve().parents[1]

class CityColourTests(unittest.TestCase):
 def test_city_colour_examples_and_current_kit_identity_are_exact(self):
  data,audit=build(ROOT);by_real={r['reference']:r for r in audit if r['status'].startswith('current')}
  expected={'Benfica':'Lisboa Vermelho','Sporting CP':'Lisboa Verde','Porto':'Porto Azul','Flamengo':'Rio de Janeiro Vermelho-Preto','Vitória BA':'Salvador Vermelho-Preto','Millwall':'Bermondsey Blue','Benfica B':'Lisboa Vermelho B','Porto B':'Porto Azul B'}
  for real,name in expected.items():self.assertEqual(by_real[real]['alias'],name)
  proof=json.loads((ROOT/'docs/data/club_kits.provenance.json').read_text())['clubs']
  self.assertEqual(sum(r['status'].startswith('current') for r in audit),378)
  sarandi=next(r for r in audit if r['reference']=='Arsenal' and r['country']=='Argentina');self.assertEqual(sarandi['alias'],'Sarandí Celeste-Rojo')
  for row in by_real.values():self.assertEqual(row['palette'],proof[row['uid']]['home'])
 def test_obsolete_source_does_not_override_current_real_identity(self):
  data,audit=build(ROOT);by_real={r['reference']:r for r in audit if r['status'].startswith('current')}
  self.assertTrue(by_real['Famalicão']['alias'].startswith('Famalicão '))
  self.assertTrue(by_real['Marítimo']['alias'].startswith('Funchal '))
  self.assertTrue(by_real['Moreirense']['alias'].startswith('Moreira de Cónegos '))
 def test_dark_navy_is_blue_and_black_stays_black(self):
  self.assertEqual(colour('000F36'),'Blue');self.assertEqual(colour('000000'),'Black')
 def test_durable_registry_has_no_official_club_labels_or_reference_material(self):
  data,audit=build(ROOT)
  self.assertEqual(data['identity'],'city-colour-v1')
  for uid,row in data['clubs'].items():self.assertEqual(set(row),{'country','family','name','canonical'})
  source=json.loads((ROOT/'docs/data/name-packs/Scorer-World-Real-Names-0.9.10.json').read_text())['clubs']
  for uid,name in source.items():self.assertNotEqual(data['clubs'][uid]['name'],name)
