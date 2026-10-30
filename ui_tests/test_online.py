import unittest
from unittest.mock import patch
from test_menus import isolated_game,settle

class OnlineUITests(unittest.TestCase):
    def test_global_screen_reachable_from_scorers_and_offline_join_is_inert(self):
        with isolated_game(saved=True) as g:
            g.view='scorers';g.draw();settle()
            with patch.object(g.leaderboard,'sync') as sync:
                g._activate_ui('leaderboard');settle()
                self.assertEqual(g.view,'leaderboard');sync.assert_not_called()
                g._activate_ui('leaderboard_join');settle()
                self.assertFalse(g.leaderboard.enabled)
                self.assertIn('not configured',g.leaderboard.status)
            self.assertIsNotNone(g._menu.body)
    def test_explicit_join_and_withdraw_have_independent_consent(self):
        with isolated_game(saved=True) as g:
            g.leaderboard.origin='https://stats.example.com'
            with patch.object(g.leaderboard,'sync'):
                g._activate_ui('leaderboard_join');self.assertTrue(g.leaderboard.enabled)
                self.assertFalse(g.usage.enabled)
                g._activate_ui('leaderboard_leave');self.assertFalse(g.leaderboard.enabled)
                self.assertTrue(g.leaderboard.pending_withdrawal)

    def test_main_menu_exposes_leaderboard_without_enabling_any_collection(self):
        from kivy.uix.button import Button
        from kivy.core.window import Window
        for world in (False,True):
            with patch('edition.WORLD_BUILD',world),isolated_game(saved=True) as g:
                g.view='hub';g.draw();settle()
                labels={w.text for w in g.walk() if isinstance(w,Button)}
                self.assertIn('LEADERBOARD',labels)
                self.assertFalse(g.leaderboard.enabled);self.assertFalse(g.usage.enabled)
