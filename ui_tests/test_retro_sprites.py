"""Real Kivy rendering of approved sprites, with gameplay-state isolation."""
import unittest,copy,math
from dataclasses import asdict
from test_menus import isolated_game,settle
from retro_sprites import hero_pose,field_pose,keeper_pose,kit_palette

class RetroSpriteIntegration(unittest.TestCase):
    def test_all_actor_roles_use_180cm_reference_at_their_world_depth(self):
        from unittest.mock import patch
        from retro_sprites import PLAYER_HEIGHT_METRES,projected_scale
        with isolated_game() as g:
            self.prepare(g);g._start_opportunity('cutback',42)
            renderer=g._retro_renderer()
            with patch.object(renderer,'draw',wraps=renderer.draw) as draw:
                g.draw()
            self.assertGreaterEqual(len(draw.call_args_list),3)
            self.assertTrue(all(call.args[5]==1.80 for call in draw.call_args_list))
            for character in renderer.manifest['characters'].values():
                for x,y in ((0,0),(-5,8),(3,19)):
                    scale=projected_scale(g,(x,y,0),character)
                    foot=g.project(x,y,0);head=g.project(x,y,1.80)
                    expected=math.hypot(head[0]-foot[0],head[1]-foot[1])
                    self.assertAlmostEqual(scale*character['standing_height_pixels'],expected)
            # Goal remains 2.44m. No old .72/.76/.80 physics scale shrinks art.
            self.assertEqual(g.goal_height,2.44);self.assertEqual(PLAYER_HEIGHT_METRES,1.80)
            g._start_opportunity('corner',42)
            while g.state==g.STATE_BUILDUP:g.update(.1)
            g.state_age=.3
            self.assertEqual(hero_pose(g).frame,0)
            height=g.ball.z;g.shoot(2.,1.)
            self.assertEqual(hero_pose(g).frame,3)
            self.assertEqual(g.ball.z,height)

    def test_recoloured_pixels_restore_after_context_reload_and_eviction_is_bounded(self):
        from sprite_animation import load_manifest
        from sprite_textures import TextureCache,DEFAULT_PLAYER
        manifest=load_manifest();cache=TextureCache(manifest,limit=2)
        clips=list(manifest['characters']['players']['animations'].values())
        textures=[]
        for clip in clips[:3]:
            texture=cache.get(clip['sheets']['front']['path'],DEFAULT_PLAYER)
            pixels=bytes(texture.pixels)
            texture.blit_buffer(bytes(len(pixels)),colorfmt='rgba',bufferfmt='ubyte')
            self.assertNotEqual(bytes(texture.pixels),pixels)
            cache._reload_texture(texture)
            self.assertEqual(bytes(texture.pixels),pixels)
            self.assertEqual((texture.min_filter,texture.mag_filter),('nearest','nearest'))
            textures.append(texture)
        self.assertEqual(len(cache.payloads),2)
        self.assertNotIn(id(textures[0]),cache.payloads)

    def prepare(self,g):
        g.career.accept_starting_offer(g.career.offers[0]);g.career.attend_coach_meeting();g.career.attend_coach_meeting()
        g._career_started=True;g.view='shot';g.shot_context='match';g._prepare_next_shot()

    def physics(self,g):
        return (copy.deepcopy(vars(g.ball)),{k:copy.deepcopy(v) for k,v in vars(g).items() if k.startswith('goalkeeper_')},[(p.x,p.y,p.team,p.phase) for p in g.field_players],g.attempts,g.goals,g.shot_time_left)

    def test_approved_art_renders_without_mutating_ball_actors_keeper_or_hitboxes(self):
        with isolated_game() as g:
            self.prepare(g)
            for kind in ('through_ball','cutback','corner','rebound','penalty'):
                g._start_opportunity(kind,42)
                for progress in (0.,.4,.51,.9):
                    if g.current_opportunity.duration:
                        g.buildup_progress=progress;g.state_age=progress*g.current_opportunity.duration
                    before=self.physics(g);g.draw();self.assertEqual(self.physics(g),before)
                    for player in g.field_players+g.buildup_actors:
                        self.assertIn(field_pose(g,player).state,('RUN','DRIBBLE','PASS','SHOOT','TACKLE','IDLE'))
                g.state=g.STATE_AIMING;g.state_age=.3;g.draw()
                self.assertEqual(hero_pose(g).frame,0 if g.shot_type=='header' else 2)
                g.shoot(2.,1.)
                self.assertEqual(hero_pose(g).frame,3)
                self.assertTrue(g.ball.active)
                before=self.physics(g);g.draw();self.assertEqual(self.physics(g),before)
            for state in (g.STATE_SHOT,g.STATE_RESULT):
                g.state=state;g.state_age=1.4
                for sign in (-1.,1.):
                    for high,low,amount in ((0.,1.,.1),(1.,0.,.1),(0.,0.,1.)):
                        g.goalkeeper_is_diving=True;g.goalkeeper_dive_sign=sign
                        g.goalkeeper_dive_amount=amount;g.goalkeeper_high_reach=high;g.goalkeeper_low_reach=low
                        for age in (0.,.15,.35,.6,.9):
                            g.goalkeeper_dive_age=age;g.goalkeeper_dive_progress=min(1,age*2.2)
                            before=self.physics(g);g.draw();self.assertEqual(self.physics(g),before)
            g.goalkeeper_is_diving=False;g.goalkeeper_holding=True
            for age in (0.,.3,.8):
                g.goalkeeper_catch_age=age;g._attach_held_ball();before=self.physics(g)
                g.draw();self.assertEqual(self.physics(g),before)
            self.assertEqual(g._retro_renderer().manifest['approval_status'],'APPROVED')

    def test_event_choices_recovery_and_existing_team_colours(self):
        with isolated_game() as g:
            self.prepare(g);g._start_opportunity('rebound',1)
            g.buildup_progress=.5;g.state_age=g.current_opportunity.duration*.5
            self.assertEqual(field_pose(g,g.buildup_blocker).state,'TACKLE')
            g.goalkeeper_is_diving=True;g.goalkeeper_dive_amount=1;g.goalkeeper_high_reach=0;g.goalkeeper_low_reach=0
            self.assertEqual(keeper_pose(g,False).state,'DIVE_LEFT')
            self.assertEqual(keeper_pose(g,True).state,'DIVE_RIGHT')
            g.state=g.STATE_RESULT;g.state_age=1.1;g.ball.active=False
            self.assertEqual(keeper_pose(g).state,'RECOVER')
            kit=((1.,0.,0.,1.),(0.,0.,0.,1.),(1.,0.,0.,1.),(0.,0.,0.,1.))
            self.assertEqual(kit_palette(kit),('FF0000','000000','000000','FF0000','F9FDF1'))
            g.shot_context='training';g._prepare_next_shot();g.draw()
            self.assertEqual({p.team for p in g.field_players+g.buildup_actors},{'attacker','defender'})
            from training_opportunities import BIB_KITS
            self.assertEqual(g._match_outfield_kits(),BIB_KITS)
            self.assertTrue({'hero','keeper'}.issubset(g._retro_renderer().clocks))
            self.assertEqual({id(p) for p in g.field_players+g.buildup_actors}, {k for k in g._retro_renderer().clocks if isinstance(k,int)})
            renderer=g._retro_renderer();before=renderer.cache.allocations
            for _ in range(100):g.draw()
            self.assertEqual(renderer.cache.allocations,before)
            self.assertLessEqual(len(renderer.cache.entries),24)
            for texture in renderer.cache.entries.values():
                self.assertEqual((texture.min_filter,texture.mag_filter),('nearest','nearest'))
