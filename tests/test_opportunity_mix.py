import unittest
from types import SimpleNamespace as NS
from career import CareerMode,CareerClub,expected_highlight_goals
from newspaper import single_page_story,clock
from localization import Localizer
class OpportunityMix(unittest.TestCase):
    def test_quality_caps_remain_but_even_elite_allows_a_clear_chance(self):
        c=CareerMode(autoload=False)
        probabilities=[]
        for rating in (45,70,95):
            p=c.opponent_chance_profile(CareerClub('Opponent','Germany','Test',1,rating,uid='test'))
            probabilities.append(p.clear_chance_probability)
            self.assertGreaterEqual(p.clear_chance_probability,.35);self.assertLessEqual(p.clear_chance_probability,.9)
        self.assertEqual(probabilities,sorted(probabilities,reverse=True))
    def test_penalty_contribution_is_reserved_without_double_counting_single_chance(self):
        self.assertEqual(expected_highlight_goals(0,1,1),0)
        self.assertAlmostEqual(expected_highlight_goals(1,1,1),.65)
        self.assertAlmostEqual(expected_highlight_goals(2,1,1),.65+.51)
        self.assertAlmostEqual(expected_highlight_goals(3,.6,.18),.867)
        self.assertEqual(expected_highlight_goals(3,.6,-1),expected_highlight_goals(3,.6))
    def test_concise_story_preserves_goal_minutes_and_player_verdict(self):
        r=dict(score=[2,1],events=[dict(minute=32,half=1,side='home'),dict(minute=48,half=1,side='away'),dict(minute=91,half=2,side='home')],goals=1,negative_run=0)
        text=single_page_story(r,Localizer(False).tr,'Alex')
        for minute in ("32'","45+3'","90+1'"):self.assertIn(minute,text)
        self.assertIn('Alex: one goal.',text)
        r['events']=[];self.assertIn('unavailable',single_page_story(r,Localizer(False).tr,'Alex'))
