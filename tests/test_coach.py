import copy,json,os,tempfile,unittest
from unittest.mock import patch
from career import CareerMode
from coach import clean_state,fresh_state,style_for,TEAM_FEEDBACK,INDIVIDUAL_ROUTINE
from player_development import FOCI

class CoachTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        env=patch.dict(os.environ,STRIKER_SAVE_DIR=self.tmp.name);env.start();self.addCleanup(env.stop)
    def signed(self):
        c=CareerMode(autoload=False);c.accept_starting_offer(c.offers[0]);return c
    def test_weekly_gate_explicit_focus_persistence_and_idempotency(self):
        c=self.signed();self.assertTrue(c.coach_meeting_required);self.assertFalse(c.begin_training())
        rng=c.rng.getstate();stats=c.morale,c.stamina,c.coach_trust
        first=c.coach_conversation();self.assertEqual(first,c.coach_conversation())
        self.assertEqual(len(first['options']),2);self.assertEqual(len(set(first['options'])),2)
        self.assertFalse(c.attend_coach_meeting('invalid'));self.assertTrue(c.attend_coach_meeting(first['options'][1]));self.assertTrue(c.coach_meeting_held)
        self.assertEqual(c.training_focus,first['options'][1]);self.assertEqual((c.morale,c.stamina,c.coach_trust),stats)
        disk=c.save_path.read_bytes();self.assertTrue(c.attend_coach_meeting());self.assertEqual(c.save_path.read_bytes(),disk)
        self.assertFalse(c.choose_training_focus(first['options'][0]));self.assertEqual(c.rng.getstate(),rng)
        d=CareerMode();self.assertTrue(d.coach_meeting_held);self.assertEqual(d.training_focus,c.training_focus);self.assertTrue(d.begin_training())
    def test_week_season_and_transfer_require_new_talk_even_without_matches(self):
        c=self.signed();c.attend_coach_meeting();c.week+=1
        self.assertTrue(c.coach_meeting_required);self.assertFalse(c.begin_training());c.attend_coach_meeting();c.season+=1
        self.assertTrue(c.coach_meeting_required);c.attend_coach_meeting()
        c.club_name=next(x.name for x in c.current_league.clubs if x.uid!=c.club.uid)
        self.assertTrue(c.coach_meeting_required);self.assertEqual(c._current_coach_state()['games'],0)
    def test_extra_matches_do_not_repeat_talk_or_change_weekly_focus(self):
        c=self.signed();c.attend_coach_meeting();focus=c.training_focus
        for _ in range(2):
            c.record_coach_performance(0,2,[],False,key_match=True);c._consume_match_training()
            self.assertFalse(c.coach_meeting_required);self.assertEqual(c.training_focus,focus);self.assertTrue(c.begin_training())
        c.week+=1;self.assertTrue(c.coach_meeting_required);self.assertEqual(c.coach_conversation()['kind'],'key_match')
    def test_drought_feedback_every_week_and_two_finishing_choices(self):
        c=self.signed()
        for index in range(1,6):
            c.attend_coach_meeting();c.record_coach_performance(0,2,[],False);c.week+=1
            self.assertTrue(c.coach_meeting_required)
            if index>=3:
                self.assertEqual(c.coach_conversation()['kind'],'drought');self.assertEqual(set(c.coach_focus_options()),{'low','placed'})
        c.record_coach_performance(1,0,[],True);self.assertEqual(c.coach_state['drought'],0)
    def test_collective_feedback_uses_actual_team_result_and_personality(self):
        c=self.signed();style=style_for(c.club.uid)
        from coach_feedback import TEAM,STYLE,INDIVIDUAL
        self.assertIn(c.coach_team_feedback().split('\n')[0],TEAM['new']);self.assertIn(c.coach_individual_feedback().split('\n')[0],INDIVIDUAL['routine'])
        for score,outcome in [('2-0','win'),('0-2','loss'),('1-1','draw'),('1-1 (pen. 5-4)','win')]:
            c.coach_state=fresh_state(c.club.uid);c.record_coach_performance(1,0,[],True)
            c.fixture_history=[dict(home=c.club.name,away='Other club',home_uid=c.club.uid,status=score)]
            self.assertIn(c.coach_team_feedback().split('\n')[0],TEAM[outcome]);self.assertIn(c.coach_team_feedback().split('\n')[-1],STYLE[style])
        self.assertEqual(len(set(TEAM_FEEDBACK['loss'])),3)
    def test_big_game_and_strong_form_produce_individual_feedback(self):
        c=self.signed();c.record_coach_performance(2,0,[dict(kind='final',minute=20,outcome='goal')],True)
        self.assertEqual(c.coach_conversation()['kind'],'decisive');self.assertNotEqual(c.coach_individual_feedback(),INDIVIDUAL_ROUTINE[style_for(c.club.uid)])
        c.attend_coach_meeting();c.week+=1
        for g in (1,2,2):c.record_coach_performance(g,0,[],True)
        self.assertEqual(c.coach_conversation()['kind'],'form')
    def test_failed_save_rolls_back_focus_meeting_and_post_match_queue(self):
        c=self.signed();c.post_match_stage='coach';state=copy.deepcopy(c.coach_state);development=copy.deepcopy(c.development);disk=c.save_path.read_bytes();focus=c.coach_focus_options()[1]
        with patch('career.os.replace',side_effect=OSError('disk full')):self.assertFalse(c.attend_coach_meeting(focus))
        self.assertEqual(c.coach_state,state);self.assertEqual(c.development,development);self.assertEqual(c.post_match_stage,'coach');self.assertEqual(c.save_path.read_bytes(),disk)
        self.assertTrue(c.attend_coach_meeting(focus));self.assertEqual(c.post_match_stage,'');self.assertEqual(c.training_focus,focus)
    def test_legacy_partial_training_keeps_original_drill_and_xp(self):
        c=self.signed();c.attend_coach_meeting();old=c.training_focus;c.begin_training();c.record_training_shot(True,True)
        doc=json.loads(c.save_path.read_text());doc['career']['coach_state']['meeting'].pop('focus');doc['career']['coach_state']['meeting'].pop('options');c.save_path.write_text(json.dumps(doc))
        d=CareerMode();self.assertTrue(d.coach_meeting_required);self.assertEqual(d.training_shots_taken,1)
        chosen=d.coach_focus_options()[0];d.attend_coach_meeting(chosen);self.assertEqual(d.training_focus,old);self.assertEqual(d.training_shots_taken,1)
        d.record_training_shot(True,True);d.record_training_shot(False);d.complete_training(99)
        self.assertEqual(d.development['skills'][old]['xp'],20);d._consume_match_training();self.assertEqual(d.training_focus,chosen)
    def test_new_week_applies_new_focus_instead_of_stale_session(self):
        c=self.signed();c.attend_coach_meeting();c.begin_training();c.record_training_shot(True,True)
        old=c.training_focus;c.week+=1
        with patch.object(c,'coach_focus_options',return_value=('heading','penalties')):
            c.attend_coach_meeting('heading' if old!='heading' else 'penalties')
        new=c.development['focus'];self.assertNotEqual(old,new);self.assertEqual(c.training_focus,new)
        self.assertTrue(c.begin_training());self.assertEqual(c.training_shots_taken,0);self.assertEqual(c.development['session']['focus'],new)

    def test_corrupt_optional_coach_data_is_bounded(self):
        c=self.signed();c.goals=9;c.save()
        bads=[None,[],{'version':1,'club':{}},dict(fresh_state(c.club.uid),games=True)]
        m=dict(key=c.coach_key,kind='routine',style=0,variant=0,focus='low',options=[{},{}]);bads.append(dict(fresh_state(c.club.uid),meeting=m))
        for bad in bads:
            clean_state(bad);doc=json.loads(c.save_path.read_text());doc['career']['coach_state']=bad;c.save_path.write_text(json.dumps(doc))
            d=CareerMode();self.assertTrue(d.load());self.assertEqual(d.goals,9);self.assertTrue(d.coach_meeting_required)
    def test_international_fixture_does_not_change_club_feedback(self):
        from types import SimpleNamespace
        c=CareerMode(SimpleNamespace(has_world_access=lambda:True),autoload=False,save_slot='world');c.accept_starting_offer(c.offers[0]);c.nationality='Argentina';c._ensure_competitions();c.attend_coach_meeting()
        before=copy.deepcopy(c.coach_state);book=c.world_competitions
        f=dict(id='friendly:coach',home='nation:Brazil',away='nation:Argentina',week=0,stage='International friendly',score=None);book.friendlies[f['id']]=f
        c.finish_match(c._competition_club(book.nations[f['home']]),c._competition_club(book.nations[f['away']]),2,0,True,(1,2),'world|friendly|'+f['id'])
        self.assertEqual(c.coach_state,before)
