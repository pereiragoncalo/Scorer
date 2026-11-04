import unittest
from unittest.mock import patch
from kivy.core.window import Window
from menu_ui import MenuTile,TouchButton
from test_menus import isolated_game,settle


class WorldEditorNavigationTests(unittest.TestCase):
    def test_editor_is_only_in_world_and_back_stays_in_world(self):
        old=Window.size
        try:
            for size in ((320,240),(960,540)):
                Window.size=size
                with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                    c=g.career;c.accept_starting_offer(c.offers[0]);g._career_started=True;g.size=size;g.view='hub';g.draw();settle()
                    original=c.club.uid,c.league_key
                    self.assertNotIn('NAMES EDITOR',{w.text for w in g.walk() if isinstance(w,TouchButton)})
                    g._activate_ui('upgrade');g.draw();settle();self.assertEqual(g.view,'world')
                    editor=next(w for w in g.walk() if isinstance(w,MenuTile) and w.text=='EDITOR')
                    self.assertGreaterEqual(editor.height,48);editor.dispatch('on_release');settle();self.assertEqual(g.view,'editor')
                    back=next(w for w in g.walk() if isinstance(w,TouchButton) and w.text=='BACK');back.dispatch('on_release');settle()
                    self.assertEqual(g.view,'world');self.assertEqual((c.club.uid,c.league_key),original)
                    g._activate_ui('editor');g._on_key_down(None,27,None,'',None);self.assertEqual(g.view,'world')
        finally:Window.size=old

    def test_free_cannot_open_editor(self):
        with patch('edition.WORLD_BUILD',False),isolated_game() as g:
            c=g.career;c.accept_starting_offer(c.offers[0]);g.view='hub';g.draw();settle();g._activate_ui('editor')
            self.assertNotEqual(g.view,'editor')
