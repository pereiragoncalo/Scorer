import unittest
from unittest.mock import patch
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from test_menus import isolated_game,settle
from anonymous_stats import create_statistics
from main import StrikerApp

class PrivacyRightsUI(unittest.TestCase):
    def test_actual_confirmation_pauses_only_legal_exception_and_back_returns(self):
        with isolated_game(saved=True) as g:
            with patch('anonymous_stats.APP_STATS_MANDATORY',True):g.usage=create_statistics(True,g.career.save_path.parent,endpoint='')
            g.usage.begin_session();self.assertFalse(g.usage.set_enabled(False))
            g.view='privacy';g.draw();g._activate_ui('privacy_rights');settle();self.assertEqual(g.view,'privacy_rights')
            with patch.object(g.privacy_request,'sync') as sync:
                g._activate_ui('rights_object');settle()
                popup=next(w for w in Window.children if isinstance(w,Popup))
                confirm=next(w for w in popup.walk() if isinstance(w,Button) and w.text=='CONFIRM');confirm.trigger_action(duration=0);settle()
                self.assertTrue(g.privacy_request.active);self.assertTrue(g.usage.privacy_hold);self.assertEqual(g.usage.counts,{})
                self.assertFalse(g.usage.record('goals_scored'));sync.assert_called_once()
                StrikerApp._flush_usage(type('App',(),{'root':g})());self.assertEqual(sync.call_count,2)
            g._activate_ui('rights_back');self.assertEqual(g.view,'privacy')
    def test_rights_page_phone_buttons_are_inside_scroll_content(self):
        old=Window.size
        try:
            for size in ((640,360),(320,240)):
                Window.size=size
                with isolated_game() as g:
                    g.size=size;g.view='privacy_rights';g.draw();settle()
                    self.assertIsNotNone(g._menu.scroll)
                    self.assertTrue(any(isinstance(w,Button) and w.text=='SUBMIT PRIVACY REQUEST' for w in g._menu.body.walk()))
                    for w in g._menu.body.walk():
                        if isinstance(w,Button):self.assertGreaterEqual(w.height,47)
        finally:Window.size=old
    def test_confirmed_withdrawal_waits_for_next_opening_before_new_counts(self):
        with isolated_game() as g:
            with patch('anonymous_stats.APP_STATS_MANDATORY',True):g.usage=create_statistics(True,g.career.save_path.parent,endpoint='')
            g.usage.respect_privacy_request(True);g.privacy_request.status='closed';g._privacy_request_done();settle()
            self.assertFalse(g.usage.record('goals_scored'));g.usage.pause_session()
            StrikerApp.on_resume(type('App',(),{'root':g})());self.assertFalse(g.usage.privacy_hold);self.assertEqual(g.usage.counts,{'sessions':1})
