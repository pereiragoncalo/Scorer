import math,random,unittest
from unittest.mock import patch
from test_menus import isolated_game
from main import PHYSICS_STEP

class DefensiveDifficultyUI(unittest.TestCase):
    def test_opponent_tier_controls_keeper_and_defenders_do_not_read_aim(self):
        from career import CareerClub
        with isolated_game(saved=True) as g:
            if g.career.club is None:g.career.accept_starting_offer(g.career.offers[0]);g.career.attend_coach_meeting()
            g.shot_context='match';g.current_chance_difficulty='hard'
            g.match_home=g.career.club;g.match_away=CareerClub('Elite','England','Test',1,90,uid='opponent')
            self.assertEqual(g._defensive_profile().level,1)
            g.shot_origin_x=5;g.shot_origin_y=18;g.shot_type='kick'
            g.career.rng.seed(123);random.seed(123);g.aim_x=-3.4;g._generate_field_players();before=[(p.x,p.y) for p in g.field_players]
            g.career.rng.seed(123);random.seed(123);g.aim_x=3.4;g._generate_field_players();self.assertEqual(before,[(p.x,p.y) for p in g.field_players]);self.assertEqual(len(before),7)
    def test_save_pose_reaches_both_high_and_low_and_collision_uses_same_pose(self):
        with isolated_game(saved=True) as g:
            if g.career.club is None:g.career.accept_starting_offer(g.career.offers[0]);g.career.attend_coach_meeting()
            g.shot_context='match';g.current_chance_difficulty='hard';g.goalkeeper_is_diving=True
            g.goalkeeper_dive_progress=.9;g.goalkeeper_dive_amount=.9;g.goalkeeper_dive_age=.28;g.goalkeeper_dive_sign=1
            g.goalkeeper_high_reach=1;g.goalkeeper_low_reach=0
            high=g._goalkeeper_pose()['hand_r'];self.assertGreater(high[1],2.0)
            g.goalkeeper_high_reach=0;g.goalkeeper_low_reach=1
            low=g._goalkeeper_pose()['hand_r'];self.assertLess(low[1],.40)
            g.ball.reset(low[0],.85,low[1]);g.ball.vy=-15
            self.assertTrue(g._collide_goalkeeper())
    def test_tier_and_recent_scoring_do_not_redirect_an_unobstructed_shot(self):
        with isolated_game(saved=True) as g:
            if g.career.club is None:g.career.accept_starting_offer(g.career.offers[0]);g.career.attend_coach_meeting()
            g.shot_context='match';g.current_chance_difficulty='hard'
            velocities=[]
            for tier in (5,1):
                g.career.club.tier=tier;g.career.goals=100 if tier==1 else 0;g._prepare_next_shot();g.shot_type='kick';g.shot_origin_x=4;g.shot_origin_y=17;g.power=.85
                g.shoot(2.8,1.2);velocities.append((g.ball.vx,g.ball.vy,g.ball.vz))
            self.assertEqual(velocities[0],velocities[1])
