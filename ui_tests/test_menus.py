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
from menu_ui import TouchButton, MenuTile, CompactTable


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

    def test_halftime_stops_after_added_time_and_resumes_at_45(self):
        with isolated_game(saved=True) as game:
            game.career.load()
            game.career.last_training_week = game.career.week
            game.start_career_match()
            game.match_first_stoppage, game.match_stoppage = 2, 3
            game.match_chance_minutes, game.match_goal_events = [], []
            game.match_minute = 44.5
            game._update_career_match(0.5)
            self.assertEqual(game.match_clock_text, '45+01:00')
            game._update_career_match(5)
            self.assertEqual(game.match_minute, 47)
            self.assertTrue(game.match_halftime)
            self.assertEqual(game.match_clock_text, '45+02:00')
            game._update_career_match(100)
            self.assertEqual(game.match_minute, 47)
            game.draw()
            settle()
            self.assertEqual(game._match_notice.button.text, 'SECOND HALF')
            self.assertLessEqual(game._match_notice.top, game._scoreboard_bounds()[1])
            game._match_notice.proceed()
            self.assertEqual(game.match_half, 2)
            self.assertFalse(game.match_halftime)
            self.assertEqual(game.match_clock_text, '45:00')
            game._update_career_match(15)
            self.assertEqual(game.match_clock_text, '90+00:00')
            with patch.object(game, '_finish_career_match') as finish:
                game._update_career_match(1)
                self.assertEqual(game.match_clock_text, '90+03:00')
                finish.assert_called_once()

    def test_events_cannot_skip_a_chance_or_halftime(self):
        with isolated_game(saved=True) as game:
            game.career.load()
            game.career.last_training_week = game.career.week
            game.start_career_match()
            game.match_first_stoppage = 2
            game.match_chance_minutes = [47, 50]
            game.match_goal_events = [(46, 'home'), (48, 'away')]
            game.match_minute = 44
            with patch.object(game, '_play_ai_goal_sound'), patch.object(game, '_play_chance_sound'):
                game._update_career_match(100)
                self.assertEqual(game.match_minute, 47)
                self.assertTrue(game.awaiting_chance)
                self.assertEqual((game.match_home_score, game.match_away_score), (1, 0))
                self.assertGreater(game.scoreboard_flash_until, game.elapsed)
                game._begin_pending_chance()
                game.result_text = 'MISS!'
                game._advance_after_shot()
                game._update_career_match(100)
                self.assertTrue(game.match_halftime)
                self.assertEqual(game.match_goal_event_index, 1)
                game._resume_second_half()
                game._update_career_match(100)
                self.assertEqual(game.match_minute, 50)
                self.assertEqual((game.match_home_score, game.match_away_score), (1, 1))
                self.assertTrue(game.awaiting_chance)

    def test_player_goal_updates_and_flashes_immediately_only_once(self):
        with isolated_game(saved=True) as game:
            game.career.load()
            game.career.last_training_week = game.career.week
            game.start_career_match()
            game.shot_context, game.view = 'match', 'shot'
            game._prepare_next_shot()
            with patch.object(game, '_play_goal_crowd_sound'):
                game._register_goal()
                game._register_goal()
            self.assertEqual(game.match_player_goals, 1)
            self.assertEqual(game.match_home_score + game.match_away_score, 1)
            self.assertGreater(game.scoreboard_flash_until, game.elapsed)
            game._advance_after_shot()
            self.assertEqual(game.match_player_goals, 1)
            self.assertEqual(game.match_home_score + game.match_away_score, 1)
            game.elapsed += 1.1
            self.assertLess(game.scoreboard_flash_until, game.elapsed)

    def test_scoreboard_geometry_and_text_stay_fixed_through_chances(self):
        self.addCleanup(setattr, Metrics, 'density', Metrics.density)
        self.addCleanup(setattr, Window, 'size', Window.size)
        with isolated_game(saved=True) as game:
            game.career.load()
            game.career.last_training_week = game.career.week
            game.start_career_match()
            for size, density in (((640, 360), 1), ((1280, 589), 1.64), ((2400, 1080), 3)):
                Window.size, Metrics.density = size, density
                game.size = size
                game.pos = (11, 7)
                game.match_minute = 17.5
                bounds = game._scoreboard_bounds()
                captures = []
                with patch.object(game, '_draw_text', side_effect=lambda *a, **k: captures.append((a, k))), patch.object(game, '_draw_club_badge'):
                    with game.canvas:
                        game._draw_match_overlay()
                    simulated = list(captures)
                    captures.clear()
                    game.view, game.shot_context = 'shot', 'match'
                    game.state = game.STATE_RESULT
                    game.result_text = ''
                    with game.canvas:
                        game._draw_hud()
                    self.assertEqual(captures, simulated)
                captures.clear()
                game.state = game.STATE_AIMING
                game.shot_time_limit = game.shot_time_left = 4
                with patch.object(game, '_draw_text', side_effect=lambda *a, **k: captures.append((a, k))), patch.object(game, '_draw_club_badge'):
                    with game.canvas:
                        game._draw_hud()
                timer = next(args for args, _ in captures if str(args[0]).startswith('TIME TO SHOOT'))
                self.assertLessEqual(timer[2] + dp(15), bounds[1] - dp(12) + 0.0001)
                self.assertEqual(bounds, game._scoreboard_bounds())
                self.assertGreaterEqual(bounds[0], game.x)
                self.assertLessEqual(bounds[0] + bounds[2], game.right)
                self.assertEqual(simulated[0][0][1], simulated[2][0][1])
                self.assertGreater(simulated[0][0][2], simulated[2][0][2])
                self.assertTrue(any(args[0] == '17:30' for args, _ in simulated))
            game.pos = (0, 0)
            Metrics.density = 1

    def test_play_requires_completed_training_and_partial_session_resumes(self):
        Window.size = (960, 540)
        with isolated_game(saved=True) as game:
            game.career.load()
            game.view = 'hub'
            game.draw()
            settle()
            play = next(w for w in game.walk() if isinstance(w, MenuTile) and w.text == 'PLAY')
            self.assertTrue(play.disabled)
            self.assertAlmostEqual(play._face_color.r, 0.22, places=4)
            game.start_career_match()
            self.assertEqual(game.view, 'hub')
            game.start_training()
            game.result_text = 'GOAL!'
            game._advance_after_shot()
            game.career = CareerMode()
            game.view = 'hub'
            game.start_training()
            self.assertEqual((game.training_shots_left, game.training_goals), (2, 1))
            for result in ('MISS!', 'GOAL!'):
                game.result_text = result
                game._advance_after_shot()
            game._activate_ui('hub')
            game.draw()
            settle()
            play = next(w for w in game.walk() if isinstance(w, MenuTile) and w.text == 'PLAY')
            self.assertFalse(play.disabled)
            game.start_career_match()
            self.assertEqual(game.view, 'match')
            game.career.week += 1
            game.view = 'hub'
            game.draw()
            settle()
            play = next(w for w in game.walk() if isinstance(w, MenuTile) and w.text == 'PLAY')
            self.assertTrue(play.disabled)

    def test_chance_touch_survives_scene_frames_without_reparenting_or_skipping(self):
        Window.size = (960, 540)
        with isolated_game(saved=True) as game:
            game.career.load()
            game.career.last_training_week = game.career.week
            game.start_career_match()
            Clock.unschedule(game.update)
            game.match_chance_minutes = [10, 47, 65]
            game.match_first_stoppage = 2
            game.match_goal_events = []
            for index, minute in enumerate(game.match_chance_minutes):
                game.match_minute = minute
                game.match_half = 1 if index < 2 else 2
                game.match_halftime = False
                game.awaiting_chance = True
                game.view = 'match'
                game.draw()
                settle()
                notice = game._match_notice
                touch = UnitTestTouch(*notice.button.center)
                touch.touch_down()
                with patch.object(game, 'remove_widget', wraps=game.remove_widget) as remove:
                    for _ in range(5):
                        game.update(0.016)
                        Clock.tick()
                    remove.assert_not_called()
                touch.touch_up()
                settle()
                self.assertEqual((game.view, game.shot_context), ('shot', 'match'))
                self.assertEqual(game.match_chance_index, index + 1)
                self.assertFalse(game.outcome_registered)
                self.assertGreater(game.shot_time_left, 0)
                game.result_text = 'MISS!'
                game._advance_after_shot()
            self.assertEqual(game.match_player_misses, 3)

    def test_match_has_at_most_one_clear_chance_and_others_are_pressured(self):
        Window.size = (960, 540)
        with isolated_game(saved=True) as game:
            game.size = Window.size
            game.career.load()
            game.career.last_training_week = game.career.week
            seen_easy, seen_no_easy = False, False
            types = set()
            with patch.object(game.career, 'chance_count', return_value=3):
                for seed in range(60):
                    game.career.rng.seed(9700 + seed)
                    game.start_career_match()
                    easy_count = 0
                    for index in range(3):
                        game.awaiting_chance = True
                        game._begin_pending_chance()
                        types.add(game.shot_type)
                        if game.current_chance_difficulty == 'easy':
                            easy_count += 1
                            self.assertLessEqual(game.shot_origin_y, 11)
                            self.assertGreaterEqual(game.shot_time_limit, 5)
                        else:
                            self.assertFalse(game.one_on_one)
                            self.assertGreaterEqual(game.shot_origin_y, 16.5)
                            self.assertGreaterEqual(abs(game.shot_origin_x), 4.5)
                            sx, sy = game.project(game.shot_origin_x, game.shot_origin_y, 0)
                            self.assertTrue(game.x <= sx <= game.right)
                            self.assertTrue(game.y <= sy <= game.top)
                            self.assertGreaterEqual(len(game.field_players), 4)
                            self.assertLessEqual(game.shot_time_limit, 3.7)
                    self.assertLessEqual(easy_count, 1)
                    seen_easy |= easy_count == 1
                    seen_no_easy |= easy_count == 0
            self.assertTrue(seen_easy and seen_no_easy)
            self.assertEqual(types, {'kick', 'penalty', 'header', 'free_kick'})
            with patch.object(game.career, 'chance_count', return_value=0):
                game.start_career_match()
                self.assertEqual(game.match_easy_chance_index, -1)

    def test_hard_chance_keeper_reacts_faster_and_training_keeps_original_timing(self):
        with isolated_game(saved=True) as game:
            game.career.load()
            game.shot_context = 'match'
            game.current_chance_difficulty = 'hard'
            game._prepare_next_shot()
            game.power = 0.85
            game.shoot(2.0, 1.0)
            self.assertLessEqual(game.goalkeeper_reaction, 0.13)
            self.assertAlmostEqual(game.goalkeeper_dive_speed, 5.8)
            game.start_training()
            self.assertEqual(game.shot_context, 'training')
            self.assertEqual(game.training_shots_left, 3)

    def test_english_menu_labels_and_name_validation(self):
        with isolated_game(saved=True) as game:
            game.view = 'start'
            game._load_career()
            expected = {
                'start': {'NEW GAME', 'LOAD GAME', 'EXIT'},
                'hub': {'PLAY', 'TRAINING', 'STANDINGS', 'TOP SCORERS', 'FIXTURES', 'AGENT', 'PLAYER', 'EXIT'},
                'training': {'START TRAINING', 'BACK'},
                'standings': {'PREVIOUS', 'NEXT', 'MY POSITION', 'STATS', 'BACK'},
                'scorers': {'PREVIOUS', 'NEXT', 'MY POSITION', 'BACK'},
                'calendar': {'PREVIOUS', 'NEXT', 'STATS', 'BACK'},
                'agent': {'FIND OFFERS', 'BACK'},
            }
            for view, required in expected.items():
                game.view = view
                game.draw()
                settle()
                labels = {w.text for w in game.walk() if isinstance(w, Label)}
                self.assertTrue(required <= labels, (view, required - labels))
            game._profile_return = 'hub'
            game.view = 'profile'
            game._activate_ui('save_profile', '')
            settle()
            self.assertEqual(game.career.message, 'Enter a name with at least 2 characters.')
            self.assertTrue(any(isinstance(w, Label) and w.text == game.career.message
                                for w in game.walk()))

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
            self.assertEqual(set(labels), {'NEW GAME', 'LOAD GAME', 'EXIT'})
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
            self.assertEqual(game.view, 'profile')
            self.assertEqual(game.career.save_path.read_bytes(), before)
            self.assertEqual(game.career.save_path.with_name('striker_career.previous.json').read_bytes(), before)
            self.assertFalse(game._career_started)
            game._activate_ui('save_profile', 'Test Player')
            self.assertEqual(game.view, 'offers')
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
            load = next(w for w in game.walk() if isinstance(w, TouchButton) and w.text == 'LOAD GAME')
            self.assertTrue(load.disabled)
            game._activate_ui('new_game')
            self.assertEqual(game.view, 'profile')
            self.assertIsNone(game._new_game_popup)

    def test_player_setup_requires_name_and_existing_player_can_be_renamed(self):
        with isolated_game() as game:
            game._activate_ui('splash_continue')
            game._activate_ui('new_game')
            game._activate_ui('save_profile', '')
            self.assertEqual(game.view, 'profile')
            game.draw()
            settle()
            form = game._menu.body
            self.assertEqual(form.name.text, '')
            form.name.text = 'Luca Vale'
            form.submit()
            self.assertEqual(game.view, 'offers')
            game._activate_ui('accept_offer', game.career.offers[0])
            game._activate_ui('profile')
            game.draw()
            settle()
            form = game._menu.body
            self.assertEqual(form.name.text, 'Luca Vale')
            form.name.text = 'Alex Costa'
            form.submit()
            self.assertEqual(game.view, 'hub')
            self.assertEqual(CareerMode().player_name, 'Alex Costa')

    def test_tables_page_through_every_row_without_scrolling(self):
        Window.size = (640, 360)
        self.game.size = Window.size
        for view in ('standings', 'scorers', 'calendar'):
            with self.subTest(view=view):
                self.game.view = view
                self.game.draw()
                settle()
                table = self.game._menu.body
                self.assertIsInstance(table, CompactTable)
                self.assertFalse(any(isinstance(w, ScrollView) for w in table.walk()))
                self.assertGreaterEqual(table.page_size, 6)
                found = []
                for _ in range(table.pages):
                    found.extend(table.visible_rows)
                    self.assertGreaterEqual(table.lines.y, table.controls.top)
                    table.next.dispatch('on_release')
                    settle()
                self.assertEqual(found, table.rows)
                if table.focus:
                    table.jump_to_focus()
                    self.assertTrue(any(str(row[1]) == table.focus for row in table.visible_rows))
                table.toggle_detail()
                settle()
                for row in table.lines.children:
                    self.assertGreaterEqual(row.x, table.x)
                    self.assertLessEqual(row.right, table.right)

    def test_buttons_have_visible_press_depth(self):
        self.game.career.last_training_week = self.game.career.week
        self.game.view = 'hub'
        self.game.draw()
        settle()
        button = next(w for w in self.game.walk() if isinstance(w, MenuTile) and w.text == 'PLAY')
        raised = button._face.pos[1]
        self.assertAlmostEqual(button._face.pos[1] + button._face.size[1] / 2, button.center_y)
        normal = tuple(button._face_color.rgba)
        button.state = 'down'
        self.assertLess(button._face.pos[1], raised)
        self.assertNotEqual(tuple(button._face_color.rgba), normal)
        button.state = 'normal'
        self.assertEqual(button._face.pos[1], raised)

    def test_training_sits_left_of_play_and_brand_uses_icon_as_s(self):
        previous = Metrics.density
        try:
            for density, size in ((1, (640, 360)), (1, (960, 540)), (1.64, (1280, 589)), (3, (2400, 1080))):
                with self.subTest(density=density, size=size):
                    Metrics.density = density
                    Window.size = size
                    self.game.size = size
                    self.game.view = 'hub'
                    self.game.draw()
                    self.game._menu._signature = None
                    self.game.draw()
                    settle()
                    buttons = [w for w in self.game.walk() if isinstance(w, MenuTile)]
                    play = next(w for w in buttons if w.text == 'PLAY')
                    training = next(w for w in buttons if w.text == 'TRAINING')
                    self.assertLess(training.right, play.x)
                    self.assertAlmostEqual(training.y, play.y, delta=1)
                    self.assertAlmostEqual(training.width, play.width, delta=1)
                    self.assertTrue(any(getattr(w, 'source', '') == 'assets/menu_logo.png' for w in self.game.walk()))
                    self.assertFalse(any(isinstance(w, Label) and w.text == 'by clemir' for w in self.game.walk()))
        finally:
            Metrics.density = previous

    def test_weekly_training_blocks_repeat_and_reload_then_unlocks_next_week(self):
        Window.size = (800, 360)
        with isolated_game(saved=True) as game:
            game._activate_ui('splash_continue')
            game._activate_ui('load_game')
            game._activate_ui('training')
            game._activate_ui('training_start')
            self.assertEqual(game.view, 'shot')
            for _ in range(3):
                game.result_text = 'GOAL!'
                game._advance_after_shot()
            self.assertEqual(game.view, 'training')
            game.draw()
            settle()
            menu = game._menu
            self.assertLessEqual(menu.body.height, menu.scroll.height + 1)
            stats = (game.career.stamina, game.career.morale)
            game._activate_ui('training_start')
            self.assertEqual(game.view, 'training')
            self.assertEqual((game.career.stamina, game.career.morale), stats)
            game.career = CareerMode()
            game.training_completed = False
            game.draw()
            settle()
            button = next(w for w in game.walk() if isinstance(w, TouchButton) and w.text == 'WEEKLY TRAINING USED')
            self.assertTrue(button.disabled)
            game.career.week += 1
            game.draw()
            settle()
            button = next(w for w in game.walk() if isinstance(w, TouchButton) and w.text == 'START TRAINING')
            self.assertFalse(button.disabled)

    def test_active_training_cannot_restart_its_shot_counter(self):
        with isolated_game(saved=True) as game:
            game._activate_ui('splash_continue')
            game._activate_ui('load_game')
            game.start_training()
            game.result_text = 'GOAL!'
            game._advance_after_shot()
            game.start_training()
            self.assertEqual((game.training_shots_left, game.training_goals), (2, 1))
            self.assertEqual(game.view, 'shot')

    def test_failed_training_reservation_does_not_start_a_session(self):
        with isolated_game(saved=True) as game:
            game._activate_ui('splash_continue')
            game._activate_ui('load_game')
            with patch('career.os.replace', side_effect=OSError('disk full')):
                game.start_training()
            self.assertEqual(game.view, 'training')
            self.assertFalse(game.career.training_used_this_week)
            self.assertEqual(game.training_shots_left, 0)

    def test_all_menu_layouts_at_phone_sizes(self):
        for size in ((640, 360), (800, 360), (960, 540), (1280, 720), (360, 800), (320, 240)):
            Window.size = size
            self.game.size = size
            for view in ('start', 'profile', 'offers', 'hub', 'training', 'standings', 'scorers', 'calendar', 'agent'):
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
        play = next(w for w in menu.walk() if isinstance(w, TouchButton) and w.text == 'PLAY')
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
                    self.assertEqual(len(buttons), 8)
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
        button = next(w for w in menu.walk() if isinstance(w, TouchButton) and w.text == 'STANDINGS')
        # Native widget callback, followed by independent real touch on header Back.
        button.dispatch('on_release')
        settle()
        self.assertEqual(self.game.view, 'standings')
        back = next(w for w in self.game._menu.walk() if isinstance(w, TouchButton) and w.text == 'BACK')
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
        self.game.career.last_training_week = -1
        self.game.career.training_session_week = -1
        self.game.view = 'training'
        self.game.draw()
        settle()
        button = next(w for w in self.game._menu.walk() if isinstance(w, TouchButton) and 'TRAINING' in w.text)
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
            self.assertEqual('EXIT' in labels, view in ('hub', 'offers'))

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
        self.assertNotIn('LOCAL EDITOR', buttons)
        self.assertNotIn('WORLD FOOTBALL', buttons)
        with patch.object(self.game, '_open_local_editor') as editor:
            self.game._activate_ui('editor')
            editor.assert_not_called()


if __name__ == '__main__':
    unittest.main()
