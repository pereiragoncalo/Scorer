"""Real font metrics and viewport bounds for scaled/CJK screen headings."""
import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
from kivy.metrics import Metrics,dp
from menu_ui import TouchButton
from test_menus import isolated_game,settle
class ResponsiveHeaders(unittest.TestCase):
    def setUp(self):
        self.addCleanup(setattr,Window,'size',Window.size)
        self.addCleanup(setattr,Metrics,'density',Metrics.density)
        self.addCleanup(setattr,Metrics,'fontscale',Metrics.fontscale)
    def test_coach_heading_style_and_form_fit_real_font_metrics(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting()
            for density,size in ((2,(1280,720)),(3,(1920,1080)),(4,(2960,1440))):
                Metrics.density=density;Window.size=size;g.size=size
                for scale in (1,1.3):
                    Metrics.fontscale=scale
                    for lang in ('pt','de','ja'):
                        g.i18n.choose(lang);g.view='coach';g.draw();settle();p=g._menu.body
                        self.assertTrue(p.layout_fits,(density,scale,lang))
                        for label in (p.title,p.style,p.recent):
                            if label.opacity<=0 or not label.text:continue
                            measure=CoreLabel(text=label.text,text_size=(int(label.width),None),font_name=label.font_name,font_size=label.font_size);measure.refresh()
                            self.assertLessEqual(measure.texture.size[1],label.height+2,(density,scale,lang,label.text))
    def test_german_back_actions_fit_viewport_with_larger_text(self):
        Metrics.density=3;Metrics.fontscale=1.3;Window.size=(1920,1080)
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g.size=Window.size;g.i18n.choose('de');g.world_league_key=c.league_key
            for view in ('standings','scorers','calendar','world_league','leaderboard'):
                g.view=view;g.draw();settle()
                buttons=[w for w in g.walk() if isinstance(w,TouchButton) and w.text==g.i18n.tr('BACK')]
                self.assertTrue(buttons)
                for button in buttons:
                    x,y=button.to_window(button.x,button.y)
                    self.assertGreaterEqual(y,0);self.assertLessEqual(y+button.height,Window.height+1)
                    self.assertGreaterEqual(button.height,dp(48))
