import copy,json,os,tempfile,unittest
from unittest.mock import patch
from career import CareerMode
from season_review import capture,finalize,clean,dismiss

class ReviewTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.env=patch.dict(os.environ,STRIKER_SAVE_DIR=self.temp.name);self.env.start()
  self.c=CareerMode();self.c.accept_starting_offer(self.c.offers[0]);self.c.attend_coach_meeting()
 def tearDown(self):self.env.stop();self.temp.cleanup()
 def prepare(self):
  c=self.c;name=c.club.name
  c.fixture_history=[dict(date='2026-08-01',competition=c.current_league.name,home=name,away='Rival',status='5-1',played=True),dict(date='2026-08-08',competition=c.current_league.name,home='Rival',away=name,status='4-0',played=True),dict(date='2025-08-08',competition='Old',home=name,away='Other',status='99-0',played=True),dict(date='2026-08-10',competition='National',home='Portugal',away='France',status='9-0',played=True,club_match=False)]
  c.current_league.scorer_goals={f'Rival {i}':20-i for i in range(8)};c.current_league.scorer_goals[c.player_name]=4
  c.matches=12;c.goals=4
 def test_frozen_results_rank_portrait_and_current_targets_survive_reset_and_load(self):
  self.prepare();c=self.c;appearance=copy.deepcopy(c.coach_appearance);capture(c);before=copy.deepcopy(c.season_review)
  self.assertEqual(before['best']['score'],'5-1');self.assertEqual(before['worst']['score'],'4-0');self.assertEqual(before['player_rank'],9)
  self.assertEqual(before['portrait'],appearance['portrait']);self.assertEqual(len(before['leaders']),5)
  c.season+=1;c.current_league.scorer_goals.clear();c.goals=0;c.matches=0;finalize(c)
  self.assertEqual(c.season_review['player_rank'],9);self.assertEqual(c.season_review['next_goal_target'],c._ensure_development()['goal_target'])
  self.assertTrue(c.save());loaded=CareerMode();self.assertEqual(loaded.season_review,c.season_review)
  self.assertTrue(dismiss(loaded));self.assertFalse(CareerMode().season_review['pending'])
 def test_actual_free_season_transition_captures_before_table_and_scorers_clear(self):
  self.prepare();c=self.c;old=c.season;c._finish_season()
  self.assertEqual(c.season,old+1);self.assertEqual(c.season_review['season'],old);self.assertTrue(c.season_review['pending'])
  self.assertEqual(c.season_review['goals'],4);self.assertIsNotNone(c.season_review['next_goal_target'])
 def test_failed_dismiss_save_remains_pending_and_invalid_optional_data_is_discarded(self):
  self.prepare();capture(self.c)
  with patch.object(self.c,'save',return_value=False):self.assertFalse(dismiss(self.c))
  self.assertTrue(self.c.season_review['pending']);bad=copy.deepcopy(self.c.season_review);bad['portrait']='../secret'
  self.assertIsNone(clean(bad));self.assertIsNone(clean(None))
 def test_capture_does_not_change_rng_or_gameplay_counters(self):
  self.prepare();c=self.c;rng=c.rng.getstate();before=(c.matches,c.goals,c.morale,c.stamina,c.coach_trust)
  capture(c)
  self.assertEqual(c.rng.getstate(),rng);self.assertEqual((c.matches,c.goals,c.morale,c.stamina,c.coach_trust),before)
  self.assertTrue(c.season_review['pending'])
