import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from test_menus import isolated_game,settle

class CoachUI(unittest.TestCase):
    def sign(self,g):
        c=g.career;c.accept_starting_offer(c.offers[0]);g._career_started=True;g.view='hub';g.draw();settle();return c
    def choose(self,g):
        c=g.career;g._activate_ui('coach_focus',c.coach_focus_options()[1]);g.draw();settle();g._activate_ui('coach_complete');g.draw();settle()
    def test_first_week_requires_choice_before_completion_and_training(self):
        with isolated_game() as g:
            c=self.sign(g);self.assertEqual(g.view,'coach');g._activate_ui('coach_complete');self.assertFalse(c.coach_meeting_held)
            g._on_key_down(Window,27,0,'',[]);self.assertEqual(g.view,'coach');g.start_training();self.assertEqual(g.view,'coach')
            self.assertEqual(len(g._menu.body.choices),2);self.assertTrue(g._menu.body.finish.disabled)
            focus=c.coach_focus_options()[1];self.choose(g);self.assertTrue(c.coach_meeting_held);self.assertEqual(c.training_focus,focus)
            g.start_training();self.assertEqual(g.view,'shot')
    def test_weekly_lock_and_training_screen_has_no_focus_selector(self):
        with isolated_game() as g:
            c=self.sign(g);self.choose(g);g._activate_ui('training');g.draw();settle()
            buttons={w.text for w in g.walk() if isinstance(w,Button)};self.assertNotIn('TRAINING FOCUS',buttons)
            focus=c.training_focus;g._activate_ui('training_focus_open');g._activate_ui('training_focus','heading');self.assertEqual(c.training_focus,focus)
            c.week+=1;g._activate_ui('training');g.draw();self.assertEqual(g.view,'coach')
    def test_collective_individual_feedback_and_weekly_choices_fit_all_languages(self):
        old=Window.size
        try:
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                c=self.sign(g)
                for size in ((320,240),(640,360),(1280,591)):
                    Window.size=size;g.size=size
                    for language in ('en','pt','es','de','it','ko','ja','zh','vi'):
                        g.i18n.choose(language);g.view='coach';g.draw();settle();screen=g._menu.body
                        self.assertTrue(screen.layout_fits,(size,language));self.assertIsNone(screen.scroll)
                        self.assertIn(c.player_name,screen.full_text);self.assertEqual(screen.closing.halign,'justify')
                        self.assertIn('team_talk.png',screen.portrait.source)
                        for button in (*screen.choices,screen.finish,screen.help):
                            self.assertGreaterEqual(button.height,dp(48)-1);self.assertGreaterEqual(button.y,g.y-1);self.assertLessEqual(button.top,g.top+1)
        finally:Window.size=old
    def test_no_gameplay_help_and_scoreboard_keeps_full_width(self):
        with isolated_game(saved=True) as g:
            c=g.career;c.load();c.attend_coach_meeting();g.start_training();g.draw();settle()
            self.assertEqual(g.view,'shot');self.assertIsNone(g._game_help)
            self.assertFalse(any(isinstance(w,Button) and w.text=='HELP' for w in g.walk()))
    def test_help_explains_weekly_focus_only_at_team_talk(self):
        from contextual_help import topics
        with isolated_game() as g:
            self.sign(g);g.view='coach';self.assertTrue(any(title=='TRAINING FOCUS' for title,_ in topics(g)))
            g.view='training';self.assertFalse(any(title=='TRAINING FOCUS' for title,_ in topics(g)))
