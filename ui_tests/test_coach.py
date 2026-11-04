"""Coach gates and touch flow in the real native menus."""
import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.metrics import dp
from coach import fresh_state, conversation_text, style_for
from menu_ui import MenuTile, TouchButton
from test_menus import isolated_game,settle


class CoachUI(unittest.TestCase):
    def sign(self,g,requested=True):
        c=g.career;c.accept_starting_offer(c.offers[0])
        if requested:c.record_coach_performance(0,1,[],False,key_match=True)
        g._career_started=True;g.view='hub';g.draw();settle();return c

    def test_direct_actions_and_back_cannot_skip_meeting_then_training_unlocks(self):
        with isolated_game() as g:
            c=self.sign(g)
            g.start_training();self.assertEqual(g.view,'coach');self.assertFalse(c.training_used_this_week)
            g._activate_ui('hub');g.start_career_match();self.assertEqual(g.view,'coach')
            self.assertFalse(c.coach_meeting_held)
            g._activate_ui('coach_complete');g.draw();settle()
            self.assertEqual(g.view,'hub');self.assertTrue(c.coach_meeting_held)
            g.start_career_match();self.assertEqual(g.view,'hub') # training still required
            g.start_training();self.assertEqual(g.view,'shot');self.assertEqual(g.shot_context,'training')

    def test_both_hubs_show_meeting_and_disable_training_and_play(self):
        old=Window.size
        try:
            for size in ((320,240),(960,540)):
                Window.size=size
                with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                    c=self.sign(g);g.size=size;g.draw();settle()
                    buttons={w.text:w for w in g.walk() if isinstance(w,MenuTile)}
                    self.assertIn('COACH MEETING',buttons);self.assertTrue(buttons['TRAINING'].disabled);self.assertTrue(buttons['PLAY'].disabled)
                    g._activate_ui('coach');g._activate_ui('coach_complete');g.draw();settle()
                    buttons={w.text:w for w in g.walk() if isinstance(w,MenuTile)}
                    self.assertFalse(buttons['TRAINING'].disabled);self.assertTrue(buttons['PLAY'].disabled)
        finally:Window.size=old

    def test_translated_feedback_and_finish_action_reachable_on_small_screens(self):
        old=Window.size
        try:
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                c=self.sign(g)
                for size in ((320,240),(640,360),(360,640)):
                    Window.size=size;g.size=size
                    for lang in ('en','pt','es','de','it','ko','ja','zh','vi'):
                        g.i18n.choose(lang)
                        c.coach_state=fresh_state(c.club.uid);c.coach_state.update(games=3,drought=3,recent=[0,0,0])
                        g._activate_ui('coach');g.draw();settle()
                        message=g.i18n.tr(conversation_text(c.coach_conversation()))
                        self.assertTrue(any(w.text==message for w in g.walk() if isinstance(w,Label)),(size,lang))
                        g._menu.scroll.scroll_y=0;settle()
                        finish=next(w for w in g.walk() if isinstance(w,TouchButton) and w.text==g.i18n.tr('FINISH MEETING'))
                        self.assertGreaterEqual(finish.height,dp(48))
                        x,y=finish.to_window(finish.x,finish.y)
                        self.assertGreaterEqual(y,-1,(size,lang,y));self.assertLessEqual(y+finish.height,size[1]+1)
                        g._activate_ui('coach_complete');self.assertTrue(c.coach_meeting_held)
        finally:Window.size=old

    def test_new_week_and_play_date_jump_require_current_meeting(self):
        with isolated_game() as g:
            c=self.sign(g);c.attend_coach_meeting();c.last_training_week=c.week
            def next_week():
                c.week+=1
                c.record_coach_performance(0,1,[],False,key_match=True)
                return ('league',*c.next_fixture())
            with patch.object(c,'next_match',side_effect=next_week):g.start_career_match()
            self.assertEqual(g.view,'coach');self.assertFalse(c.coach_meeting_held)
            c.attend_coach_meeting();self.assertFalse(c.trained_this_week)


    def test_ordinary_week_has_no_meeting_button_and_training_is_available(self):
        with isolated_game() as g:
            c=self.sign(g,requested=False)
            buttons={w.text:w for w in g.walk() if isinstance(w,MenuTile)}
            self.assertNotIn('COACH MEETING',buttons);self.assertFalse(buttons['TRAINING'].disabled)
            g._activate_ui('coach');self.assertEqual(g.view,'hub')
            g.start_training();self.assertEqual(g.view,'shot')
