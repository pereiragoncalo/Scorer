import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.metrics import Metrics,dp
from menu_ui import MenuLogo,CareerStartDialog
from test_menus import isolated_game,settle

class StartDialogTests(unittest.TestCase):
    def test_confirmation_fits_content_and_banner_stays_hidden_through_rotation(self):
        old=Window.size;density=Metrics.density
        try:
            Metrics.density=1
            with isolated_game(saved=True) as g:
                Window.size=(1280,640);g.size=Window.size;g.view='start';g.draw();settle()
                self.assertTrue(g.ads.entry_shown);before=g.career.save_path.read_bytes()
                g._activate_ui('new_game');settle();dialog=g._new_game_popup
                self.assertIsInstance(dialog,CareerStartDialog);self.assertFalse(g.ads.entry_shown)
                for size in [(1280,640),(640,360),(360,640)]:
                    Window.size=size;g.size=size;g.draw();settle()
                    self.assertFalse(g.ads.entry_shown)
                    self.assertLessEqual(dialog.width,dp(520)+1)
                    self.assertLessEqual(abs(dialog.height-dialog.panel.minimum_height),1)
                    for b in dialog.buttons.children:
                        self.assertGreaterEqual(b.height,dp(48)-1);self.assertGreaterEqual(b.y,dialog.y);self.assertLessEqual(b.top,dialog.top+1)
                self.assertEqual(g.career.save_path.read_bytes(),before)
                dialog.dismiss();settle();self.assertIsNone(g._new_game_popup)
                self.assertTrue(g.ads.entry_shown)
        finally:Window.size=old;Metrics.density=density
    def test_confirm_never_restores_entry_banner_and_failed_backup_preserves_career(self):
        with isolated_game(saved=True) as g:
            g.view='start';g.draw();settle();before=g.career.save_path.read_bytes()
            g._activate_ui('new_game');settle()
            with patch.object(g.career,'backup_before_new_game',return_value=False):g._start_new_career()
            self.assertEqual(g.view,'start');self.assertEqual(g.career.save_path.read_bytes(),before)
            g._activate_ui('new_game');settle()
            with patch.object(g.ads,'entry_visible',wraps=g.ads.entry_visible) as calls:g._start_new_career();settle()
            self.assertEqual(g.view,'profile');self.assertFalse(g.ads.entry_shown)
            self.assertFalse(any(c.args and c.args[0] is True for c in calls.call_args_list))
    def test_entry_logo_is_top_left_and_world_has_a_native_world_lockup(self):
        old=Window.size;density=Metrics.density
        try:
            Metrics.density=1.6
            for world in (False,True):
                with patch('edition.WORLD_BUILD',world),isolated_game() as g:
                    g.view='start'
                    for size in [(1280,640),(640,360),(360,640)]:
                        Window.size=size;g.size=size;g.draw();settle();e=g._menu.body
                        self.assertIsInstance(e.brand,MenuLogo)
                        self.assertLessEqual(e.brand.x-g.x,dp(12)+1)
                        self.assertLessEqual(g.top-e.brand.top,dp(12)+1)
                        self.assertLessEqual(e.panel.top,e.brand.y+1)
                        self.assertEqual(e.brand.world is not None,world)
                        if world:self.assertEqual(e.brand.world.text,'WORLD')
        finally:Window.size=old;Metrics.density=density
    def test_translated_confirmation_keeps_wrapped_message_and_buttons_inside(self):
        old=Window.size
        try:
            Window.size=(360,640)
            with patch('edition.WORLD_BUILD',True),patch('main.phone_locale_tag',return_value='de-DE'),isolated_game() as g:
                c=g.career;c.accept_starting_offer(c.offers[0]);g.view='start';g.draw();g._activate_ui('new_game');settle();p=g._new_game_popup
                self.assertEqual(p.heading.text,g.i18n.tr('Start a new career?'))
                self.assertLessEqual(p.message.top,p.heading.y+1)
                self.assertGreaterEqual(p.message.y,p.buttons.top-1)
                self.assertLessEqual(p.top,Window.height+1);self.assertGreaterEqual(p.y,0)
        finally:Window.size=old
