"""Measure full new-career captions using real Kivy text rendering."""
import unittest
from unittest.mock import patch
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
from kivy.metrics import Metrics,dp
from menu_ui import CreationTile
from test_menus import isolated_game,settle

class CreationFitTests(unittest.TestCase):
 def test_full_creation_captions_fit_landscape_portrait_and_large_density(self):
  old=Window.size;density=Metrics.density
  try:
   with patch('edition.WORLD_BUILD',True),isolated_game() as g:
    g._select_career_mode('world')
    g._activate_ui('splash_continue');g._activate_ui('new_game');g.draw();settle()
    for density_value,size in [(1,(640,360)),(1.6,(1280,640)),(1.6,(640,360)),(1.6,(360,640)),(3,(1920,1080))]:
     Metrics.density=density_value;Window.size=size;g.size=size
     for language in ('en','pt','de'):
      g.i18n.choose(language);g.draw();settle();f=g._menu.body
      f.draft.update(nationality='Bosnia and Herzegovina',country='Saint Vincent and the Grenadines');f._country_labels()
      f.favourite.text='Junipermere Wanderers';settle()
      for button in [*f.choices.children,*f.actions.children]:
       with self.subTest(size=size,density=density_value,language=language,text=button.text):
        self.assertIsInstance(button,CreationTile);self.assertFalse(button.shorten)
        self.assertGreaterEqual(button.height,dp(48)-1)
        self.assertGreaterEqual(button.x,f.panel.x-1);self.assertLessEqual(button.right,f.panel.right+1)
        self.assertGreaterEqual(button.y,f.panel.y-1);self.assertLessEqual(button.top,f.panel.top+1)
        measure=CoreLabel(text=button.text,text_size=(button.width-dp(16),None),font_name=button.font_name,font_size=button.font_size,bold=button.bold,line_height=button.line_height);measure.refresh()
        self.assertLessEqual(measure.texture.size[1],button.height-dp(12)+1)
     if density_value==1.6 and size==(1280,640):
      g.i18n.choose('en');g.draw();settle();g.export_to_png('/workspace/striker-runtime/creation-fix-render.png')
  finally:Metrics.density=density;Window.size=old
