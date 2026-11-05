import time,unittest,tempfile,json
from pathlib import Path
from unittest.mock import patch
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from test_menus import isolated_game,settle
from anonymous_stats import create_statistics
from main import StrikerApp

class PublicationUITests(unittest.TestCase):
    def test_compact_notice_keeps_disclosure_and_help_paragraphs_are_justified(self):
        from menu_ui import LaunchNotice,FlowLabel
        from online_safety import NOTICE_TEXT
        from kivy.metrics import dp
        with isolated_game() as g:
            g.size=(1280,591);g.view='data_notice';g.draw();settle()
            notice=next(w for w in g.walk() if isinstance(w,LaunchNotice))
            self.assertLess(notice.panel.width,notice.width)
            self.assertEqual(notice.message.halign,'justify')
            self.assertEqual(notice.message.text,NOTICE_TEXT)
            self.assertLessEqual(notice.message.font_size,dp(13))
            for page in range(4):
                g.view='help';g.help_page=page;g.draw();settle()
                paragraphs=[w for w in g.walk() if isinstance(w,FlowLabel) and len(w.text)>70]
                self.assertTrue(paragraphs)
                self.assertTrue(all(w.halign=='justify' for w in paragraphs))

    def test_first_run_notice_precedes_delivery_and_cannot_be_bypassed_by_back(self):
        with isolated_game(saved=True) as g:
            with patch('anonymous_stats.APP_STATS_MANDATORY',True):g.usage=create_statistics(False,g.career.save_path.parent,endpoint='https://stats.example.com/v1/usage')
            with patch.object(g.usage,'_sender',return_value=False) as sender:
                app=type('App',(),{'root':g})();StrikerApp.on_start(app)
                try:
                    g._activate_ui('splash_continue');self.assertEqual(g.view,'data_notice');self.assertFalse(g.usage.delivery_ready)
                    g.usage.flush_async();sender.assert_not_called()
                    g._activate_ui('notice_continue');self.assertEqual(g.view,'start');self.assertTrue(g.usage.delivery_ready);self.assertTrue(g.family.notice_seen)
                    self.assertTrue(g.usage.enabled);self.assertFalse(g.usage.set_enabled(False))
                finally:StrikerApp.on_stop(app)
    def test_guardian_setup_unlock_and_disable_stops_publication_without_disabling_usage(self):
        with isolated_game(saved=True) as g:
            with patch('anonymous_stats.APP_STATS_MANDATORY',True):g.usage=create_statistics(False,g.career.save_path.parent,endpoint='')
            with patch.object(g.leaderboard,'sync') as sync:
                g._activate_ui('leaderboard');self.assertEqual(g.view,'leaderboard');sync.assert_not_called()
                g._activate_ui('leaderboard_join');self.assertEqual(g.view,'family');sync.assert_not_called()
                g._safety_draft=dict(birth='2018-01-01',pin='123456',confirm='123456');g._activate_ui('adult_setup');self.assertFalse(g.family.social)
                g._safety_draft=dict(birth='1980-01-01',pin='123456',confirm='123456');g._activate_ui('adult_setup');self.assertTrue(g.family.social)
                g._activate_ui('safety_back');g.leaderboard.origin='https://stats.example.com'
                g._activate_ui('leaderboard_join');self.assertIsNotNone(g._records_popup)
                g._activate_ui('leaderboard_confirm_join');self.assertTrue(g.leaderboard.enabled);self.assertEqual(g.leaderboard.terms_version,1)
                g._activate_ui('family_controls');g._safety_draft={'pin':'123456'};g._activate_ui('adult_disable')
                self.assertFalse(g.family.social);self.assertFalse(g.leaderboard.enabled);self.assertTrue(g.leaderboard.pending_withdrawal)
                self.assertTrue(sync.call_args.kwargs.get('withdraw'))
                self.assertTrue(g.usage.enabled);self.assertTrue(g.usage.mandatory);self.assertFalse(g.usage.set_enabled(False))
    def test_phone_safety_forms_wrap_and_actions_fit_scroll_content(self):
        old=Window.size
        try:
            for size in ((640,360),(320,240)):
                Window.size=size
                with isolated_game(saved=True) as g:
                    g.size=size
                    for view in ('family','record_safety','privacy'):
                        g.view=view;g.draw();settle();self.assertIsNotNone(g._menu.scroll)
                        for w in g._menu.body.walk():
                            if isinstance(w,Button):self.assertGreaterEqual(w.height,48-1)
        finally:Window.size=old
    def test_translated_disclosures_in_world_and_untranslated_opaque_names(self):
        import edition
        from online_safety import NOTICE_TEXT,TERMS_TEXT
        with patch('edition.WORLD_BUILD',True),isolated_game(saved=True) as g:
            keys=json.loads(Path('docs/play/publication_translation_keys.json').read_text())
            for language in ('pt','es','de','it','ko','ja','zh','vi'):
                g.i18n.choose(language)
                for key in keys:self.assertNotEqual(g.i18n.tr(key),key,(language,key))
            g.i18n.choose('pt');g.view='data_notice';g.draw();settle()
            self.assertIn('ANTES DE JOGAR',{w.text for w in g.walk() if isinstance(w,Label)})

    def test_pending_removal_retries_while_public_access_remains_locked(self):
        with isolated_game(saved=True) as g:
            g.family.social=False;g.leaderboard.pending_withdrawal=True
            with patch.object(g.leaderboard,'sync') as sync:
                StrikerApp._flush_usage(type('App',(),{'root':g})())
                sync.assert_called_once_with(g.career,False,withdraw=True)
                self.assertFalse(g.family.social);self.assertFalse(g.leaderboard.enabled)

    def test_help_contains_only_gameplay_guidance(self):
        with isolated_game() as g:
            g.view='help';g.help_page=3;g.draw();settle()
            text=' '.join(w.text for w in g.walk() if isinstance(w,Label))
            self.assertIn('names editor',text);self.assertNotIn('adult-managed',text)
            self.assertNotIn('Usage counts',text)
            self.assertNotIn('training ads',text);self.assertNotIn('earn +1 morale',text)
