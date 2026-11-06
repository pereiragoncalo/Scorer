"""Native club navigation, host ground, supporter sectors and scorer-only cheers."""
import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.metrics import Metrics
from kivy.uix.label import Label
from club_profiles import profile
from stadium_scene import context,away_seat,jump,cheering,seat_noise
from test_menus import isolated_game,settle

class ClubStadium(unittest.TestCase):
    def test_seat_colours_are_mixed_stable_and_do_not_consume_gameplay_randomness(self):
        import random
        before=random.getstate()
        def row(r):return [seat_noise(-35.5+c*71/163,-4.4-r*.85,.3+r*.27,c*17+r*31,12345)&1 for c in range(164)]
        rows=[row(r) for r in range(12)]
        self.assertEqual(rows,[row(r) for r in range(12)])
        self.assertEqual(before,random.getstate())
        bits=[bit for values in rows for bit in values]
        self.assertTrue(.4<sum(bits)/len(bits)<.6)
        for values in rows:
            self.assertGreater(sum(a!=b for a,b in zip(values,values[1:])),45)
        self.assertGreater(sum(a!=b for a,b in zip(rows[0],rows[1])),45)

    def test_no_supporter_banner_is_drawn(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            self.teams(g)
            with patch.object(g,'_draw_text') as text:
                g._draw_stadium_stands()
            text.assert_not_called()
            self.assertNotIn('banner',context(g))

    def teams(self,g):
        c=g.career
        clubs={x.uid:x for l in c.leagues.values() for x in l.clubs}
        player=clubs['f9554f2ce1ab5ff99892'];opponent=clubs['7347ae77d98a546baffd']
        c.league_key=next(k for k,l in c.leagues.items() if player in l.clubs);c.club_name=player.name
        c.display_aliases['clubs'].update({player.uid:'Vitória BA',opponent.uid:'Bahia'});c.alias_revision+=1;g._career_started=True
        g.shot_context='match';g.match_is_international=False;g.match_home=opponent;g.match_away=player
        return player,opponent

    def test_host_stadium_is_used_when_player_is_away_and_training_uses_own_ground(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            player,home=self.teams(g);g._draw_stadium_stands()
            self.assertEqual(g.stadium_capacity,profile(home)['capacity']);self.assertEqual(g.stadium_tiers,2)
            self.assertGreater(g.crowd_team_counts['home'],0);self.assertGreater(g.crowd_team_counts['away'],0)
            self.assertFalse(hasattr(g,'away_banner_text'))
            g.shot_context='training';g._draw_stadium_stands()
            self.assertEqual(g.stadium_capacity,profile(player)['capacity']);self.assertEqual(g.stadium_tiers,1)
            with patch.object(g,'_draw_crowd_meshes') as crowd:g._draw_stadium_stands();crowd.assert_not_called()

    def test_fixture_and_alias_changes_invalidate_supporter_cache_without_resize(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            player,home=self.teams(g);g._draw_stadium_stands();first=g._crowd_mesh_cache;key=g._crowd_mesh_cache_key
            g.match_home,g.match_away=player,home;g._draw_stadium_stands()
            self.assertNotEqual(key,g._crowd_mesh_cache_key);self.assertIsNot(first,g._crowd_mesh_cache)
            self.assertFalse(hasattr(g,'away_banner_text'))
            g.match_away=next(x for l in g.career.leagues.values() for x in l.clubs if not profile(x)['supporters'])
            g.career.display_aliases['clubs'][g.match_away.uid]='Custom visitors';g._draw_stadium_stands()
            self.assertFalse(hasattr(g,'away_banner_text'))

    def test_away_sector_is_only_lower_deck_and_palette_batches_are_team_tagged(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            self.teams(g);g._draw_stadium_stands()
            self.assertTrue(away_seat(30,-5,0));self.assertFalse(away_seat(30,-25,1));self.assertFalse(away_seat(-20,-5,0));self.assertFalse(away_seat(40,5,0,'side'))
            self.assertEqual({row[4] for row in g._crowd_mesh_cache},{'home','away'})
            self.assertLessEqual(len(g._crowd_mesh_cache),56)
            for color,vertices,indices,group,team in g._crowd_mesh_cache:
                self.assertTrue(indices);self.assertLess(max(indices),65536);self.assertLess(max(indices),len(vertices)//4)

    def test_visitor_club_size_controls_sector_and_two_files_flank_each_stair(self):
        import stadium_scene
        from supporter_layout import FIRST_GOAL_STAIR_X,STAIR_HALF_WIDTH
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            away,home=self.teams(g)
            original=stadium_scene.build_crowd;seats=[]
            def capture(game,spectators,ctx=None):
                seats[:]=spectators;return original(game,spectators,ctx)
            for capacity in (5000,60000):
                with patch('stadium_scene.stadium_capacity',side_effect=lambda club: capacity if club is away else 70000),patch('stadium_scene.build_crowd',side_effect=capture):
                    g._draw_stadium_stands()
                    visitors=[p for p in seats if p[4]=='away']
                    self.assertTrue(visitors);self.assertTrue(all(p[5]==0 for p in visitors))
                    if capacity==5000:self.assertTrue(all(p[0]>36.2 and p[1]<-4 for p in visitors))
                    else:
                        behind=[p for p in visitors if p[0]<=36.2]
                        self.assertTrue(behind)
                        self.assertTrue(all(p[0]>FIRST_GOAL_STAIR_X+STAIR_HALF_WIDTH for p in behind))
                    ctx=context(g);self.assertEqual(g.stadium_capacity,70000)
                    self.assertEqual(len(g.steward_positions),4*ctx['ground'].lower_rows)
                    self.assertEqual({(p[3],p[4]) for p in g.steward_positions},{('goal',0),('goal',1),('side',0),('side',1)})
                    self.assertGreater(g.steward_visible,0)
                    self.assertIn((.46,1.,.015,1),[p[0] for p in g._steward_mesh_cache])
                    guards=g._steward_mesh_cache
                    g._record_report_goal('away',10);g.elapsed+=.1;g._draw_stadium_stands()
                    self.assertIs(g._steward_mesh_cache,guards)
            g.shot_context='training';g._draw_stadium_stands()
            self.assertEqual(g.steward_positions,[]);self.assertEqual(g._steward_mesh_cache,[])

    def test_real_goal_reporting_celebrates_only_the_scoring_side_then_expires(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            self.teams(g);g.elapsed=10.;g._record_report_goal('away',12);g.elapsed+=.17
            self.assertEqual(cheering(g),'away');self.assertTrue(any(jump(g,'away',i)>0 for i in range(4)))
            self.assertTrue(all(jump(g,'home',i)==0 for i in range(4)))
            g._record_report_goal('home',14);g.elapsed+=.17
            self.assertEqual(cheering(g),'home');self.assertTrue(all(jump(g,'away',i)==0 for i in range(4)))
            g.elapsed+=2.36;self.assertIsNone(cheering(g))
            g._record_report_goal('away',16);g.shot_context='training';self.assertIsNone(cheering(g))

    def test_player_goal_away_is_not_mistaken_for_home_supporters_or_duplicated(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            self.teams(g);g._match_shot_goal_counted=False;g.match_player_goals=0;g.match_home_score=g.match_away_score=0
            g._record_player_match_goal();until=g._crowd_celebrate_until
            self.assertEqual(g._celebrating_side,'away');g.elapsed+=.1;g._record_player_match_goal()
            self.assertEqual((g.match_home_score,g.match_away_score),(0,1));self.assertEqual(until,g._crowd_celebrate_until)

    def test_coloured_club_button_opens_facts_and_back_in_regular_and_compact_hubs(self):
        old=Window.size;density=Metrics.density
        try:
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                player,_=self.teams(g)
                for size in ((1280,591),(640,360),(320,240)):
                    Window.size=size;g.size=size;g.view='hub';g.draw();settle();button=g._menu.body.club_button
                    self.assertEqual(button.text,'Vitória BA');self.assertAlmostEqual(button._face_color.rgba[0],1.)
                    self.assertAlmostEqual(button._club_stripe_color.rgba[0],0.)
                    button.dispatch('on_release');settle();self.assertEqual(g.view,'club')
                    texts=[w.text for w in g.walk() if isinstance(w,Label)]
                    self.assertIn('1899',texts);self.assertIn('Barradão',texts);self.assertIn('35,618',texts)
                    self.assertTrue(any('Campeonato Brasileiro Série B' in t for t in texts))
                    self.assertEqual(g.career.club.uid,player.uid)
                    g._on_key_down(None,27,0,'',[]);g.draw();settle();self.assertEqual(g.view,'hub')
        finally:Window.size=old;Metrics.density=density
    def test_ai_goals_report_home_and_away_without_crediting_the_player(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            self.teams(g);g.match_finished=g.awaiting_chance=g.match_halftime=False
            g.match_half=1;g.match_minute=0.;g.match_first_stoppage=0
            g.match_chance_minutes=[];g.match_chance_index=0
            g.match_goal_events=[(1,'home'),(4,'away')];g.match_goal_event_index=0
            g.match_home_score=g.match_away_score=g.match_player_goals=0
            with patch.object(g,'_play_ai_goal_sound'):
                g._update_career_match(1.);self.assertEqual(g._celebrating_side,'home')
                g._update_career_match(1.);self.assertEqual(g._celebrating_side,'away')
            self.assertEqual((g.match_home_score,g.match_away_score,g.match_player_goals),(1,1,0))
