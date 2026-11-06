import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.uix.label import Label
from menu_ui import MenuTile,TouchButton
from test_menus import isolated_game,settle
from honours import participate,award

class PostMatchFlow(unittest.TestCase):
    def sign(self,g):
        c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True;return c
    def result(self,g,key=False):
        c=self.sign(g);h,a=c.next_fixture()
        g.match_home,g.match_away=h,a;g.match_home_score=1;g.match_away_score=0
        g.match_competition='league';g.match_player_goals=0;g.match_player_misses=1;g.match_stakes={'kind':'final'} if key else {}
        g.match_is_international=False;g.view='match';g.match_finished=False;g._finish_career_match();return c
    def test_final_then_paper_then_optional_coach_then_hub_survives_reload(self):
        for requested in (False,True):
            with isolated_game() as g:
                c=self.result(g,requested);self.assertEqual(g.view,'match')
                self.assertEqual(c.post_match_stage,'newspaper');self.assertTrue(c.load())
                g._activate_ui('match_continue');g.draw();settle();self.assertEqual(g.view,'newspaper')
                g._on_key_down(None,27,None,'',None);g.draw();settle()
                self.assertEqual(g.view,'coach')
                if True:
                    self.assertTrue(c.load());self.assertEqual(c.post_match_stage,'coach')
                    g._on_key_down(None,27,None,'',None);self.assertEqual(g.view,'coach')
                    g._activate_ui('coach_focus',c.coach_focus_options()[0]);g._activate_ui('coach_complete');g.draw();settle();self.assertEqual(g.view,'hub')
                self.assertEqual(c.post_match_stage,'');self.assertTrue(c.load());self.assertEqual(c.post_match_stage,'')
    def test_failed_paper_save_retains_stage_and_does_not_skip_coach(self):
        with isolated_game() as g:
            c=self.result(g,True);g._activate_ui('match_continue')
            with patch.object(c,'save',return_value=False):g._activate_ui('post_match_continue')
            self.assertEqual(g.view,'newspaper');self.assertEqual(c.post_match_stage,'newspaper')
    def test_hubs_have_no_news_or_coach_and_agent_follows_window(self):
        old=Window.size;self.addCleanup(setattr,Window,'size',old)
        for size in ((320,240),(960,540)):
            Window.size=size
            with isolated_game() as g:
                c=self.sign(g);g.size=size
                for week,disabled in ((12,True),(0,False)):
                    c.week=week;c.attend_coach_meeting();g.view='hub';g.draw();settle()
                    buttons={w.text:w for w in g.walk() if isinstance(w,MenuTile)}
                    self.assertNotIn('NEWSPAPER',buttons);self.assertNotIn('COACH MEETING',buttons)
                    self.assertEqual(buttons['AGENT'].disabled,disabled)
                    if disabled:g._activate_ui('agent');self.assertEqual(g.view,'hub')
    def test_profile_objectives_preserve_saved_trophies_and_controls_fit_small_screens(self):
        old=Window.size;self.addCleanup(setattr,Window,'size',old)
        with isolated_game() as g:
            c=self.sign(g);participate(c,'cup','Test cup',c.club.uid,c.club.name,c.club.country);award(c,c.honours['campaigns'][0]);c.save();self.assertTrue(c.load())
            for size in ((320,240),(960,540)):
                Window.size=size;g.size=size;g.view='hub';g._activate_ui('profile');g.draw();settle()
                p=g._menu.body;labels=[w.text for w in p.walk() if isinstance(w,Label)]
                self.assertIn('OBJECTIVES',labels);self.assertNotIn('TROPHIES',labels)
                self.assertTrue(any(t['title']=='Test cup' for t in c.honours['trophies']))
                self.assertGreaterEqual(p.actions.y,p.y);self.assertLessEqual(p.panel.top,p.top+1)
