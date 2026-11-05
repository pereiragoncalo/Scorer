"""Verify font selection in real Kivy widgets, including the splash exception."""
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from localization import using
from menu_ui import SplashScreen, MenuLogo, BoundedLabel
from ui_localization import LocalizedInput
from test_menus import isolated_game, settle

class RetroWidgetTests(unittest.TestCase):
    def test_labels_inputs_popup_and_splash_keep_expected_typefaces(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as game:
            game.i18n.choose('en')
            with using(game.i18n):
                label=BoundedLabel(text='TRAINING')
                field=LocalizedInput(text='Gonçalo',hint_text='Player name')
                self.assertEqual(Path(label.font_name).name,'ScorerRetro.ttf')
                self.assertEqual(Path(field.font_name).name,'ScorerRetro.ttf')
                field.text='日本'
                self.assertNotEqual(Path(field.font_name).name,'ScorerRetro.ttf')
                splash=SplashScreen(SimpleNamespace(game=game))
                labels=[w for w in splash.walk() if isinstance(w,BoundedLabel)]
                self.assertTrue(labels)
                self.assertTrue(all(Path(w.font_name).name=='Barlow-Regular.ttf' for w in labels))
                logo=MenuLogo()
                self.assertEqual(logo.image.source,'assets/menu_logo_world.png')
