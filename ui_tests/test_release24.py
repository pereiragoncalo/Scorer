import math,unittest
from unittest.mock import patch
from test_menus import isolated_game
from defensive_pressure import advance,player_position
from retro_sprites import field_pose
from celebrations import GoalCelebration,advance as celebrate,has_ball
from ball_retrieval import Retrieval

class NearestPressure(unittest.TestCase):
 def test_nearest_opponent_closes_player_and_others_keep_shape(self):
  with isolated_game() as g:
   g.draw=lambda:None;g.shot_context='match';g._start_opportunity('long_shot',17)
   p=g._pressure;self.assertIsNotNone(p)
   target=player_position(g)
   self.assertLessEqual(math.dist(p.position,target),min(math.dist(g._field_player_position(a),target)for a in g.field_players if a.team=='defender')+1e-9)
   g.state=g.STATE_AIMING;g.buildup_progress=1.
   others=[a for a in g.field_players if a is not p.actor];before=[g._field_player_position(a)for a in others]
   distance=math.dist(p.position,player_position(g));advance(g,.2)
   self.assertLess(math.dist(p.position,player_position(g)),distance);self.assertEqual(field_pose(g,p.actor).state,'RUN')
   self.assertEqual(before,[g._field_player_position(a)for a in others])
   g.outcome_registered=True;point=p.position;advance(g,.2);self.assertEqual(p.position,point)
 def test_penalty_and_free_kick_wall_stay_legal(self):
  with isolated_game() as g:
   g.draw=lambda:None;g._start_opportunity('penalty',4);self.assertIsNone(g._pressure)
   g._start_opportunity('free_kick',4);point=g._pressure.position;advance(g,.5);self.assertEqual(point,g._pressure.position)

class RetrievalIntegration(unittest.TestCase):
 def test_goal_ball_is_not_hidden_at_a_fixed_timer_before_pickup(self):
  with isolated_game() as g:
   g.view='shot';g.shot_context='match';g.elapsed=3.
   r=Retrieval((0.,10.),(0.,-.25));g.goal_celebration=GoalCelebration(0,'home',False,(0.,10.),(0.,0.),(0.,0.),2.,(0.,0.),True,(0.,-.25),r)
   with patch('net_presentation.ball_position',return_value=(2.,-2.,.115)):
    celebrate(g,.1)
   self.assertEqual(r.target,(2.,-2.));self.assertFalse(has_ball(g))

class GoalEntrySweep(unittest.TestCase):
 def test_fast_oblique_goal_starts_at_crossing_before_side_collision(self):
  with isolated_game() as g:
   g.draw=lambda:None;g.shot_context='training';g.ball.reset(3.2,.02,1.5)
   g.ball.vx,g.ball.vy,g.ball.vz=40.,-15.,0.;g.ball.active=True
   with patch.object(g,'_collide_goalkeeper',return_value=False),patch.object(g,'_collide_field_players'):
    g._update_ball(1/60)
   self.assertEqual(g.goals,1);self.assertIn('right',g._net_replay.first_contacts)
   self.assertLessEqual(g._net_replay.ball[0],g.goal_half_width+.2)
