import copy,unittest
from unittest.mock import patch
from test_menus import isolated_game
from test_club_stadium import ClubStadium
from stadium_scene import context,animate_crowd

class StadiumSeats(unittest.TestCase):
 def test_home_colour_and_all_chairs_survive_empty_training(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   player,home=ClubStadium().teams(g);g._draw_stadium_stands()
   self.assertEqual(g.stadium_seat_colour,tuple(context(g)['home_kit'][0][:3])+(1.,))
   self.assertEqual(g.stadium_seat_count,g.crowd_available)
   self.assertGreater(g.stadium_seat_count,g.crowd_total)
   g.shot_context='training';g._draw_stadium_stands()
   self.assertGreater(g.stadium_seat_count,0)
   self.assertEqual(g.crowd_total,0);self.assertEqual(g.steward_visible,0)
   self.assertTrue(g._stand_mesh_cache)
   self.assertEqual(g.stadium_seat_colour,tuple(g.career.kit_for_club(player)[0][:3])+(1.,))
   for _,vertices,indices in g._stand_mesh_cache:
    self.assertLess(max(indices),65536)
 def test_scoring_fans_rise_then_return_to_seats_chairs_stay_fixed(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   ClubStadium().teams(g);g._draw_stadium_stands();chairs=copy.deepcopy(g._stand_mesh_cache)
   before=[tuple(v[s+j*4+1] for j in range(len(base))) for _,_,v,s,base,*_ in g._crowd_motions]
   g._record_report_goal('away',30);g.elapsed+=.9;animate_crowd(g)
   changed=[]
   for i,(team,_,v,s,base,*_) in enumerate(g._crowd_motions):
    now=tuple(v[s+j*4+1] for j in range(len(base)))
    if team=='home':self.assertEqual(now,before[i])
    else:changed.append(now!=before[i])
   self.assertTrue(any(changed));self.assertEqual(chairs,g._stand_mesh_cache)
   g.elapsed+=4;animate_crowd(g)
   for i,(_,_,v,s,base,*_) in enumerate(g._crowd_motions):
    self.assertEqual(tuple(v[s+j*4+1] for j in range(len(base))),before[i])
