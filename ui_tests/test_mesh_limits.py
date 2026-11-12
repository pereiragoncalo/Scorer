import unittest
from unittest.mock import patch
from test_menus import isolated_game

class MeshLimits(unittest.TestCase):
 def test_large_ground_training_and_fully_occupied_match_fit_kivy_limits(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True
   for mode in ('training','match'):
    g.shot_context=mode;g.match_home=c.club;g.match_away=next(x for x in c.current_league.clubs if x.uid!=c.club.uid)
    g._stand_mesh_cache_key=None;g._crowd_mesh_cache_key=None
    with patch('stadium_scene.stadium_capacity',return_value=150000),patch('stadium_scene.fixture_snapshot',return_value={'home':1.,'away':1.}):
     g._draw_stadium_stands()
    self.assertGreater(g.stadium_seat_count,10000)
    batches=[(v,i) for _,v,i in g._stand_mesh_cache]+[(row[1],row[2]) for row in g._crowd_mesh_cache]
    for v,i in batches:
     self.assertLessEqual(len(i),24000)
     self.assertLess(max(i),65536);self.assertLess(max(i),len(v)//4)
    if mode=='training':self.assertEqual(g.crowd_total,0)
    else:self.assertGreater(g.crowd_total,0)
