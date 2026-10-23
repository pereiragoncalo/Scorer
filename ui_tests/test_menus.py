"""Real Kivy layout and input tests; run with the development Kivy interpreter."""
import os
import tempfile
import unittest
from unittest.mock import patch
from contextlib import contextmanager
from types import SimpleNamespace

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, Metrics
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.tests.common import UnitTestTouch

from main import StrikerGame, StrikerApp
from career import CareerMode
from menu_ui import TouchButton, MenuTile


def settle():
    for _ in range(18):
        Clock.tick()
        Clock.tick_draw()


@contextmanager
def isolated_game(saved=False, corrupt=False):
    with tempfile.TemporaryDirectory() as root, patch.dict(os.environ, STRIKER_SAVE_DIR=root):
        c = CareerMode()
        if saved:
            c.accept_starting_offer(c.offers[0])
            c.goals = 17
            c.save()
        if corrupt:
            c.save_path.write_text('{broken')
        game = StrikerGame()
        Window.add_widget(game)
        try:
            yield game
        finally:
            for popup in (game._exit_popup, game._new_game_popup):
                if popup is not None:
                    popup.dismiss()
            Clock.unschedule(game.update)
            Window.remove_widget(game)
            Window.unbind(on_key_down=game._on_key_down)


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

    def test_splash_survives_rotation_and_time_until_real_touch(self):
        with isolated_game(saved=True) as game:
            before = game.career.save_path.read_bytes()
            for size in ((360, 800), (1280, 589), (960, 540)):
                Window.size = size
                game.size = size
                for _ in range(12):
                    game.update(1)
                settle()
                self.assertEqual(game.view, 'splash')
                self.assertEqual(game.career.club_name, '')
            StrikerApp.on_pause(SimpleNamespace(root=game))
            StrikerApp.on_stop(SimpleNamespace(root=game))
            self.assertEqual(game.career.save_path.read_bytes(), before)
            touch = UnitTestTouch(*game.center)
            touch.touch_down()
            touch.touch_up()
            settle()
            self.assertEqual(game.view, 'start')
            labels = [w.text for w in game.walk() if isinstance(w, TouchButton)]
            self.assertEqual(set(labels), {'NOVO JOGO', 'CARREGAR JOGO', 'SAIR'})
            self.assertEqual(game.career.save_path.read_bytes(), before)
            game._activate_ui('load_game')
            settle()
            self.assertEqual(game.view, 'hub')
            self.assertEqual(game.career.goals, 17)

    def test_new_game_cancel_and_confirmation_preserve_old_save(self):
        with isolated_game(saved=True) as game:
            before = game.career.save_path.read_bytes()
            game._activate_ui('splash_continue')
            game.draw()
            game._activate_ui('new_game')
            settle()
            self.assertIsNotNone(game._new_game_popup)
            game._new_game_popup.dismiss()
            self.assertEqual(game.view, 'start')
            self.assertEqual(game.career.save_path.read_bytes(), before)
            game._activate_ui('new_game')
            game._start_new_career()
            settle()
            self.assertEqual(game.view, 'offers')
            self.assertEqual(game.career.save_path.read_bytes(), before)
            self.assertEqual(game.career.save_path.with_name('striker_career.previous.json').read_bytes(), before)
            self.assertFalse(game._career_started)
            game._activate_ui('accept_offer', game.career.offers[0])
            self.assertTrue(game._career_started)
            self.assertEqual(game.career.goals, 0)
            self.assertEqual(game.career.save_path.with_name('striker_career.previous.json').read_bytes(), before)

    def test_new_game_backup_failure_and_corrupt_load_stay_on_entry(self):
        with isolated_game(corrupt=True) as game:
            game._activate_ui('splash_continue')
            game._load_career()
            self.assertEqual(game.view, 'start')
            self.assertEqual(game.career.save_path.read_text(), '{broken')
            with patch.object(game.career, 'backup_before_new_game', return_value=False):
                game._start_new_career()
            self.assertEqual(game.view, 'start')
            self.assertEqual(game.career.save_path.read_text(), '{broken')

    def test_load_is_disabled_when_no_save_exists(self):
        with isolated_game() as game:
            game._activate_ui('splash_continue')
            game.draw()
            settle()
            load = next(w for w in game.walk() if isinstance(w, TouchButton) and w.text == 'CARREGAR JOGO')
            self.assertTrue(load.disabled)
            game._activate_ui('new_game')
            self.assertEqual(game.view, 'offers')
            self.assertIsNone(game._new_game_popup)

    def test_all_menu_layouts_at_phone_sizes(self):
        for size in ((640, 360), (800, 360), (960, 540), (1280, 720), (360, 800), (320, 240)):
            Window.size = size
            self.game.size = size
            for view in ('start', 'offers', 'hub', 'training', 'standings', 'scorers', 'calendar', 'agent'):
                with self.subTest(size=size, view=view):
                    self.game.view = view
                    self.game.draw()
                    settle()
                    menu = self.game._menu
                    self.assertIsNotNone(menu)
                    self.assertGreater(menu.body.height, 0)
                    for widget in menu.walk():
                        if isinstance(widget, TouchButton):
                            self.assertGreaterEqual(widget.height, dp(52) - 1)
                            padding = (16, 12) if isinstance(widget, MenuTile) else (24, 20)
                            self.assertLessEqual(widget.texture_size[0], widget.width - dp(padding[0]) + 2)
                            self.assertLessEqual(widget.texture_size[1], widget.height - dp(padding[1]) + 2)
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
        self.assertGreater(y, menu.body.y)
        self.assertLess(y, menu.body.top)

    def test_main_menu_has_no_scroll_and_all_actions_are_visible(self):
        previous = Metrics.density
        try:
            for density, size in ((1, (640, 360)), (1, (800, 360)),
                                  (1.64, (1280, 589)), (3, (2400, 1080)),
                                  (1, (360, 800)), (1, (320, 240))):
                with self.subTest(density=density, size=size):
                    Metrics.density = density
                    Window.size = size
                    self.game.size = size
                    self.game.view = 'hub'
                    self.game.draw()
                    self.game._menu._signature = None
                    self.game.draw()
                    settle()
                    menu = self.game._menu
                    self.assertFalse(any(isinstance(w, ScrollView) for w in menu.walk()))
                    buttons = [w for w in menu.walk() if isinstance(w, TouchButton)]
                    self.assertEqual(len(buttons), 7)
                    for button in buttons:
                        self.assertGreaterEqual(button.width, dp(48) - 1)
                        self.assertGreaterEqual(button.height, dp(48) - 1)
                        self.assertGreaterEqual(button.x, menu.x - 1)
                        self.assertGreaterEqual(button.y, menu.y - 1)
                        self.assertLessEqual(button.right, menu.right + 1)
                        self.assertLessEqual(button.top, menu.top + 1)
                    for i, a in enumerate(buttons):
                        for b in buttons[i+1:]:
                            overlap = min(a.right, b.right) - max(a.x, b.x)
                            if overlap > 1:
                                self.assertLessEqual(min(a.top, b.top) - max(a.y, b.y), 1)
        finally:
            Metrics.density = previous

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
            self.assertGreater(menu.body.height, 0)
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

    def test_exit_is_only_on_main_menu(self):
        for view in ('hub', 'offers', 'training', 'standings', 'agent', 'match', 'shot'):
            self.game.view = view
            self.game.draw()
            settle()
            labels = [w.text for w in self.game.walk() if isinstance(w, TouchButton)]
            self.assertEqual('SAIR' in labels, view in ('hub', 'offers'))

    def test_finished_panel_wraps_and_continue_returns_to_career(self):
        self.game.match_finished = True
        self.game.match_summary = 'FINAL Northgate City Athletic Football Club 0-0 Highmoor Athletic United'
        self.game.awaiting_chance = False
        for size in ((640, 360), (1280, 589), (960, 540)):
            self.game.view = 'match'
            Window.size = size
            self.game.size = size
            self.game.draw()
            settle()
            panel = self.game._match_notice
            self.assertIsNotNone(panel)
            self.assertGreaterEqual(panel.button.height, dp(52))
            self.assertGreaterEqual(panel.scroll.y, panel.button.top)
            self.assertLessEqual(panel.top, self.game.top)
            self.assertLessEqual(panel.height, panel.body.minimum_height + panel.button.height + dp(40))
            self.assertLess(panel.button.width, panel.width * 0.6)
            self.assertLessEqual(panel.height, dp(200))
            for widget in panel.body.children:
                self.assertLessEqual(widget.texture_size[0], widget.width + 2)
                self.assertLessEqual(widget.texture_size[1], widget.height + 2)
            # Scene redraws must preserve the native widget canvas.
            self.game.draw()
            settle()
            self.assertIs(panel.parent, self.game)
        panel.button.dispatch('on_release')
        settle()
        self.assertEqual(self.game.view, 'hub')
        self.game.match_finished = False

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
