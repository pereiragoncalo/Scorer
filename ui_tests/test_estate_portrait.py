import unittest
from unittest.mock import patch
from kivy.clock import Clock
from test_menus import isolated_game,settle
import test_retro_attendance_titles as retro
from estate_portrait import EstatePortrait,OUTFITS,outfit_texture
class EstatePortraitTests(unittest.TestCase):
 def test_photo_tracks_independent_best_owned_items_and_inventory_stays_accessible(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=retro.RetroSceneTests().prepare(g);Clock.unschedule(g.update);c.life['owned']={'mansion':1,'house':1,'utility':1,'designer':1,'casual':1};g.view='possessions';g.draw();settle()
   scene=g._menu.body.portrait;self.assertEqual(scene.scene_items,{'home':'mansion','car':'utility','clothes':'designer'});self.assertIs(scene.person,outfit_texture(4));self.assertIsNotNone(scene.car)
   self.assertEqual(scene.house.mag_filter,'nearest');self.assertEqual(scene.person.mag_filter,'nearest')
   g._activate_ui('collection');g.draw();settle();self.assertTrue(g._menu.body.owned);g._activate_ui('possessions');g.draw();settle();self.assertIsInstance(g._menu.body.portrait,EstatePortrait)
 def test_empty_assets_never_display_an_unowned_car_and_all_outfits_are_distinct(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=retro.RetroSceneTests().prepare(g);c.life['owned']={};scene=EstatePortrait(c);self.assertIsNone(scene.car);self.assertEqual(scene.scene_items,{'home':None,'car':None,'clothes':None})
   self.assertEqual(len(set(OUTFITS.values())),5);self.assertEqual(len({bytes(outfit_texture(i).pixels) for i in range(5)}),5)
