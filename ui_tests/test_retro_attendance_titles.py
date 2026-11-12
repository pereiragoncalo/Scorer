import copy,unittest
from unittest.mock import patch
from kivy.uix.button import Button
from test_menus import isolated_game,settle
from retro_props import cache
from stadium_scene import animate_crowd
import honours,title_events
class RetroSceneTests(unittest.TestCase):
    def prepare(self,g):
        from test_club_stadium import ClubStadium
        ClubStadium().teams(g);g.career.attend_coach_meeting();g.view='shot';g.shot_context='match';g._prepare_next_shot();return g.career
    def test_ball_sprite_keeps_physics_and_textures_recover_without_growth(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            self.prepare(g);state=copy.deepcopy(vars(g.ball));g._draw_ball();textures=cache(g);n=textures.allocations
            for i in range(100):g.elapsed=i*.01;g._draw_ball()
            self.assertEqual(vars(g.ball),state);self.assertEqual(textures.allocations,n)
            t=textures.get('ball.png');pixels=bytes(t.pixels);textures._reload(t);self.assertEqual(bytes(t.pixels),pixels);self.assertEqual(t.mag_filter,'nearest')
    def test_crowd_is_two_textured_batches_and_opponents_and_stewards_stay_still(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            self.prepare(g);g._draw_stadium_stands();self.assertEqual(set(g._crowd_textures),{'home','away'});self.assertTrue(g._crowd_mesh_cache);self.assertTrue(all(len(row[2])<=24000 for row in g._crowd_mesh_cache))
            self.assertLess(g.crowd_total,g.crowd_available);guard=copy.deepcopy(g._steward_mesh_cache)
            g._record_report_goal('away',30);g.elapsed+=.4;animate_crowd(g)
            self.assertTrue(all(g._crowd_motion_offsets[i]==0 for i,m in enumerate(g._crowd_motions) if m[0]=='home'));self.assertEqual(g._steward_mesh_cache,guard)
    def test_title_sequence_reloads_and_special_coach_keeps_weekly_focus(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=self.prepare(g);focus=c.training_focus;row=dict(season=c.season,competition='cup:qa',title='QA collective cup',team_uid=c.club.uid,team=c.club.name,country=c.club.country)
            honours.award(c,row);c.post_match_stage='newspaper';c.save();g.view='hub';g.draw();settle();self.assertEqual(g.view,'trophy')
            ball=copy.deepcopy(vars(g.ball));scores=c.goals,c.matches;g.elapsed+=6.;g.draw();self.assertEqual(vars(g.ball),ball);self.assertEqual((c.goals,c.matches),scores)
            g._activate_ui('title_continue');settle();self.assertEqual(g.view,'title_coach');self.assertTrue(c.load());g._menu._signature=None;g.draw();settle()
            self.assertEqual(len(g._menu.body.choices),0);self.assertFalse(g._menu.body.finish.disabled)
            g._activate_ui('title_coach_complete');g.draw();settle();self.assertEqual(g.view,'newspaper');self.assertEqual(c.training_focus,focus);self.assertIsNone(title_events.pending(c))
    def test_due_weekly_talk_requires_two_options_and_cannot_skip_special_talk(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=self.prepare(g);honours.award(c,dict(season=c.season,competition='cup:qa',title='QA cup',team_uid=c.club.uid,team=c.club.name,country=c.club.country));title_events.to_coach(c);c.week+=1
            g.view='title_coach';g.draw();settle();self.assertEqual(len(g._menu.body.choices),2);g._activate_ui('title_coach_complete');self.assertEqual(g.view,'title_coach')
            pick=c.coach_focus_options()[0];g._activate_ui('coach_focus',pick);g.draw();g._activate_ui('title_coach_complete');self.assertTrue(c.coach_meeting_held);self.assertEqual(c.training_focus,pick)
