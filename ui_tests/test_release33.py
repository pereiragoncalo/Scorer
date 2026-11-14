import random,unittest
from unittest.mock import patch
from kivy.core.window import Window
from test_menus import isolated_game,settle
from club_profiles import profile
from stadium_portraits import portrait

class StadiumRevision(unittest.TestCase):
 def test_city_only_on_open_grounds_and_roofs_have_no_support_poles(self):
  with isolated_game()as g:
   before=vars(g.ball).copy();rng=random.getstate()
   for capacity in (5000,10000,10001,150000):
    with patch('stadium_scene.stadium_capacity',return_value=capacity),patch('stadium_architecture.Rectangle')as rectangles:
     g._draw_stadium_stands()
     self.assertEqual(bool(rectangles.call_count),capacity<=10000)
     batches=g._stadium_architecture[1]
     self.assertNotIn((.27,.34,.38,1),[x[1]for x in batches])
     if capacity>10000:self.assertIn('stadium_roof_fascia.png',[x[0]for x in batches])
   self.assertEqual(vars(g.ball),before);self.assertEqual(random.getstate(),rng)
 def test_all_six_portraits_use_distinct_regions_and_bounded_palette_cache(self):
  with isolated_game()as g:
   regions=[]
   for capacity in (3000,8000,18000,35000,60000,100000):
    texture=portrait(g,capacity,((.2,.3,.8,1),(1,1,1,1)))
    self.assertEqual(texture.size,(512,512));self.assertEqual(texture.mag_filter,'nearest');regions.append(texture.tex_coords)
   self.assertEqual(len(set(regions)),6)
   for value in (.1,.2,.3,.4):portrait(g,3000,((value,.5,.1,1),(1,1,1,1)))
   self.assertLessEqual(len(g._stadium_portrait_textures.entries),2)
 def test_coimbra_facts_readable_at_phone_and_desktop_sizes(self):
  old=Window.size
  try:
   with patch('edition.WORLD_BUILD',True),isolated_game()as g:
    c=g.career;club=next(x for l in c.leagues.values()for x in l.clubs if x.uid=='6d0a94b6d9d584ce77e0')
    c.league_key=next(k for k,l in c.leagues.items()if club in l.clubs);c.club_name=club.name;original=profile(club)
    for size in ((640,295),(1280,720)):
     Window.size=size;g.size=size;g.view='club';g.draw();settle();screen=g._menu.body
     self.assertEqual(screen.facts,original)
     self.assertEqual(len(screen.fact_values),6)
     for value in screen.fact_values.values():self.assertTrue(value.text.strip());self.assertGreater(value.width,100)
     self.assertIn('1887',[v.text for v in screen.fact_values.values()]);self.assertIn('29,622',[v.text for v in screen.fact_values.values()])
     self.assertFalse(screen.scroll.do_scroll_x)
  finally:Window.size=old
