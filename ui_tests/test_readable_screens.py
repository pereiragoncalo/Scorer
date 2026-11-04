import unittest,copy
from unittest.mock import patch
from kivy.core.window import Window
from kivy.metrics import Metrics,dp
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.tests.common import UnitTestTouch
from coach import fresh_state
from menu_ui import MenuTile,FlowLabel
from test_menus import isolated_game,settle

class ReadableScreens(unittest.TestCase):
    def sign(self,g):
        c=g.career;c.accept_starting_offer(c.offers[0]);g._career_started=True;return c
    def test_first_splash_touch_works_before_child_layout(self):
        with isolated_game() as g:
            g.draw();settle();g._menu.body.pos=(10000,10000)
            t=UnitTestTouch(*g.center);g.on_touch_down(t)
            self.assertEqual(g.view,'start');self.assertFalse(g._career_started)
    def test_notice_is_justified(self):
        with isolated_game() as g:
            g.view='data_notice';g.draw();settle()
            labels=[w for w in g.walk() if isinstance(w,FlowLabel)]
            self.assertTrue(any(w.halign=='justify' and len(w.text)>100 for w in labels))
    def test_name_button_and_three_header_buttons_align_to_stats_box(self):
        old=Window.size;self.addCleanup(setattr,Window,'size',old)
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=self.sign(g)
            for size in ((960,540),(1280,591)):
                Window.size=size;g.size=size;g.view='hub';g.draw();settle()
                p=g._menu.body;group=g._menu.hub_header_actions
                self.assertEqual(len(group.children),3)
                self.assertAlmostEqual(group.x,p.season.x,delta=1);self.assertAlmostEqual(group.right,p.season.right,delta=1)
                self.assertEqual(p.player_button.text,c.player_name)
                p.player_button.dispatch('on_release');self.assertEqual(g.view,'profile')
    def test_news_and_coach_are_one_screen_in_all_languages(self):
        old=Window.size;self.addCleanup(setattr,Window,'size',old)
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=self.sign(g);h,a=c.next_fixture();score=(1,3) if h.uid==c.club.uid else (3,1)
            c.finish_match(h,a,1,0,forced_score=score)
            for size in ((320,240),(640,360),(1280,591)):
                Window.size=size;g.size=size
                for lang in ('en','pt','es','de','it','ko','ja','zh','vi'):
                    g.i18n.choose(lang);g.view='newspaper';g.draw();settle();p=g._menu.body
                    self.assertEqual(len(p.pages),1,(size,lang));self.assertTrue(p.layout_fits,(size,lang,p.body_font_size))
                    self.assertFalse(any(isinstance(w,ScrollView) for w in p.walk()))
                    self.assertIsNone(p.following.parent);self.assertIsNone(p.previous.parent)
                    c.coach_state=fresh_state(c.club.uid);c.coach_state.update(games=3,drought=3,recent=[0,0,0])
                    g.view='coach';g.draw();settle();p=g._menu.body
                    self.assertTrue(p.layout_fits,(size,lang,p.feedback_font_size));self.assertIsNone(g._menu.scroll)
                    self.assertEqual(len(p.feedback.text.split('\n\n')),3)
                    self.assertFalse(any(isinstance(w,ScrollView) for w in p.walk()))
                    self.assertGreaterEqual(p.finish.y,0);self.assertLessEqual(p.finish.top,g.top)
    def test_every_recorded_minute_fits_on_one_sheet(self):
        old=Window.size;self.addCleanup(setattr,Window,'size',old)
        with isolated_game() as g:
            c=self.sign(g);h,a=c.next_fixture();c.finish_match(h,a,0,1,forced_score=(32,32))
            r=c.press_state['report'];r['events']=[dict(minute=i,half=1 if i<=45 else 2,side='home' if i%2 else 'away') for i in range(1,65)]
            for size in ((320,240),(640,360)):
                Window.size=size;g.size=size;g.view='newspaper';g.draw();settle();p=g._menu.body
                self.assertTrue(p.layout_fits,(size,p.body_font_size,p.story_text));self.assertEqual(len(p.pages),1)
                printed=''.join(part['text'] for page in p.pages for part in page)
                for i in range(1,65):self.assertIn(str(i)+"'",printed)
    def test_dashboard_rebuilds_after_root_resize_without_another_tap(self):
        old=Window.size;self.addCleanup(setattr,Window,'size',old)
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=self.sign(g);Window.size=(320,240);g.size=(320,240);g.view='hub';g.draw();settle()
            self.assertIsNone(getattr(g._menu,'hub_header_actions',None))
            Window.size=(1280,720);g.size=(1280,720);g.draw();settle()
            self.assertIsNotNone(g._menu.hub_header_actions)
            self.assertEqual(g._menu.body.player_button.text,c.player_name)

            g._activate_ui('profile');g.draw();settle();profile=g._menu.body
            profile.name.text='Alex Draft'
            Window.size=(640,360);g.size=(640,360);g.draw();settle()
            self.assertIs(g._menu.body,profile);self.assertEqual(profile.name.text,'Alex Draft')
