import copy,json,os,tempfile,unittest
from types import SimpleNamespace as NS
from unittest.mock import patch
from attendance import turnout,occupied_seats,fixture_snapshot
from title_events import pending,to_coach,finish,view,clean
from career import CareerMode
import honours

class AttendanceTests(unittest.TestCase):
    def test_collective_results_affect_both_sides_and_snapshot_is_fixed(self):
        good=NS(uid='a',country='England',tier=1,played=10,points=30)
        bad=NS(uid='b',country='England',tier=1,played=10,points=0)
        middle=[NS(uid=str(i),country='England',tier=1,played=10,points=15) for i in range(5)]
        league=NS(table=lambda:sorted([good,bad,*middle],key=lambda x:-x.points))
        self.assertGreater(turnout(good,league),turnout(bad,league))
        g=NS(career=NS(leagues={'England|1':league},world_competitions=None),match_opportunity_seed=('fixture',1))
        ratios=fixture_snapshot(g,good,bad);self.assertGreater(ratios['home'],ratios['away'])
        good.points=0;bad.points=30;self.assertEqual(fixture_snapshot(g,good,bad),ratios)
        g.match_opportunity_seed=('fixture',2);self.assertLess(fixture_snapshot(g,good,bad)['home'],fixture_snapshot(g,good,bad)['away'])
    def test_each_sector_fills_highest_rows_first_with_scattered_partial_row(self):
        seats=[(x,y,z,i,team,0) for team in ('home','away') for z in range(6) for i,(x,y) in enumerate(((0,-5),(1,-5),(37,-6),(38,-6),(38,2),(38,3)))]
        for fraction in (.1,.4,.9,1.):
            chosen=occupied_seats(seats,dict(home=fraction,away=fraction/2),lambda x,y,z,c:(c*13+int(z)*7)%19)
            for team in ('home','away'):
                for section in ('goal','corner','side'):
                    def same(s):return s[4]==team and ('corner' if s[0]>36.2 and s[1]<-4 else 'side' if s[0]>36.2 else 'goal')==section
                    yes=[s for s in chosen if same(s)];no=[s for s in seats if same(s) and s not in chosen]
                    if yes and no:self.assertGreaterEqual(min(s[2] for s in yes),max(s[2] for s in no))

class TitleEventsTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);p=patch.dict(os.environ,STRIKER_SAVE_DIR=self.tmp.name);p.start();self.addCleanup(p.stop)
        self.c=CareerMode(autoload=False);self.c.accept_starting_offer(self.c.offers[0]);self.c.attend_coach_meeting()
    def award(self,key='cup'):
        c=self.c;row=dict(season=c.season,competition=key,title='Collective cup',team_uid=c.club.uid,team=c.club.name,country=c.club.country)
        honours.award(c,row);return row
    def test_only_new_collective_titles_queue_and_reload_does_not_reaward(self):
        c=self.c;row=self.award();self.award();self.award('scorer:England|4');self.award('playoff:test')
        self.assertEqual(len(c.title_events['queue']),1);self.assertEqual(view(c),'trophy');c.save()
        d=CareerMode();self.assertEqual(d.title_events,c.title_events);self.assertEqual(d.honours,c.honours)
        self.assertTrue(to_coach(d));self.assertEqual(view(d),'title_coach');self.assertTrue(finish(d));self.assertIsNone(pending(d))
        self.assertTrue(d.load());honours.award(d,row);self.assertIsNone(pending(d))
    def test_failed_stage_and_speech_save_keep_event_and_training_focus(self):
        c=self.c;self.award();before=copy.deepcopy(c.title_events)
        with patch.object(c,'save',return_value=False):self.assertFalse(to_coach(c))
        self.assertEqual(c.title_events,before);to_coach(c);before=copy.deepcopy(c.title_events);stats=c.training_focus,c.coach_trust,c.morale,c.rng.getstate()
        with patch.object(c,'save',return_value=False):self.assertFalse(finish(c))
        self.assertEqual(c.title_events,before);self.assertTrue(finish(c));self.assertEqual((c.training_focus,c.coach_trust,c.morale,c.rng.getstate()),stats)
    def test_title_talk_merges_due_weekly_choice_once(self):
        c=self.c;self.award();to_coach(c);c.week+=1
        self.assertFalse(finish(c));focus=c.coach_focus_options()[1];self.assertTrue(finish(c,focus));self.assertTrue(c.coach_meeting_held);self.assertEqual(c.training_focus,focus)
    def test_title_coach_feedback_is_collective_and_individual(self):
        c=self.c;self.award();to_coach(c)
        self.assertIn(c.coach_team_feedback(),__import__('coach').TITLE_TEAM_FEEDBACK)
        self.assertIn(c.coach_individual_feedback(),__import__('coach').TITLE_INDIVIDUAL_FEEDBACK)
    def test_old_saves_do_not_replay_past_trophies_and_bad_events_are_optional(self):
        c=self.c;self.award();doc=c.title_events
        self.assertEqual(clean(None,c.honours)['queue'],[])
        bad=copy.deepcopy(doc);bad['queue'][0]['team_uid']='unknown';self.assertEqual(clean(bad,c.honours)['queue'],[])
        bad=copy.deepcopy(doc);bad['queue'][0]['scene']['turnout']['home']=float('nan');self.assertEqual(clean(bad,c.honours)['queue'],[])
    def test_actual_world_final_queues_trophy_with_final_teams(self):
        from world_competitions import Tournament
        from edition import entitlement_provider
        with patch('edition.WORLD_BUILD',True):
            c=CareerMode(entitlement_provider(),autoload=False,save_slot='world');c.accept_starting_offer(c.offers[0]);c._ensure_competitions()
            other=next(t for t in c.current_league.clubs if t.uid!=c.club.uid)
            teams=[{k:getattr(t,k) for k in ('uid','name','country','tier','rating')} for t in (c.club,other)]
            cup=Tournament('qa:final','QA cup',teams,'qa',kind='knockout',start_week=c.week);c.world_competitions.tournaments[cup.key]=cup
            f=cup.fixtures[0];f['week']=c.week;h=c._competition_club(cup.teams[f['home']]);a=c._competition_club(cup.teams[f['away']]);score=(1,0) if h.uid==c.club.uid else (0,1)
            c.finish_match(h,a,0,0,competition='world|'+cup.key+'|'+f['id'],forced_score=score)
            e=pending(c);self.assertIsNotNone(e);self.assertEqual(e['competition'],cup.key);self.assertEqual(e['scene']['home']['uid'],h.uid);self.assertEqual(e['scene']['away']['uid'],a.uid)
            self.assertTrue(c.load());self.assertEqual(pending(c),e)
