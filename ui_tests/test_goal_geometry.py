import unittest
from unittest.mock import patch
from kivy.core.window import Window
from career import GOAL_WIDTH,GOAL_HEIGHT,PHYSICS_STEP,GOALKEEPER_Y
from test_menus import isolated_game,settle

class WindowsGoalTests(unittest.TestCase):
    def test_instance_geometry_updates_render_profile_aim_and_clamp_without_android_change(self):
        with patch('release_settings.DESKTOP_WINDOWS',True,create=True),isolated_game() as g:
            self.assertAlmostEqual(g.goal_width,GOAL_WIDTH*1.12);self.assertAlmostEqual(g.goal_height,GOAL_HEIGHT*1.10)
            self.assertAlmostEqual(g.aim_center_z,g.goal_height*.5)
            self.assertEqual(g._veil_profile(0),(0,g.goal_height))
            self.assertAlmostEqual(g._veil_profile(1)[1],0)
            self.assertAlmostEqual(g._veil_height_at_y(-.2),g.goal_height)
            self.assertAlmostEqual(g._veil_amount_at_y(-.2),.2/g.goal_geometry.veil_path_length)
        with isolated_game() as g:self.assertEqual((g.goal_width,g.goal_height),(GOAL_WIDTH,GOAL_HEIGHT))
    def test_new_mouth_counts_goal_in_extended_width_but_not_outside_or_high(self):
        with patch('release_settings.DESKTOP_WINDOWS',True,create=True),isolated_game() as g:
            g.draw=lambda:None
            for x,z,expected in ((3.85,1.1,True),(0,2.49,True),(4.5,1.1,False),(0,2.95,False)):
                g.view='shot';g.state=g.STATE_SHOT;g.outcome_registered=False;g.result_text='';g.goalkeeper_holding=False
                b=g.ball;b.x=x;b.y=.02;b.z=z;b.vx=0;b.vy=-15;b.vz=0;b.crossed_goal=False;b.active=True
                with patch.object(g,'_collide_field_players'),patch.object(g,'_collide_goalkeeper',return_value=False),patch.object(g,'_collide_net'),patch.object(g,'_play_goal_crowd_sound'):
                    g._update_ball(PHYSICS_STEP)
                self.assertEqual(g.result_text=='GOAL!',expected,(x,z,g.result_text))
    def test_ball_render_order_uses_depth_for_active_stopped_and_held_ball(self):
        with isolated_game() as g:
            for active in (True,False):
                for y in (-1.0,.35,2.0):
                    g.view='shot';g.ball.active=active;g.ball.y=y;g.goalkeeper_holding=False;calls=[]
                    methods=('_draw_background','_draw_stadium_stands','_draw_pitch','_draw_world_promotion_boards','_draw_goal_net','_draw_field_players','_draw_player','_draw_aim_marker','_draw_hud')
                    with __import__('contextlib').ExitStack() as stack:
                        for method in methods:stack.enter_context(patch.object(g,method))
                        for name in ('_draw_ball','_draw_goal_frame','_draw_goalkeeper'):
                            stack.enter_context(patch.object(g,name,side_effect=lambda n=name:calls.append(n)))
                        g.draw()
                    self.assertEqual(calls.count('_draw_ball'),1)
                    self.assertEqual(calls.index('_draw_ball')<calls.index('_draw_goalkeeper'),y<GOALKEEPER_Y-g.ball.radius)
                    self.assertEqual(calls.index('_draw_ball')<calls.index('_draw_goal_frame'),y<0)
            g.goalkeeper_holding=True;g.ball.y=-1;self.assertFalse(g._ball_behind_keeper())
    def test_windows_goal_net_and_sponsor_boards_render_after_resize(self):
        with patch('release_settings.DESKTOP_WINDOWS',True,create=True),isolated_game() as g:
            g.view='shot';g.ball.active=False;g.ball.y=-.8;g.ball.z=.5
            for size in ((1280,720),(800,600)):
                Window.size=size;g.size=size;g.draw();settle()
                self.assertIn('YOUR COMPANY HERE',g._promotion_textures);self.assertLessEqual(len(g._promotion_textures),4)
                l=g.project(-g.goal_half_width,0,0);r=g.project(g.goal_half_width,0,0)
                self.assertGreater(abs(r[0]-l[0]),1);self.assertTrue(g._ball_behind_keeper())
    def test_real_post_and_crossbar_collisions_match_enlarged_geometry(self):
        with patch('release_settings.DESKTOP_WINDOWS',True,create=True),isolated_game() as g:
            for x,z in ((g.goal_half_width,1.1),(0,g.goal_height)):
                b=g.ball;b.x=x;b.y=.01;b.z=z;b.vx=0;b.vy=-10;b.vz=0;b.post_cooldown=0
                g.outcome_registered=False;self.assertTrue(g._collide_goal_frame())
                self.assertEqual(g.result_text,'OFF THE POST!')

    def test_windows_keeper_pose_collision_scale_and_faster_flight_are_isolated(self):
        poses=[]
        for desktop in (False,True):
            with patch('release_settings.DESKTOP_WINDOWS',desktop,create=True),isolated_game() as g:
                g.power=.85;g.state=g.STATE_AIMING
                poses.append(g._goalkeeper_pose())
                self.assertAlmostEqual(g.goalkeeper_scale,.8*(.86 if desktop else 1))
                for hard in (False,True):
                    for distance in (1,15,40):
                        from career import clamp
                        expected=clamp(distance/((17 if hard else 18)+.85*8),.28 if hard else .2,.82 if hard else 1.15)
                        self.assertAlmostEqual(g._shot_flight_time(distance,hard),expected/(1.22 if desktop else 1))
                for context in ('training','match'):
                    g.shot_context=context
                    with patch.object(g,'_draw_stand_meshes') as stands,patch.object(g,'_draw_crowd_meshes') as crowd:
                        g._draw_stadium_stands()
                        stands.assert_called_once()
                        self.assertEqual(crowd.called,context!='training')
        for key in poses[0]:
            self.assertAlmostEqual(poses[1][key][1],poses[0][key][1]*.86)

    def test_crossed_shots_reach_marker_from_both_sides_in_every_profile(self):
        from contextlib import ExitStack
        for desktop in (False,True):
            with patch('release_settings.DESKTOP_WINDOWS',desktop,create=True),isolated_game() as g:
                g.draw=lambda:None;g.shot_context='match'
                for origin in (-12,-6,0,6,12):
                    for target in (-2.5,0,2.5):
                        g.shot_origin_x=origin;g.shot_origin_y=18;g.shot_type='normal'
                        g.state=g.STATE_AIMING;g.power=.85
                        with ExitStack() as stack:
                            for method in ('_collide_field_players','_collide_goal_frame','_collide_goalkeeper','_collide_net','_play_goal_crowd_sound'):
                                stack.enter_context(patch.object(g,method,return_value=False))
                            g.shoot(target,1.4)
                            for _ in range(400):
                                g._update_ball(PHYSICS_STEP)
                                if g.ball.crossed_goal:break
                        self.assertIsNotNone(g.last_goal_line_point)
                        self.assertAlmostEqual(g.last_goal_line_point[0],target,places=5)
                        self.assertAlmostEqual(g.last_goal_line_point[1],1.4,places=5)
