import unittest,copy
from unittest.mock import patch
from test_menus import isolated_game,settle
from celebrations import active
from stadium_scene import animate_crowd

class GoalCelebrations(unittest.TestCase):
 def test_automatic_resume_keeps_match_clock_and_goal_count_until_cutscene_finishes(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   self.prepare(g);g._register_goal();g.state=g.STATE_RESULT;g.ball.active=False
   c=g.goal_celebration;minute=g.match_minute;attempts=g.attempts
   with patch.object(g,'draw'):
    for _ in range(150):
     if g.view!='shot':break
     g.update(.1)
   self.assertEqual(g.view,'match');self.assertEqual(g.match_minute,minute)
   self.assertEqual(g.match_player_goals,1);self.assertEqual(g.attempts,attempts)
   self.assertIsNone(g.goal_celebration)
 def prepare(self,g):
  from test_club_stadium import ClubStadium
  ClubStadium().teams(g);g.view='shot';g._prepare_next_shot();g.shot_context='match'
  g.match_half=2;g.match_minute=87;g.match_home_score=0;g.match_away_score=0;g.match_stakes={}
  g._match_shot_goal_counted=False;g.outcome_registered=False;g.state=g.STATE_SHOT
 def test_goal_starts_once_pauses_auto_result_then_normal_tap_can_advance(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   self.prepare(g)
   renderer=g._retro_renderer()
   with patch.object(renderer,'draw',wraps=renderer.draw) as render:
    g.draw()
   origin=next(call.args[4][:2] for call in render.call_args_list if call.args[1]=='hero')
   g._register_goal();g.state=g.STATE_RESULT
   c=g.goal_celebration;self.assertIsNotNone(c);self.assertTrue(c.decisive);self.assertEqual(c.side,'away')
   self.assertEqual(c.origin,origin)
   self.assertEqual((g.match_home_score,g.match_away_score,g.match_player_goals),(0,1,1))
   g._register_goal();g._record_player_match_goal();self.assertIs(g.goal_celebration,c)
   g.ball.active=False;g.state_age=3.;g.elapsed=c.started+1.;g.update(.02)
   self.assertEqual(g.view,'shot');self.assertTrue(active(g))
   physical=copy.deepcopy(vars(g.ball));actors=[vars(p).copy() for p in g.field_players]
   for age in (0.,c.run_seconds+.5,c.duration-1.):
    g.elapsed=c.started+age;g.draw();self.assertEqual(vars(g.ball),physical)
    self.assertEqual([vars(p) for p in g.field_players],actors)
   g._advance_after_shot();self.assertIsNone(g.goal_celebration);self.assertEqual(g.view,'match')
   self.assertEqual(g.match_player_goals,1)
 def test_unique_fans_move_only_for_scoring_side_heads_follow_bodies_and_guards_stay(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   self.prepare(g);g._draw_stadium_stands();g._record_report_goal('away',15)
   guards=copy.deepcopy(g._steward_mesh_cache);g.elapsed+=.4;animate_crowd(g)
   away=[]
   for index,(team,seed,bv,bs,by,hv,hs,hy) in enumerate(g._crowd_motions):
    offset=g._crowd_motion_offsets[index]
    if team=='home':self.assertEqual(offset,0.)
    else:away.append(offset)
    self.assertAlmostEqual(bv[bs+1]-by[0],hv[hs+1]-hy[0])
   self.assertGreater(len(set(round(h,3) for h in away)),20)
   self.assertTrue(any(h==0 for h in away));self.assertTrue(any(h>0 for h in away))
   self.assertEqual(g._steward_mesh_cache,guards)
   g.elapsed+=3;animate_crowd(g);self.assertTrue(all(h==0 for h in g._crowd_motion_offsets))
 def test_normal_goal_celebrates_at_home_supporters_without_slide_or_training_cutscene(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   self.prepare(g);g.match_home,g.match_away=g.match_away,g.match_home;g.match_minute=20
   g._register_goal();c=g.goal_celebration
   self.assertEqual(c.side,'home');self.assertFalse(c.decisive);self.assertLess(c.target[0],0)
   g._prepare_next_shot();g.shot_context='training';g.outcome_registered=False;g._register_goal()
   self.assertIsNone(g.goal_celebration)
