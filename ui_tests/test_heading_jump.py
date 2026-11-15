import copy,unittest
from unittest.mock import patch
from test_menus import isolated_game
from retro_sprites import hero_pose,projected_scale,PLAYER_HEIGHT_METRES
from heading_animation import root_target,WINDUP_SECONDS
from main import HEADER_BALL_HEIGHT
class JumpingHeaders(unittest.TestCase):
 def prepare(self,g):
  c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True;g.view='shot';g.shot_context='training';g._start_opportunity('cross',35);g.buildup_progress=.999;g._update_buildup(.2)
 def test_crouch_takeoff_contact_land_and_single_frozen_aim_launch(self):
  with isolated_game()as g:
   self.prepare(g);g.shot_time_left=.05;before=copy.deepcopy(vars(g.ball));attempts=g.attempts
   g.shoot(1.,1.);self.assertEqual((g.aim_x,g.aim_z),(1.,1.));g.shoot(-2.,2.);self.assertEqual(vars(g.ball),before);self.assertEqual(g.attempts,attempts)
   g.update(.08);self.assertEqual(hero_pose(g).frame,1);self.assertEqual(g.shot_time_left,.05);self.assertFalse(g.ball.active)
   g.update(.08);self.assertEqual(hero_pose(g).frame,2);self.assertFalse(g.ball.active)
   g.update(.06);self.assertEqual(g.state,g.STATE_SHOT);self.assertEqual(hero_pose(g).frame,3);self.assertEqual(g.attempts,attempts+1);self.assertEqual((g.aim_x,g.aim_z),(1.,1.));self.assertTrue(g.ball.active);self.assertEqual(g.ball.z,HEADER_BALL_HEIGHT)
   r=g._retro_renderer();position=(0.,10.,0.);contact=g.project(0.,10.,HEADER_BALL_HEIGHT);pose=hero_pose(g)
   target=root_target(g,r,pose,position,contact);character=r.manifest['characters']['players'];hx,hy=character['animations']['HEADER']['joints']['back'][3]['forehead'];ax,ay=character['anchor'];scale=projected_scale(g,position,character,PLAYER_HEIGHT_METRES)
   self.assertAlmostEqual(target[0]+(hx+.5-ax)*scale,contact[0]);self.assertAlmostEqual(target[1]+(ay-hy-.5)*scale,contact[1])
   ankle=character['animations']['HEADER']['joints']['back'][3]['ankle_0'][1]
   self.assertGreater(target[1]+(ay-ankle-.5)*scale-g.project(*position)[1],6*scale)
   g.player_kick_progress=1.;self.assertEqual(hero_pose(g).frame,7);self.assertEqual(root_target(g,r,hero_pose(g),position,contact),g.project(*position))
 def test_drawing_never_moves_ball_and_reset_discards_pending_header(self):
  with isolated_game()as g:
   self.prepare(g);g.shoot();g.update(.08);before=copy.deepcopy(vars(g.ball));g._draw_player();self.assertEqual(vars(g.ball),before)
   g._start_opportunity('penalty',37);self.assertIsNone(g._header_pending);g.state=g.STATE_AIMING;g.shoot(.5,.5);self.assertEqual(g.state,g.STATE_SHOT)
