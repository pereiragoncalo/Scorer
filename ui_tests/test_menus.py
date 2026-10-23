"""Real Kivy layout and input tests; run with the development Kivy interpreter."""
import os
import tempfile
import unittest
from unittest.mock import patch

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, Metrics
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.tests.common import UnitTestTouch

from main import StrikerGame
from menu_ui import TouchButton


def settle():
    for _ in range(18):
        Clock.tick()
        Clock.tick_draw()


class MenuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.env = patch.dict(os.environ, STRIKER_SAVE_DIR=cls.temp.name)
        cls.env.start()
        cls.game = StrikerGame()
        Window.add_widget(cls.game)
        cls.game.career.accept_starting_offer(cls.game.career.offers[0])

    @classmethod
    def tearDownClass(cls):
        Clock.unschedule(cls.game.update)
        Window.remove_widget(cls.game)
        Window.unbind(on_key_down=cls.game._on_key_down)
        cls.env.stop()
        cls.temp.cleanup()

    def test_all_menu_layouts_at_phone_sizes(self):
        for size in ((640, 360), (800, 360), (960, 540), (1280, 720), (360, 800), (320, 240)):
            Window.size = size
            self.game.size = size
            for view in ('offers', 'hub', 'training', 'standings', 'scorers', 'calendar', 'agent'):
                with self.subTest(size=size, view=view):
                    self.game.view = view
                    self.game.draw()
                    settle()
                    menu = self.game._menu
                    self.assertIsNotNone(menu)
                    self.assertGreater(menu.scroll.height, 0)
                    for widget in menu.walk():
                        if isinstance(widget, TouchButton):
                            self.assertGreaterEqual(widget.height, dp(52) - 1)
                            self.assertLessEqual(widget.texture_size[0], widget.width - dp(24) + 2)
                            self.assertLessEqual(widget.texture_size[1], widget.height - dp(20) + 2)
                        elif isinstance(widget, Label) and not widget.shorten:
                            self.assertLessEqual(widget.texture_size[0], widget.width + 2)
                            self.assertLessEqual(widget.texture_size[1], widget.height + 2)
                    for row in menu.walk():
                        if type(row) is BoxLayout and row.children and all(type(child) is Label for child in row.children):
                            for cell in row.children:
                                self.assertGreaterEqual(cell.x, row.x - 1)
                                self.assertLessEqual(cell.right, row.right + 1)
                    for child in menu.children:
                        self.assertGreaterEqual(child.y, menu.y - 1)
                        self.assertLessEqual(child.top, menu.top + 1)

    def test_primary_play_button_visible_on_compact_phone(self):
        Window.size = (640, 360)
        self.game.size = Window.size
        self.game.view = 'hub'
        self.game.draw()
        settle()
        menu = self.game._menu
        play = next(w for w in menu.walk() if isinstance(w, TouchButton) and w.text == 'JOGAR')
        x, y = play.to_window(*play.center)
        self.assertGreater(y, menu.scroll.y)
        self.assertLess(y, menu.scroll.top)

    def test_large_system_font_stays_in_menu_bounds(self):
        previous = Metrics.fontscale
        try:
            Metrics.fontscale = 1.6
            Window.size = (640, 360)
            self.game.size = Window.size
            self.game.view = 'hub'
            self.game.draw()
            self.game._menu._signature = None
            self.game.draw()
            settle()
            menu = self.game._menu
            self.assertGreater(menu.scroll.height, 0)
            for widget in menu.walk():
                if isinstance(widget, Label):
                    self.assertGreater(widget.texture_size[1], 0)
                    self.assertLessEqual(widget.texture_size[0], widget.width + 2)
                    self.assertLessEqual(widget.texture_size[1], widget.height + 2)
        finally:
            Metrics.fontscale = previous
            self.game._menu._signature = None
            self.game.draw()
            settle()

    def test_tap_navigation_does_not_shoot(self):
        Window.size = (960, 540)
        self.game.size = Window.size
        self.game.view = 'hub'
        self.game.draw()
        settle()
        menu = self.game._menu
        button = next(w for w in menu.walk() if isinstance(w, TouchButton) and w.text == 'CLASSIFICAÇÃO')
        # Native widget callback, followed by independent real touch on header Back.
        button.dispatch('on_release')
        settle()
        self.assertEqual(self.game.view, 'standings')
        back = next(w for w in self.game._menu.walk() if isinstance(w, TouchButton) and w.text == 'VOLTAR')
        touch = UnitTestTouch(*back.center)
        touch.touch_down()
        touch.touch_up()
        settle()
        self.assertEqual(self.game.view, 'hub')

    def test_exit_cancel_and_save_before_stop(self):
        self.game.view = 'hub'
        self.game.draw()
        self.game._request_exit()
        settle()
        self.assertIsNotNone(self.game._exit_popup)
        self.game._exit_popup.dismiss()
        settle()
        self.assertIsNone(self.game._exit_popup)
        calls = []
        with patch.object(self.game.career, 'save', side_effect=lambda: calls.append('save')):
            with patch('main.App.get_running_app') as get_app:
                get_app.return_value.stop.side_effect = lambda: calls.append('stop')
                self.game._confirm_exit()
        self.assertEqual(calls, ['save', 'stop'])

    def test_exit_save_failure_keeps_app_open(self):
        with patch.object(self.game.career, 'save', return_value=False):
            with patch('main.App.get_running_app') as get_app:
                self.game._confirm_exit()
                get_app.assert_not_called()

    def test_training_transition_removes_menu_and_returns(self):
        self.game.view = 'training'
        self.game.draw()
        settle()
        button = next(w for w in self.game._menu.walk() if isinstance(w, TouchButton) and 'TREINO' in w.text)
        button.dispatch('on_release')
        settle()
        self.assertEqual(self.game.view, 'shot')
        self.assertIsNone(self.game._menu)
        self.game._activate_ui('hub')
        self.game.draw()
        settle()
        self.assertIsNotNone(self.game._menu)

    def test_free_hides_paid_editor_and_world_actions(self):
        self.game.view = 'hub'
        self.game.draw()
        settle()
        buttons = [w.text for w in self.game._menu.walk() if isinstance(w, TouchButton)]
        self.assertNotIn('EDITOR LOCAL', buttons)
        self.assertNotIn('MUNDO DO FUTEBOL', buttons)
        with patch.object(self.game, '_open_local_editor') as editor:
            self.game._activate_ui('editor')
            editor.assert_not_called()


if __name__ == '__main__':
    unittest.main()
