"""Goal aperture, anatomy and training isolation in the actual native game."""
import math,unittest
from unittest.mock import patch
from test_menus import isolated_game,settle
from coach import conversation_text
from menu_ui import TouchButton
from kivy.uix.label import Label
from kivy.core.window import Window

class FairFinishing(unittest.TestCase):
    def test_aim_stays_in_open_aperture_and_visits_both_sides_and_heights(self):
        with isolated_game(saved=True) as g:
            if g.career.club is None:g.career.accept_starting_offer(g.career.offers[0])
            for seed in range(12):
                g.career.rng.seed(seed);g._randomize_aim_pattern();points=[]
                for step in range(2400):
                    g.aim_phase=step*.025;g._apply_aim_pattern();points.append((g.aim_x,g.aim_z))
                    self.assertLess(abs(g.aim_x)+g.ball.radius,g.goal_half_width)
                    self.assertGreater(g.aim_z,g.ball.radius)
                    self.assertLess(g.aim_z+g.ball.radius,g.goal_height)
                self.assertLess(min(x for x,z in points),-1.8)
                self.assertGreater(max(x for x,z in points),1.8)
                self.assertLess(min(z for x,z in points),.65)
                self.assertGreater(max(z for x,z in points),1.7)

    def test_arms_keep_fixed_length_even_when_save_target_is_unreachable(self):
        with isolated_game(saved=True) as g:
            if g.career.club is None:g.career.accept_starting_offer(g.career.offers[0])
            for side in (-1,1):
                for high,low in ((1,0),(0,1),(.4,.5)):
                    for step in range(21):
                        g.goalkeeper_dive_sign=side;g.goalkeeper_high_reach=high;g.goalkeeper_low_reach=low
                        g.goalkeeper_dive_progress=step/20;g.goalkeeper_dive_amount=1;g.goalkeeper_dive_age=step*.05
                        g.goalkeeper_save_x=side*8;g.goalkeeper_save_height=.2 if low else 3
                        p=g._goalkeeper_pose()
                        for s in ('l','r'):
                            self.assertAlmostEqual(math.dist(p['hand_'+s],p['shoulder_'+s]),.68*g.goalkeeper_scale)

    def test_every_training_shot_has_only_shooter_and_keeper(self):
        with isolated_game(saved=True) as g:
            if g.career.club is None:g.career.accept_starting_offer(g.career.offers[0])
            g.shot_context='training'
            for seed in range(50):
                g.career.rng.seed(seed);g._prepare_next_shot()
                self.assertEqual(g.field_players,[])
                self.assertEqual(g.shot_type,'kick')
            g.shot_context='match';g.current_chance_difficulty='hard';g._prepare_next_shot()
            self.assertTrue(g.field_players)

    def test_scoreboard_never_draws_badges(self):
        with isolated_game(saved=True) as g:
            if g.career.club is None:g.career.accept_starting_offer(g.career.offers[0])
            g.match_home,g.match_away=g.career.next_fixture()
            with patch.object(g,'_draw_club_badge',create=True) as badge:g._draw_match_overlay()
            badge.assert_not_called()

    def test_training_progress_and_advice_are_visible_and_use_saved_values(self):
        with isolated_game(saved=True) as g:
            if g.career.club is None:g.career.accept_starting_offer(g.career.offers[0])
            self.addCleanup(setattr,Window,'size',Window.size)
            Window.size=(960,540);settle();g.size=Window.size
            c=g.career;c.begin_training();c.record_training_shot(True)
            g.view='training';g.draw();settle()
            labels=[w.text for w in g.walk() if isinstance(w,Label)]
            self.assertIn('Completed shots: 1/3 · Goals: 1/3',labels)
            self.assertIn('SESSION PLAN',labels);self.assertIn('PLAYER READINESS',labels)

    def test_coach_has_three_distinct_paragraphs_in_each_context_and_language(self):
        from localization import Localizer,LANGUAGES
        for kind in ('drought','decisive','key_match'):
            for style in range(3):
                text=conversation_text(dict(kind=kind,style=style,variant=0))
                self.assertEqual(len(text.split('\n\n')),3)
                for lang in LANGUAGES:
                    loc=Localizer(world=True);loc.choose(lang)
                    result=loc.tr(text)
                    self.assertEqual(len(result.split('\n\n')),3)
                    if lang!='en':self.assertNotEqual(result,text)
