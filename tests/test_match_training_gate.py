"""Three persisted practice shots are required again after each appearance."""
import json,os,tempfile,unittest
from unittest.mock import patch
from career import CareerMode
from world_competitions import Tournament

class Access:
    def has_world_access(self):return True

class MatchTrainingGate(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        env=patch.dict(os.environ,STRIKER_SAVE_DIR=self.temp.name);env.start();self.addCleanup(env.stop)
    def signed(self,world=False):
        c=CareerMode(Access() if world else None,autoload=False,save_slot='world' if world else 'legacy')
        c.accept_starting_offer(c.offers[0]);return c
    def train(self,c):
        self.assertTrue(c.begin_training())
        for outcome in (True,False,False):self.assertTrue(c.record_training_shot(outcome))
        self.assertGreater(c.complete_training(3),0)
    def test_abandoned_sessions_cannot_unlock_play_or_award_rewards(self):
        c=self.signed();before=c.stamina,c.morale
        self.assertEqual(c.complete_training(3),0);self.assertFalse(c.trained_this_week)
        c.begin_training()
        for taken in range(3):
            self.assertEqual(c.training_shots_taken,taken)
            self.assertEqual(c.complete_training(3),0)
            self.assertEqual((c.stamina,c.morale),before);self.assertFalse(c.trained_this_week)
            self.assertTrue(c.record_training_shot(taken==0))
        self.assertAlmostEqual(c.complete_training(3),1.5) # one persisted goal, not caller's three
        self.assertTrue(c.trained_this_week)
        self.assertEqual(c.complete_training(3),0)
    def test_world_club_fixture_consumes_training_without_advancing_week(self):
        c=self.signed(True);self.train(c);c._ensure_competitions()
        h,a=c.next_fixture();key='training:test'
        rows=[dict(uid=x.uid,name=x.name,country=x.country,rating=x.rating,tier=x.tier) for x in (h,a)]
        cup=Tournament(key,'Training gate fixture',rows,'gate',kind='knockout',start_week=c.week)
        c.world_competitions.tournaments[key]=cup;f=cup.fixtures[0];f['week']=c.week
        home=c._competition_club(cup.teams[f['home']]);away=c._competition_club(cup.teams[f['away']]);week=c.week
        c.finish_match(home,away,0,1,competition='world|'+key+'|'+f['id'],forced_score=(1,0))
        self.assertEqual(c.week,week);self.assertFalse(c.trained_this_week)
        d=CareerMode(Access(),save_slot='world');self.assertFalse(d.trained_this_week)
        self.assertEqual(d.training_shots_taken,0);self.assertTrue(d.begin_training())
    def test_world_national_fixture_consumes_training_and_cannot_recomplete_old_shots(self):
        c=self.signed(True);self.train(c);c._ensure_competitions();book=c.world_competitions
        own='nation:'+c.nationality;other=next(x for x in book.nations if x!=own)
        f=dict(id='friendly:training',home=own,away=other,week=c.week,stage='International friendly',score=None)
        book.friendlies[f['id']]=f;week=c.week
        c.finish_match(c._competition_club(book.nations[own]),c._competition_club(book.nations[other]),0,1,
                       competition='world|friendly|'+f['id'],forced_score=(0,0))
        self.assertEqual(c.week,week);self.assertFalse(c.trained_this_week)
        self.assertEqual(c.complete_training(3),0);self.assertTrue(c.begin_training())
        self.assertEqual(c.training_shots_taken,0)
    def test_old_completion_resets_once_but_partial_progress_survives_upgrade(self):
        c=self.signed();self.train(c);data=json.loads(c.save_path.read_text())
        data['career'].pop('training_gate_version');c.save_path.write_text(json.dumps(data))
        d=CareerMode();self.assertFalse(d.trained_this_week);self.assertTrue(d.begin_training())
        d.record_training_shot(True);data=json.loads(d.save_path.read_text());data['career'].pop('training_gate_version')
        d.save_path.write_text(json.dumps(data));e=CareerMode()
        self.assertEqual(e.training_shots_taken,1);self.assertEqual(e.training_session_goals,1)
        self.assertFalse(e.trained_this_week)
