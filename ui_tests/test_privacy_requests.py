import unittest
from unittest.mock import patch
from kivy.uix.button import Button
from kivy.core.window import Window
from test_menus import isolated_game,settle
from anonymous_stats import create_statistics
from main import StrikerApp

class LaunchNoticeUI(unittest.TestCase):
    def test_every_launch_notice_has_only_ok_and_not_ok_and_reject_exits_directly(self):
        old=Window.size
        try:
            for size in ((640,360),(320,240),(360,640)):
                Window.size=size
                with patch('edition.WORLD_BUILD',True),isolated_game(saved=True) as g:
                    g.i18n.choose('pt');g.size=size;g.family.acknowledge()
                    with patch('anonymous_stats.APP_STATS_MANDATORY',True):g.usage=create_statistics(True,g.career.save_path.parent,endpoint='')
                    g._activate_ui('splash_continue');g.draw();settle()
                    self.assertEqual(g.view,'data_notice');self.assertFalse(g.usage.delivery_ready)
                    buttons=[w for w in g._menu.walk() if isinstance(w,Button)]
                    self.assertEqual({w.text for w in buttons},{'CONCORDO','NÃO CONCORDO'})
                    for w in buttons:
                        self.assertGreaterEqual(w.height,48);self.assertGreaterEqual(w.y,g.y);self.assertLessEqual(w.top,g.top+1)
                    g.usage.begin_session()
                    app=type('App',(),{'stop':lambda self:None})()
                    with patch('main.App.get_running_app',return_value=app),patch.object(app,'stop') as stop:
                        next(w for w in buttons if w.text=='NÃO CONCORDO').trigger_action(duration=0);settle();stop.assert_called_once()
                    self.assertTrue(g.usage.notice_rejected);self.assertEqual(g.usage.counts,{})
                    StrikerApp.on_stop(type('App',(),{'root':g})());self.assertEqual(g.usage.counts,{})
        finally:Window.size=old
    def test_world_submenu_exposes_editor_and_import_at_top(self):
        import edition
        with patch('edition.WORLD_BUILD',True),isolated_game(saved=True) as g:
            g.view='hub';g.draw();settle()
            self.assertFalse(any(isinstance(w,Button) and w.text=='EDITOR' for w in g.walk()))
            g._activate_ui('upgrade');g.draw();settle();self.assertEqual(g.view,'world')
            editor=next(w for w in g.walk() if isinstance(w,Button) and w.text=='EDITOR')
            editor.trigger_action(duration=0);settle();self.assertEqual(g.view,'editor')
            self.assertTrue(any(isinstance(w,Button) and w.text=='IMPORT NAMES FILE' for w in g.walk()))
