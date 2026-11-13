import random,unittest
from unittest.mock import patch
from test_menus import isolated_game
from retro_sprites import field_pose
from celebrations import GoalCelebration,motion
from finishing_balance import penalty_dive_target

class Release21Gameplay(unittest.TestCase):
 def test_penalty_direction_distribution_is_sixty_percent_opposite(self):
  rng=random.Random(91);wrong=0
  for i in range(10000):
   x=2.4 if i%2 else -2.4
   wrong+=penalty_dive_target(rng,x,3.66)*x<0
  self.assertTrue(5800<wrong<6200,wrong)
 def test_keeper_starts_centred_and_commits_opposite_without_changing_mind(self):
  with isolated_game() as g:
   g.draw=lambda:None;g.shot_context='training';g.goalkeeper_x=2.;g._start_opportunity('penalty',42)
   self.assertEqual(g.goalkeeper_x,0.);g._update_goalkeeper_idle(.1);self.assertEqual(g.goalkeeper_x,0.)
   with patch('finishing_balance.penalty_dive_target',return_value=-2.5):g.shoot(2.5,.8)
   self.assertEqual(g.penalty_dive_target,-2.5)
   for _ in range(180):
    g._update_goalkeeper_shot(1/120)
    if g.goalkeeper_is_diving:break
    g.ball.x+=g.ball.vx/120;g.ball.y+=g.ball.vy/120;g.ball.z+=g.ball.vz/120
   self.assertTrue(g.goalkeeper_is_diving);self.assertLess(g.goalkeeper_dive_sign,0)
   chosen=g.goalkeeper_target_x;g.ball.x=-2.5;g._update_goalkeeper_shot(.1)
   self.assertEqual(g.goalkeeper_target_x,chosen)
 def test_stationary_blocker_is_idle_but_chasing_players_run(self):
  with isolated_game() as g:
   g.draw=lambda:None;g._start_opportunity('rebound',1);g.state_age=3.
   self.assertEqual(field_pose(g,g.buildup_blocker).state,'IDLE')
   g._start_opportunity('through_ball',2)
   self.assertEqual(field_pose(g,g.onside_defender).state,'RUN')
 def test_retrieval_faces_midfield_and_waiting_team_mates_do_not_run(self):
  c=GoalCelebration(0,'home',False,(0,10),(3,-2),(4,-5),2,(3,-2),True,(0,-.25))
  position=c.actor(4)[0];target,moving=motion(c,4)
  self.assertTrue(moving);self.assertGreater(target[1],position[1])
  waiting=GoalCelebration(0,'home',False,(0,10),(3,-2),(4,-5),2,(3,-2))
  self.assertEqual(waiting.actor(.1,3)[1],'IDLE')
 def test_long_result_names_and_review_content_fit_small_landscape(self):
  from kivy.core.window import Window
  from kivy.metrics import Metrics
  from test_menus import settle
  old_size=Window.size;old_density=Metrics.density
  try:
   Metrics.density=1.;Window.size=(640,295)
   with isolated_game() as g:
    c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();c._finish_season()
    c.season_review['worst']=dict(home='Coimbra Preto',away='Oliveira de Azeméis Vermelha',score='0-2',date='2027-07-23',competition='Portugal Division 2')
    c.season_review['public_records']=[dict(division=2,season=c.season-1,player=c.player_name,goals=40)]
    c.post_match_stage='';c.title_events['queue']=[];c.life['private_meeting']='';g.view='hub';g._career_started=True;g.draw();settle()
    for label in g._menu.body.items:
     self.assertLessEqual(label._natural_height,label.height+1,label.text)
     self.assertGreaterEqual(label.y,g._menu.body.y)
  finally:Metrics.density=old_density;Window.size=old_size
