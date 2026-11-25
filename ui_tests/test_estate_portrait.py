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
 def test_new_catalogue_items_can_be_bought_reloaded_and_shown(self):
  from career_life import CATALOGUE_VARIANTS, purchase
  with patch('edition.WORLD_BUILD',True), isolated_game() as game:
   career=retro.RetroSceneTests().prepare(game)
   career.life['balance']=2_000_000
   for key in CATALOGUE_VARIANTS:
    self.assertTrue(purchase(career,key),key)
   self.assertTrue(career.load())
   self.assertEqual(set(CATALOGUE_VARIANTS),set(career.life['owned']))
   portrait=EstatePortrait(career)
   self.assertEqual(portrait.scene_items,{'home':'villa','car':'gt','clothes':'linen'})
   self.assertTrue(portrait.house and portrait.car and portrait.person)
   for category in range(4):
    game.view='shopping';game._shop_category=category;game._shop_pos=2;game.draw();settle()
    from kivy.uix.image import Image
    self.assertTrue(any(widget.texture for widget in game._menu.body.walk()
                        if isinstance(widget,Image)))

 def test_empty_assets_never_display_an_unowned_car_and_all_outfits_are_distinct(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=retro.RetroSceneTests().prepare(g);c.life['owned']={};scene=EstatePortrait(c);self.assertIsNone(scene.car);self.assertEqual(scene.scene_items,{'home':None,'car':None,'clothes':None})
   self.assertEqual(len(set(OUTFITS.values())),5);self.assertEqual(len({bytes(outfit_texture(i).pixels) for i in range(5)}),5)
