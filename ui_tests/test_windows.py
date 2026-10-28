import unittest
from unittest.mock import patch
from kivy.uix.label import Label
from test_menus import isolated_game,settle

class WindowsFreeUITests(unittest.TestCase):
    def test_windows_privacy_does_not_claim_google_sdk_or_offer_video_reward(self):
        with patch('release_settings.DESKTOP_WINDOWS',True,create=True),isolated_game(saved=True) as g:
            g.view='privacy';g.draw();settle()
            texts={w.text for w in g.walk() if isinstance(w,Label)}
            self.assertTrue(any('no Google advertising SDK' in t for t in texts))
            self.assertFalse(any('Google TEST ads' in t for t in texts))
            self.assertIn('ALLOW USAGE STATS',texts)
            g.view='training';g.draw();settle()
            self.assertNotIn('WATCH AD: +1 MORALE',{w.text for w in g.walk() if isinstance(w,Label)})
            self.assertFalse(g.career.world_unlocked)
    def test_android_privacy_and_training_controls_retained(self):
        with isolated_game(saved=True) as g:
            g.view='privacy';g.draw();settle()
            self.assertTrue(any('Google TEST ads' in w.text for w in g.walk() if isinstance(w,Label)))
            g.view='training';g.draw();settle()
            self.assertIn('WATCH AD: +1 MORALE',{w.text for w in g.walk() if isinstance(w,Label)})
