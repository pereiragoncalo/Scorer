"""Real save contacts, front-fall presentation and paused forehead placement."""
import copy,math,unittest
from unittest.mock import patch
from test_menus import isolated_game
from main import GOALKEEPER_Y,HEADER_BALL_HEIGHT,PHYSICS_STEP
from retro_sprites import keeper_pose,hero_pose

class KeeperHeaderContactTests(unittest.TestCase):
 def prepare(self,g):
  c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True;g.view='shot';g.shot_context='match';g._prepare_next_shot()
 def test_central_high_glove_contact_tips_over_bar_on_physical_trajectory(self):
  with isolated_game() as g:
   self.prepare(g);g.state=g.STATE_SHOT;g.outcome_registered=False;g.goalkeeper_x=0.;g.goalkeeper_is_diving=True;g.goalkeeper_high_reach=1.;g.goalkeeper_dive_amount=.0;g.goalkeeper_dive_age=.18;g.goalkeeper_dive_progress=.4
   pose=g._goalkeeper_pose();hand=pose['hand_r'];g.ball.reset(hand[0],GOALKEEPER_Y+.1,hand[1]);g.ball.vy=-18.;g.ball.vz=0.;g.ball.active=True
   self.assertGreater(g.ball.z,g.goal_height*.70);self.assertTrue(g._collide_goalkeeper());self.assertTrue(g.ball.goalkeeper_touched);self.assertEqual(keeper_pose(g).state,'TIP_OVER');self.assertLess(g.ball.vy,0);self.assertGreater(g.ball.vz,0);self.assertTrue(g.ball.active)
   for _ in range(200):
    g._update_goalkeeper_shot(PHYSICS_STEP);g._update_ball(PHYSICS_STEP)
    if g.last_goal_line_point is not None:break
   self.assertIsNotNone(g.last_goal_line_point);self.assertGreater(g.last_goal_line_point[1],g.goal_height+g.ball.radius);self.assertNotEqual(g.result_text,'GOAL!')
 def test_high_ball_without_real_contact_is_not_redirected(self):
  with isolated_game() as g:
   self.prepare(g);g.goalkeeper_is_diving=True;g.goalkeeper_high_reach=1.;g.goalkeeper_dive_amount=0.;g.ball.reset(3.1,GOALKEEPER_Y+.1,2.2);g.ball.vy=-18.;before=copy.deepcopy(vars(g.ball))
   self.assertFalse(g._collide_goalkeeper());self.assertEqual(vars(g.ball),before);self.assertLess(g.goalkeeper_tip_age,0)
 def test_frontal_catch_keeps_ball_at_gloves_and_has_no_sideways_roll(self):
  with isolated_game() as g:
   self.prepare(g);g.goalkeeper_holding=True;g.goalkeeper_catch_age=.8;g._attach_held_ball();before=copy.deepcopy(vars(g.ball))
   renderer=g._retro_renderer()
   with patch.object(renderer,'draw') as draw:g._draw_goalkeeper()
   self.assertEqual(draw.call_args.kwargs['rotation'],0.);self.assertLess(draw.call_args.kwargs['vertical_scale'],.5);self.assertEqual(vars(g.ball),before)
   p=g._goalkeeper_world_pose();expected=tuple((a+b)/2 for a,b in zip(p['hand_l'],p['hand_r']));self.assertAlmostEqual(g.ball.x,expected[0]);self.assertAlmostEqual(g.ball.y,expected[1])
 def test_header_waits_before_forehead_then_uses_authored_contact_frame(self):
  with isolated_game() as g:
   self.prepare(g);g._start_opportunity('cross',35);g.buildup_progress=.999;g._update_buildup(.2)
   self.assertEqual(g.state,g.STATE_AIMING);self.assertEqual(g.ball.z,HEADER_BALL_HEIGHT);self.assertFalse(g.ball.active);self.assertEqual(hero_pose(g).frame,0)
   renderer=g._retro_renderer();before=copy.deepcopy(vars(g.ball))
   with patch.object(renderer,'draw') as draw:g._draw_player()
   self.assertEqual(draw.call_args.kwargs['joint'],'forehead');self.assertEqual(vars(g.ball),before)
   g.shoot(1.,1.);self.assertEqual(hero_pose(g).frame,3);self.assertTrue(g.ball.active);self.assertEqual(g.ball.z,HEADER_BALL_HEIGHT)
