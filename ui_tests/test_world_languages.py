"""Real Kivy controls, font rendering and state isolation for World languages."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.metrics import Metrics, dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from test_menus import isolated_game, settle
from localization import LANGUAGES, Localizer, CJK_FONTS
from menu_ui import MenuTile, CompactTable, LanguageScreen
from main import StrikerApp


class WorldLanguageTests(unittest.TestCase):
    def test_free_stays_english_and_cannot_open_language_settings(self):
        with patch('main.phone_locale_tag',side_effect=AssertionError('Free must ignore phone language')):
            with isolated_game() as game:
                game.view='start';game.draw();settle()
                texts={w.text for w in game.walk() if isinstance(w,Button)}
                self.assertIn('NEW GAME',texts);self.assertNotIn('LANGUAGE',texts)
                game._activate_ui('language');self.assertEqual(game.view,'start')
                game._activate_ui('choose_language','ja')
                self.assertEqual(game.i18n.language,'en')
                self.assertFalse(game.career.world_unlocked)

    def test_world_entry_uses_each_phone_language_without_changing_start_country(self):
        for code in LANGUAGES:
            with self.subTest(language=code),patch('edition.WORLD_BUILD',True),patch('main.phone_locale_tag',return_value=code),patch('main.phone_country',return_value='Portugal'):
                with isolated_game() as game:
                    self.assertEqual(game.i18n.language,code)
                    self.assertEqual(game.career.suggested_country,'Portugal')
                    game.view='start';game.draw();settle()
                    texts={w.text for w in game.walk() if isinstance(w,Button)}
                    self.assertIn(game.i18n.tr('NEW GAME'),texts)
                    self.assertIn(game.i18n.tr('LANGUAGE'),texts)
                    self.assertIn(game.i18n.tr('LOAD GAME'),texts)

    def test_language_choice_uses_buttons_persists_and_keeps_names_and_save_bytes(self):
        with patch('edition.WORLD_BUILD',True),patch('main.phone_locale_tag',return_value='en'):
            with isolated_game() as game:
                c=game.career;c.set_player_name('Nguyễn 日本語');c.accept_starting_offer(c.offers[0])
                c.apply_names({'version':1,'clubs':{c.club.uid:'HELP'},'leagues':{c.league_key:'PLAY'}})
                c.save();before=c.save_path.read_bytes();identity=(c.player_name,c.club.uid,c.league_key)
                game._career_started=True;game.view='hub';game._activate_ui('help');game._activate_ui('language');game.draw();settle()
                button=next(w for w in game.walk() if isinstance(w,MenuTile) and w.text=='Deutsch')
                button.dispatch('on_release');game.draw();settle()
                self.assertEqual(game.i18n.language,'de')
                self.assertEqual(Localizer(True,'ja',c.save_path.parent).language,'de')
                self.assertEqual(c.save_path.read_bytes(),before)
                self.assertEqual((c.player_name,c.club.uid,c.league_key),identity)
                game._activate_ui('language_back');self.assertEqual(game.view,'help')
                game._activate_ui('help_back');game.draw();settle()
                labels={w.text for w in game.walk() if isinstance(w,Label)}
                self.assertIn('HELP',labels);self.assertIn('PLAY',labels)
                self.assertIn(c.player_name,labels)

    def test_table_headers_stay_translated_after_paging_and_asynchronous_layout(self):
        with patch('edition.WORLD_BUILD',True),patch('main.phone_locale_tag',return_value='ja'):
            with isolated_game() as game:
                c=game.career;c.accept_starting_offer(c.offers[0]);c.apply_names({'version':1,'clubs':{c.club.uid:'HELP'}})
                game.view='standings';game.draw();settle()
                table=next(w for w in game.walk() if isinstance(w,CompactTable))
                table.move(1);table.width-=5;settle();table.jump_to_focus();settle()
                self.assertIn(game.i18n.tr('CLUB'),{w.text for w in table.head.children})
                self.assertIn('HELP',{w.text for w in table.lines.walk() if isinstance(w,Label)})

    def test_all_languages_are_accessible_without_scroll_on_small_and_large_screens(self):
        old_size=Window.size;old_density=Metrics.density
        try:
            Metrics.density=1.6
            for size in [(1280,640),(640,360),(360,640)]:
                with self.subTest(size=size),patch('edition.WORLD_BUILD',True),patch('main.phone_locale_tag',return_value='en'):
                    with isolated_game() as game:
                        Window.size=size;game.size=size;game.view='start';game._activate_ui('language');game.draw();settle()
                        screen=game._menu.body;self.assertIsInstance(screen,LanguageScreen)
                        self.assertFalse(any(isinstance(w,ScrollView) for w in screen.walk()))
                        found=set()
                        for _ in range(3):
                            found.update(w.text for w in screen.grid.children)
                            for w in screen.walk():
                                if isinstance(w,MenuTile):
                                    self.assertGreaterEqual(w.width,dp(48)-1)
                                    self.assertGreaterEqual(w.height,dp(48)-1)
                                    self.assertGreaterEqual(w.y,game.y-1)
                                    self.assertLessEqual(w.top,game.top+1)
                            screen.move(1);settle()
                        self.assertEqual(found,set(LANGUAGES.values()))
        finally:Window.size=old_size;Metrics.density=old_density

    def test_editor_values_and_json_schema_are_not_translated(self):
        with patch('edition.WORLD_BUILD',True),patch('main.phone_locale_tag',return_value='ko'):
            with isolated_game() as game:
                c=game.career;c.accept_starting_offer(c.offers[0]);c.apply_names({'version':1,'clubs':{c.club.uid:'PLAY 日本語'},'leagues':{c.league_key:'HELP'}})
                game.editor_key=c.league_key;game.editor_club_index=c.current_league.clubs.index(c.club)
                game.view='editor';game.draw();settle()
                fields={w.text for w in game.walk() if isinstance(w,TextInput)}
                self.assertIn('PLAY 日本語',fields);self.assertIn('HELP',fields)
                game._activate_ui('names_format');settle()
                popup=game._names_format_popup
                try:
                    self.assertEqual(popup.title,game.i18n.tr('NAME FILE FORMAT — JSON'))
                    sample=next(w for w in popup.walk() if isinstance(w,TextInput) and w.readonly)
                    data=json.loads(sample.text)
                    self.assertEqual(set(data),{'version','clubs','leagues','players'})
                    self.assertEqual(data['clubs'][c.club.uid],'PLAY 日本語')
                finally:popup.dismiss()

    def test_system_language_change_preserves_unsaved_text_input(self):
        with patch('edition.WORLD_BUILD',True),patch('main.phone_locale_tag',return_value='en'):
            with isolated_game() as game:
                game.view='profile';game.draw();settle()
                game._menu.body.name.text='Nguyễn 日本語';game._menu.body.name.cursor=(3,0)
                app=StrikerApp();app.root=game
                try:
                    with patch('main.phone_locale_tag',return_value='ja-JP'):app.on_resume()
                    settle()
                    self.assertEqual(game._menu.body.name.text,'Nguyễn 日本語')
                    self.assertEqual(game._menu.body.name.hint_text,game.i18n.tr('Player name'))
                    self.assertEqual(game.i18n.language,'ja')
                finally:app.root=None

    def test_match_clock_and_goal_text_render_in_every_world_language(self):
        for code in LANGUAGES:
            with self.subTest(language=code),patch('edition.WORLD_BUILD',True),patch('main.phone_locale_tag',return_value=code):
                with isolated_game() as game:
                    c=game.career;c.accept_starting_offer(c.offers[0]);c.last_training_week=c.week
                    c.apply_names({'version':1,'clubs':{c.club.uid:'HELP'}})
                    game.start_career_match();game.draw();settle()
                    texts={key[0] for key in game._text_texture_cache}
                    self.assertIn(game.i18n.tr('First half'),texts)
                    self.assertIn('HELP',texts)
                    game.match_halftime=True;game.draw()
                    self.assertIn(game.i18n.tr('Half time'),{key[0] for key in game._text_texture_cache})
                    game.match_halftime=False;game.match_finished=True;game.draw()
                    self.assertIn(game.i18n.tr('Full time'),{key[0] for key in game._text_texture_cache})
                    game.match_finished=False
                    game.awaiting_chance=True;game._begin_pending_chance();game.result_text='GOAL!';game.draw();settle()
                    self.assertIn(game.i18n.tr('GOAL!'),{key[0] for key in game._text_texture_cache})
                    self.assertEqual(game.result_text,'GOAL!')
