import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from career import CareerMode
from coach import fresh_state, clean_state, conversation, conversation_text, style_for, STYLES


class CoachTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.env=patch.dict(os.environ,STRIKER_SAVE_DIR=self.t.name);self.env.start();self.addCleanup(self.env.stop)

    def signed(self):
        c=CareerMode(autoload=False);c.accept_starting_offer(c.offers[0]);return c

    def test_required_before_training_no_read_or_backdoor_unlock(self):
        c=self.signed();c.record_coach_performance(0,1,[],False,key_match=True);state=c.rng.getstate();before=(c.morale,c.stamina,c.training_session_week)
        self.assertFalse(c.coach_meeting_held);self.assertFalse(c.begin_training());self.assertFalse(c.record_training_shot(True));self.assertEqual(c.complete_training(3),0)
        first=c.coach_conversation();self.assertEqual(first,c.coach_conversation());self.assertFalse(c.coach_meeting_held)
        self.assertEqual((c.morale,c.stamina,c.training_session_week),before);self.assertEqual(c.rng.getstate(),state)
        self.assertTrue(c.attend_coach_meeting());self.assertTrue(c.begin_training())
        d=CareerMode();self.assertTrue(d.coach_meeting_held);self.assertEqual(d.coach_conversation(),first)
        data=d.save_path.read_bytes();self.assertTrue(d.attend_coach_meeting());self.assertEqual(d.save_path.read_bytes(),data)
        self.assertEqual(c.rng.getstate(),state)

    def test_week_season_and_transfer_require_a_new_meeting(self):
        c=self.signed();c.record_coach_performance(0,1,[],False,key_match=True);c.attend_coach_meeting();style=c.coach_conversation()['style']
        c.week+=1;self.assertFalse(c.coach_meeting_required);self.assertTrue(c.begin_training());c.record_coach_performance(0,1,[],False,key_match=True);c.attend_coach_meeting()
        self.assertEqual(c.coach_conversation()['style'],style)
        c.season+=1;self.assertFalse(c.coach_meeting_held);c.attend_coach_meeting()
        c.club_name=next(cl.name for cl in c.current_league.clubs if cl.uid!=c.club.uid)
        self.assertFalse(c.coach_meeting_held);self.assertEqual(c._current_coach_state()['games'],0)

    def test_drought_feedback_at_three_and_six_not_every_week(self):
        c=self.signed()
        for index in range(1,7):
            c.record_coach_performance(0,2,[],False);c.week+=1
            self.assertEqual(c.coach_conversation()['kind'],'drought' if index in (3,6) else 'routine')
            c.attend_coach_meeting()
        c.week+=1;self.assertEqual(c.coach_conversation()['kind'],'routine')
        c.record_coach_performance(1,0,[],True);self.assertEqual(c.coach_state['drought'],0)

    def test_big_match_feedback_uses_real_personal_performance_and_is_not_repeated(self):
        c=self.signed();event=dict(kind='final',minute=20,outcome='goal')
        c.record_coach_performance(0,3,[event],True)
        self.assertEqual(c.coach_conversation()['kind'],'key_match')
        c.record_coach_performance(2,0,[event],True);c.week+=1
        self.assertEqual(c.coach_conversation()['kind'],'decisive')
        c.record_coach_performance(0,1,[],False) # same week's second fixture cannot erase it
        self.assertEqual(c.coach_conversation()['kind'],'decisive')
        c.attend_coach_meeting();c.week+=1
        self.assertEqual(c.coach_conversation()['kind'],'routine')
        c.record_coach_performance(1,0,[dict(kind='equaliser',minute=89,outcome='goal')],True)
        self.assertEqual(c.coach_conversation()['kind'],'decisive')

    def test_strong_form_and_three_personalities_offer_different_responses(self):
        c=self.signed()
        for goals in (2,1,2):c.record_coach_performance(goals,0,[],True)
        self.assertFalse(c.coach_meeting_required)
        uids={style_for(str(i)):str(i) for i in range(50)};self.assertEqual(set(uids),{0,1,2})
        responses=set()
        for style,uid in uids.items():
            state=fresh_state(uid);state.update(games=1,latest_decisive=True)
            m=conversation(state,'2026:2:'+uid,uid);self.assertEqual(m['style'],style);responses.add(conversation_text(m))
        self.assertEqual(len(responses),3)
        self.assertNotEqual(conversation_text(dict(kind='drought',style=0,variant=0)),conversation_text(dict(kind='drought',style=0,variant=1)))

    def test_save_failure_rolls_back_and_retry_cannot_farm_attributes(self):
        c=self.signed();c.record_coach_performance(0,1,[],False,key_match=True);before=copy.deepcopy(c.coach_state);disk=c.save_path.read_bytes();stats=c.morale,c.stamina,c.rng.getstate()
        with patch('career.os.replace',side_effect=OSError('disk full')):self.assertFalse(c.attend_coach_meeting())
        self.assertEqual(c.coach_state,before);self.assertEqual(c.save_path.read_bytes(),disk);self.assertTrue(c.coach_meeting_required)
        self.assertTrue(c.attend_coach_meeting());self.assertTrue(c.attend_coach_meeting());self.assertEqual((c.morale,c.stamina,c.rng.getstate()),stats)

    def test_legacy_partial_training_keeps_progress_then_requires_next_meeting(self):
        c=self.signed();c.attend_coach_meeting();c.begin_training();c.record_training_shot(True)
        data=json.loads(c.save_path.read_text());data['career'].pop('coach_state');c.save_path.write_text(json.dumps(data))
        d=CareerMode();self.assertFalse(d.coach_meeting_held);self.assertEqual(d.training_shots_taken,1)
        d.attend_coach_meeting();self.assertTrue(d.begin_training());self.assertEqual(d.training_shots_taken,1)
        d.week+=1;self.assertFalse(d.coach_meeting_held)

    def test_malformed_state_is_bounded_and_does_not_discard_career(self):
        c=self.signed();c.goals=9;c.save()
        for bad in (None,[],{'version':1,'club':{}},dict(fresh_state(c.club.uid),games=True),dict(fresh_state(c.club.uid),recent=[0]*100)):
            self.assertEqual(clean_state(bad)['meeting'],None)
            data=json.loads(c.save_path.read_text());data['career']['coach_state']=bad;c.save_path.write_text(json.dumps(data))
            d=CareerMode();self.assertTrue(d.load());self.assertEqual(d.goals,9);self.assertFalse(d.coach_meeting_held)

    def test_actual_club_match_updates_drought_and_history_before_save(self):
        c=self.signed();h,a=c.next_fixture();c.finish_match(h,a,0,2,forced_score=(0,0))
        d=CareerMode();self.assertEqual(d.coach_state['games'],1);self.assertEqual(d.coach_state['drought'],1)

    def test_international_fixture_does_not_change_club_feedback(self):
        from types import SimpleNamespace
        access=SimpleNamespace(has_world_access=lambda:True)
        c=CareerMode(access,autoload=False,starter_country='Brazil',save_slot='world');c.accept_starting_offer(c.offers[0]);c.nationality='Argentina';c._ensure_competitions()
        c.record_coach_performance(0,2,[],False);before=copy.deepcopy(c.coach_state)
        f=dict(id='friendly:coach',home='nation:Brazil',away='nation:Argentina',week=0,stage='International friendly',score=None)
        c.world_competitions.friendlies[f['id']]=f;book=c.world_competitions
        c.finish_match(c._competition_club(book.nations[f['home']]),c._competition_club(book.nations[f['away']]),2,0,True,(1,2),'world|friendly|'+f['id'])
        self.assertEqual(c.coach_state,before)


    def test_no_meeting_in_ordinary_weeks_or_after_a_missed_late_chance(self):
        c=self.signed();self.assertFalse(c.coach_meeting_required);self.assertTrue(c.begin_training())
        c.week+=1;c.record_coach_performance(0,1,[dict(kind='lead',minute=88,outcome='missed')],True)
        self.assertFalse(c.coach_meeting_required)
        c.record_coach_performance(0,1,[],False,key_match=True)
        self.assertTrue(c.coach_meeting_required);self.assertEqual(c.coach_conversation()['kind'],'key_match')

    def test_another_key_game_same_week_requires_its_own_review(self):
        c=self.signed();c.record_coach_performance(0,1,[],False,key_match=True);c.attend_coach_meeting()
        self.assertFalse(c.coach_meeting_required)
        c.record_coach_performance(0,1,[],False,key_match=True)
        self.assertTrue(c.coach_meeting_required);c.attend_coach_meeting();self.assertFalse(c.coach_meeting_required)
