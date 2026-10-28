import os,unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.metrics import Metrics,dp
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from test_menus import isolated_game,settle
from desktop_dashboard import WindowsDashboard

class MatchdayDashboardTests(unittest.TestCase):
    def populated(self,g):
        g._activate_ui('splash_continue');g._activate_ui('load_game')
        c=g.career
        c.current_league.scorer_goals={f'Test Forward {i} ({club.name})':2+i%5 for i,club in enumerate(c.current_league.clubs)}
        c.current_league.scorer_goals[c.player_name]=3
        g.view='hub';g.draw();settle();return g._menu.body
    def test_windows_fixture_and_scorer_columns_highlight_and_no_scroll(self):
        with patch('release_settings.DESKTOP_WINDOWS',True,create=True),isolated_game(saved=True) as g:
            Window.size=(1366,697);g.size=Window.size;body=self.populated(g)
            self.assertIsInstance(body,WindowsDashboard);self.assertIsNone(g._menu.scroll)
            self.assertEqual(len(body.fixtures.visible_rows),len(body.data.fixtures))
            self.assertEqual(sum(r.focused for r in body.fixtures.visible_rows),1)
            self.assertFalse(any(isinstance(w,ScrollView) for w in body.walk()))
            self.assertGreater(len(body.scorers.visible_rows),5)
            self.assertLess(body.fixtures.right,body.scorers.x)
            labels={w.text for w in body.walk() if isinstance(w,Label)}
            self.assertTrue(any(text.startswith('YOU · #') for text in labels))
            self.assertTrue(body.play.disabled);self.assertGreaterEqual(body.training.height,dp(48))
    def test_paging_and_resize_keep_every_fixture_accessible_without_mutation(self):
        with patch('release_settings.DESKTOP_WINDOWS',True,create=True),isolated_game(saved=True) as g:
            Window.size=(800,600);g.size=Window.size;body=self.populated(g)
            before=g.career.save_path.read_bytes();rng=g.career.rng.getstate()
            for size in ((800,600),(1024,600),(1920,1080),(1366,768)):
                Window.size=size;g.size=Window.size;settle()
                table=body.fixtures;seen=set()
                for page in range(table.page_count):
                    table.page=page;table.user_paged=True;table._trigger();settle()
                    for row in table.visible_rows:
                        self.assertGreater(row.height,0);self.assertGreater(row.width,0)
                        seen.add(tuple(w.text for w in row.children if isinstance(w,Label)))
                self.assertEqual(len(seen),len(body.data.fixtures))
                self.assertGreaterEqual(body.play.height,dp(48));self.assertLessEqual(body.actions.top,body.top+1)
            self.assertEqual(g.career.rng.getstate(),rng);self.assertEqual(g.career.save_path.read_bytes(),before)
    def test_android_keeps_original_dashboard(self):
        with isolated_game(saved=True) as g:
            g.view='hub';g.draw();settle();self.assertNotIsInstance(g._menu.body,WindowsDashboard)
    def test_small_window_uses_compact_hub_and_restores_tables_when_enlarged(self):
        with patch('release_settings.DESKTOP_WINDOWS',True,create=True),isolated_game(saved=True) as g:
            Window.size=(1366,697);g.size=Window.size;self.populated(g)
            Window.size=(640,360);g.size=Window.size;g.draw();settle()
            self.assertNotIsInstance(g._menu.body,WindowsDashboard);self.assertIsNone(g._menu.scroll)
            Window.size=(1366,697);g.size=Window.size;g.draw();settle()
            self.assertIsInstance(g._menu.body,WindowsDashboard)
