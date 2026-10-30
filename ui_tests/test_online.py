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
                g._activate_ui('leaderboard_join');self.assertFalse(g.leaderboard.enabled)
                self.assertIsNotNone(g._records_popup)
                g._activate_ui('leaderboard_confirm_join');self.assertTrue(g.leaderboard.enabled)
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

    def test_records_layout_has_separate_controls_table_and_pages_at_phone_sizes(self):
        from kivy.core.window import Window
        from kivy.metrics import Metrics,dp
        from kivy.uix.scrollview import ScrollView
        from menu_ui import SeasonRecordsScreen
        old=Metrics.density
        try:
            for density,size in ((1,(640,360)),(1.64,(1280,591)),(1,(320,240)),(1,(1366,697))):
                Metrics.density=density;Window.size=size
                with isolated_game(saved=True) as g:
                    g.size=size;g.view='leaderboard'
                    g.leaderboard.entries=[dict(edition='free',country='Scorer',division=1,season=2026,player='João Silva '+str(i),team='União Lisboa',matches=46,goals=30-i) for i in range(20)]
                    g.draw();settle();screen=g._menu.body
                    self.assertIsInstance(screen,SeasonRecordsScreen)
                    self.assertFalse(any(isinstance(w,ScrollView) for w in g._menu.walk()))
                    self.assertLessEqual(screen.table.top,screen.actions.y+1)
                    self.assertGreaterEqual(screen.table.controls.height,dp(48)-1)
                    for row in screen.table.lines.children:
                        self.assertGreaterEqual(row.y,screen.table.controls.top-1)
                        self.assertLessEqual(row.top,screen.table.head.y+1)
                    from kivy.uix.boxlayout import BoxLayout
                    records=[w for w in screen.table.lines.children if isinstance(w,BoxLayout)]
                    if records:self.assertLessEqual(abs(max(w.top for w in records)-screen.table.head.y),dp(5))
                    if len(screen.table.rows)>screen.table.page_size:
                        screen.table.move(1);settle();self.assertEqual(screen.table.page,1)
        finally:Metrics.density=old
