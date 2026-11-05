import unittest,tempfile,json,copy,math
from pathlib import Path
from unittest.mock import patch
from career import CareerMode,CareerClub
from player_development import clean,fresh,FOCI,needed
class PlayerDevelopment(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
  self.env=patch.dict('os.environ',STRIKER_SAVE_DIR=self.temp.name);self.env.start();self.addCleanup(self.env.stop)
  self.c=CareerMode(autoload=False);self.c.accept_starting_offer(self.c.offers[0])
 def train(self,focus='placed',on_focus=3):
  c=self.c;self.assertTrue(c.choose_training_focus(focus));self.assertTrue(c.begin_training())
  for i in range(3):self.assertTrue(c.record_training_shot(True,i<on_focus))
  c.complete_training(99)
 def test_only_selected_skill_earns_xp_once_from_persisted_three_shots(self):
  c=self.c;self.train('heading',2)
  self.assertEqual(c.development['skills']['heading'],dict(level=0,xp=20))
  self.assertTrue(all(c.skill_level(k)==0 for k in FOCI));self.assertEqual(c.coach_trust,52)
  before=copy.deepcopy(c.development);c.complete_training(999);self.assertEqual(c.development,before)
  self.assertFalse(c.choose_training_focus('low'));self.assertEqual(c.training_focus,'heading')
  c._consume_match_training();self.assertTrue(c.choose_training_focus('low'));self.assertEqual(c.training_focus,'low')
 def test_three_focused_sessions_gain_one_level_and_cap_is_bounded(self):
  c=self.c
  for _ in range(3):
   self.train('low',2);c._consume_match_training()
  self.assertEqual(c.development['skills']['low'],dict(level=1,xp=0));self.assertEqual(c.skill_level('placed'),0)
  c.development['skills']['low']=dict(level=9,xp=needed(9)-1)
  self.train('low',3);self.assertEqual(c.development['skills']['low'],dict(level=10,xp=0))
 def test_partial_session_and_focused_goals_survive_load_without_reroll(self):
  c=self.c;c.choose_training_focus('penalties');c.begin_training();c.record_training_shot(True,True)
  self.assertTrue(c.load());self.assertEqual(c.training_focus,'penalties');self.assertEqual(c.training_shots_taken,1)
  self.assertFalse(c.choose_training_focus('heading'))
  c.begin_training();c.record_training_shot(True,True);c.record_training_shot(False);c.complete_training(3)
  self.assertEqual(c.development['skills']['penalties']['xp'],20)
  self.assertTrue(c.load());c.complete_training(3);self.assertEqual(c.development['skills']['penalties']['xp'],20)
 def test_failed_reservation_shot_completion_and_focus_save_roll_back(self):
  c=self.c;before=copy.deepcopy(c.development)
  with patch.object(c,'save',return_value=False):
   self.assertFalse(c.choose_training_focus('heading'));self.assertEqual(c.development,before)
   self.assertFalse(c.begin_training());self.assertEqual(c.development,before)
  c.begin_training();before=copy.deepcopy(c.development)
  with patch.object(c,'save',return_value=False):self.assertFalse(c.record_training_shot(True,True))
  self.assertEqual(c.development,before);self.assertEqual(c.training_shots_taken,0)
  for _ in range(3):c.record_training_shot(True,True)
  before=copy.deepcopy(c.development)
  with patch.object(c,'save',return_value=False):self.assertEqual(c.complete_training(3),0.)
  self.assertEqual(c.development,before);self.assertFalse(c.trained_this_week)
  c.complete_training(3);self.assertEqual(c.development['skills']['placed']['xp'],24)
 def test_role_minutes_trust_recovery_and_morale_floors(self):
  c=self.c;c.development.update(trust=40,peak_trust=50)
  self.assertEqual(c.team_role,'Substitute');self.assertEqual(c.playing_window(),(60,90))
  c.last_training_week=c.week;c.morale=16
  opponent=CareerClub('Elite','Germany','Division 1',1,95)
  for _ in range(20):self.assertEqual(c.chance_count(opponent),3)
  c._consume_match_training()
  for _ in range(6):self.train(on_focus=0);c._consume_match_training()
  self.assertGreaterEqual(c.coach_trust,50);self.assertEqual(c.team_role,'Starter')
  self.assertEqual(c.playing_window(),(0,75));self.assertEqual(c.playing_window(key_match=True),(0,90))
  for _ in range(3):c.record_development_match(2,0,True)
  self.assertEqual(c.team_role,'Key player');self.assertEqual(c.playing_window(),(0,90))
  c.record_development_match(0,3);self.assertGreaterEqual(c.coach_trust,0)
 def test_match_hook_counts_actual_club_goals_and_national_does_not_change_trust(self):
  c=self.c;h,a=c.next_fixture();own=0 if h.uid==c.club.uid else 1
  score=[0,0];score[own]=2;c.finish_match(h,a,2,0,forced_score=tuple(score))
  self.assertEqual(c.development['season_goals'],2);self.assertEqual(c.development['career_goals'],2)
  self.assertEqual(c.coach_trust,62);self.assertEqual(c.development['last_minutes'],75)
  trust=c.coach_trust
  c.finish_match(CareerClub('Portugal','Portugal','National Team',1,89),CareerClub('Spain','Spain','National Team',1,90),1,0,True,(1,0))
  self.assertEqual(c.coach_trust,trust);self.assertEqual(c.development['season_goals'],2)
 def test_goals_are_sticky_and_season_archive_and_skills_survive_rollover(self):
  c=self.c;c.development['goal_target']=5;c.record_development_match(5,0,True)
  self.assertIn('goals',c.development['season_earned'])
  c.development.update(trust=70,peak_trust=70);c._recognise_development()
  c.current_league.scorer_goals[c.player_name]=5
  c.finish_development_season();c.finish_development_season();self.assertEqual(len(c.development['archive']),1)
  self.assertEqual(set(c.development['archive'][0]['earned']),{'goals','trust','top3'})
  c.development['skills']['low']=dict(level=2,xp=10);c.season+=1;c._ensure_development()
  self.assertEqual(c.development['season_goals'],0);self.assertEqual(c.development['career_goals'],5)
  self.assertEqual(c.skill_level('low'),2);self.assertEqual(c.development['season_earned'],[])
  self.assertEqual(clean(c.development,c.season),c.development)
 def test_transfer_resets_club_trust_but_preserves_skills_and_goals(self):
  c=self.c;c.development.update(trust=90,peak_trust=90);c.development['skills']['heading']=dict(level=3,xp=7)
  target=next(t for t in c.current_league.clubs if t.uid!=c.club.uid)
  c.agent_offers=[(target.name,c.league_key)];c.accept_transfer(target.name,c.league_key)
  self.assertEqual(c.coach_trust,50);self.assertEqual(c.skill_level('heading'),3)
  self.assertEqual(c.development['transfers'],1);self.assertTrue(c.load());self.assertEqual(c.development['transfers'],1)
 def test_legacy_and_damaged_extension_keep_career_and_known_progress(self):
  c=self.c;c.goals=7;c.matches=9;c.save();document=json.loads(c.save_path.read_text());document['career'].pop('development')
  c.save_path.write_text(json.dumps(document));self.assertTrue(c.load())
  self.assertEqual(c.development['career_goals'],7);self.assertEqual(c.coach_trust,50)
  for broken in (None,[],{'version':True},dict(fresh(),trust=math.nan),dict(fresh(),skills={}),dict(fresh(),session={'id':-1})):
   document['career']['development']=broken;c.save_path.write_text(json.dumps(document));self.assertTrue(c.load())
   self.assertEqual(c.goals,7);self.assertEqual(c.development['career_goals'],7)
 def test_mandatory_training_does_not_mask_drought_and_scoring_restores_role(self):
  c=self.c
  for _ in range(5):
   self.train();c.record_development_match(0,3);c._consume_match_training()
  self.assertEqual(c.coach_trust,40);self.assertEqual(c.team_role,'Substitute')
  self.train();c.record_development_match(1,0)
  self.assertEqual(c.coach_trust,48);self.assertEqual(c.team_role,'Starter')
 def test_failed_transfer_keeps_old_club_and_milestone(self):
  c=self.c;old=c.club.uid;target=next(t for t in c.current_league.clubs if t.uid!=old)
  c.agent_offers=[(target.name,c.league_key)]
  with patch.object(c,'save',return_value=False):c.accept_transfer(target.name,c.league_key)
  self.assertEqual(c.club.uid,old);self.assertEqual(c.development['transfers'],0)
  self.assertTrue(c.agent_offers)
 def test_legacy_current_season_goals_are_recognised_without_playing_again(self):
  c=self.c;c.goals=20;c.matches=30;c.save();document=json.loads(c.save_path.read_text())
  document['career'].pop('development');c.save_path.write_text(json.dumps(document));self.assertTrue(c.load())
  self.assertEqual(c.development['goal_target'],c._development_target())
  self.assertIn('goals',c.development['season_earned']);self.assertEqual(c.development['career_goals'],20)
  self.assertEqual(c.development['archive'],[])
 def test_skills_change_only_documented_controls_with_caps(self):
  c=self.c
  for key in FOCI:c.development['skills'][key]=dict(level=10,xp=0)
  self.assertEqual(c.finishing_controls('kick'),(0.,.88));self.assertEqual(c.finishing_controls('free_kick'),(0.,1.))
  self.assertEqual(c.finishing_controls('header'),(1.,.92));self.assertEqual(c.finishing_controls('penalty'),(.8,.92))
  self.assertEqual(c.low_finish_speed('kick',.3),1.06)
  self.assertEqual(c.low_finish_speed('kick',1.5),1.);self.assertEqual(c.low_finish_speed('header',.3),1.)
