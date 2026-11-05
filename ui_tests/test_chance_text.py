"""Real translated notices fit without hidden lines, including the owner's phone."""
import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
from kivy.metrics import Metrics
from test_menus import isolated_game,settle
from opportunity_sequences import TEXT

class ChanceText(unittest.TestCase):
    def test_opportunity_text_is_complete_below_scoreboard_in_all_languages(self):
        old=Window.size;density=Metrics.density;scale=Metrics.fontscale
        try:
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                c=g.career;c.accept_starting_offer(c.offers[0]);c.last_training_week=c.week
                g.start_career_match()
                for width,height,ratio,fontscale in ((320,240,1,1),(1280,591,1.4,1),(800,480,1.5,1),(1920,1080,3,1.3)):
                    Window.size=(width,height);g.size=Window.size;Metrics.density=ratio;Metrics.fontscale=fontscale
                    for lang in ('en','pt','es','de','it','ko','ja','zh','vi'):
                        g.i18n.choose(lang)
                        for kind in ('through_ball','long_cross','corner','penalty'):
                            g.match_opportunities=(kind,);g.match_chance_index=0
                            g.match_easy_chance_index=0 if kind=='through_ball' else -1
                            g.match_penalty_chance_index=0 if kind=='penalty' else -1
                            g.match_moment='equaliser';g.awaiting_chance=True;g.match_finished=g.match_halftime=False;g.view='match';g.draw();settle()
                            p=g._match_notice;context=(width,height,lang,kind)
                            self.assertTrue(p.layout_fits,context)
                            self.assertLessEqual(p.top,g._scoreboard_bounds()[1]+1,context)
                            self.assertGreaterEqual(p.y,g.y,context)
                            self.assertGreaterEqual(p.scroll.height,p.body.height-2,context)
                            texts=[w.text for w in p.body.children]
                            self.assertTrue(any(g.i18n.tr(TEXT[kind][1]) in text for text in texts),context)
                            self.assertFalse(any('90' in text or g.i18n.tr('Expected playing time: {minutes} minutes',minutes=90) in text for text in texts),context)
                            for label in p.body.children:
                                m=CoreLabel(text=label.text,font_name=label.font_name,font_size=label.font_size,bold=label.bold,text_size=(label.width,None));m.refresh()
                                self.assertLessEqual(m.texture.size[1],label.height+1,context)
                                ly=label.to_window(*label.pos)[1];sy=p.scroll.to_window(*p.scroll.pos)[1]
                                self.assertGreaterEqual(ly,sy-1,context)
                                self.assertLessEqual(ly+label.height,sy+p.scroll.height+1,context)
        finally:Window.size=old;Metrics.density=density;Metrics.fontscale=scale
