import unittest
from unittest.mock import patch
from kivy.uix.label import Label
from test_menus import isolated_game,settle

class WindowsFreeUITests(unittest.TestCase):
    def test_windows_privacy_does_not_claim_google_sdk_or_offer_video_reward(self):
        with patch('release_settings.DESKTOP_WINDOWS',True,create=True),isolated_game(saved=True) as g:
            g.view='privacy';g.draw();settle()
            texts={w.text for w in g.walk() if isinstance(w,Label)}
            self.assertTrue(any('no advertising' in t for t in texts))
            self.assertFalse(any('Google TEST ads' in t for t in texts))
            self.assertIn('ALLOW USAGE STATS',texts)
            g.view='training';g.draw();settle()
            self.assertNotIn('WATCH AD: +1 MORALE',{w.text for w in g.walk() if isinstance(w,Label)})
            self.assertFalse(g.career.world_unlocked)
    def test_android_is_adfree_and_has_no_reward_control(self):
        with isolated_game(saved=True) as g:
            g.view='privacy';g.draw();settle()
            self.assertTrue(any('no advertising' in w.text for w in g.walk() if isinstance(w,Label)))
            g.view='training';g.draw();settle()
            self.assertNotIn('WATCH AD: +1 MORALE',{w.text for w in g.walk() if isinstance(w,Label)})
