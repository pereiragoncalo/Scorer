import math,random,unittest
from unittest.mock import patch
from kivy.core.window import Window
from test_menus import isolated_game,settle
from club_profiles import profile,stadium_variant,stadium_capacity

class StadiumArchitecture(unittest.TestCase):
 def test_roof_boundary_low_wall_training_and_static_cache_do_not_change_physics_or_rng(self):
  with isolated_game()as g:
   g.shot_context='training';before=vars(g.ball).copy();rng=random.getstate()
   for capacity in (5000,10000,10001,40000,80000,150000):
    with patch('stadium_scene.stadium_capacity',return_value=capacity),patch.object(g,'_draw_crowd_meshes')as crowd:
     g._draw_stadium_stands();crowd.assert_not_called()
     self.assertEqual(g.stadium_capacity,capacity);self.assertEqual(g.stadium_has_roof,capacity>10000)
     self.assertEqual(g.stadium_wall_height,.55)
     batches=g._stadium_architecture[1];assets={row[0]for row in batches}
     self.assertIn('stadium_wall.png',assets);self.assertEqual('stadium_roof.png'in assets,capacity>10000)
     for _,_,vertices,indices in batches:self.assertTrue(all(math.isfinite(x)for x in vertices));self.assertLess(len(indices),24000)
     if capacity>10000:
      roof=next(v for asset,_,v,_ in batches if asset=='stadium_roof.png')
      self.assertLess(min(roof[1::4]),g.height-60) # roof reaches the visible scene below HUD
      self.assertGreater(max(roof[1::4]),0)
     allocation=g._scene_textures.allocations;geometry=g._stadium_architecture
     for _ in range(5):g._draw_stadium_stands()
     self.assertIs(geometry,g._stadium_architecture);self.assertEqual(g._scene_textures.allocations,allocation)
   self.assertEqual(vars(g.ball),before);self.assertEqual(random.getstate(),rng)
 def test_home_venue_when_away_and_own_ground_when_training(self):
  with patch('edition.WORLD_BUILD',True),isolated_game()as g:
   c=g.career;clubs=[x for league in c.leagues.values()for x in league.clubs]
   own=next(x for x in clubs if 0<(profile(x)['capacity']or 0)<=10000)
   home=next(x for x in clubs if (profile(x)['capacity']or 0)>40000)
   c.league_key=next(k for k,l in c.leagues.items()if own in l.clubs);c.club_name=own.name
   g.shot_context='match';g.match_home=home;g.match_away=own;g._draw_stadium_stands();self.assertTrue(g.stadium_has_roof)
   g.shot_context='training';g._draw_stadium_stands();self.assertFalse(g.stadium_has_roof)
   self.assertEqual(g.stadium_capacity,stadium_capacity(own))
 def test_club_portrait_and_facts_fit_phone_and_desktop_without_changing_profile(self):
  old=Window.size
  try:
   with patch('edition.WORLD_BUILD',True),isolated_game()as g:
    c=g.career;club=next(x for l in c.leagues.values()for x in l.clubs if (profile(x)['capacity']or 0)>80000)
    c.league_key=next(k for k,l in c.leagues.items()if club in l.clubs);c.club_name=club.name;facts=profile(club)
    for size in ((640,295),(1280,720)):
     Window.size=size;g.size=size;g.view='club';g.draw();settle()
     screen=g._menu.body;self.assertEqual(screen.stadium_variant,stadium_variant(stadium_capacity(club)))
     self.assertEqual(screen.facts,facts);self.assertEqual(screen.stadium_picture.texture.mag_filter,'nearest')
     if screen.overview.orientation=='horizontal':self.assertGreaterEqual(screen.stadium_picture.x,screen.facts_box.right)
     else:self.assertLessEqual(screen.stadium_picture.top,screen.facts_box.y)
     self.assertLessEqual(screen.stadium_picture.right,screen.card.right)
     self.assertFalse(screen.scroll.do_scroll_x)
  finally:Window.size=old
