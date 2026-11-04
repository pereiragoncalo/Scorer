import copy,json,os,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch
from career import CareerMode
from localization import Localizer
from newspaper import fresh_state,clean_state,make_report,article,current_report,PHOTOS


class NewspaperTests(unittest.TestCase):
    def report(self,state=None,goals=0,misses=1,score=(1,1),moments=(),away=False):
        h,a=NS(uid='h',name='Home'),NS(uid='a',name='Away')
        return make_report(state or fresh_state(),dict(date='2026-11-04',competition='League',country='England',status=f'{score[0]}-{score[1]}'),h,a,'a' if away else 'h',score,goals,misses,moments)

    def render(self,r):
        return article(r,Localizer(False).tr,lambda e,side:e[side],'PLAYER UNIQUE','League')

    def test_scoreless_ordinary_appearance_never_mentions_player(self):
        for goals,score in ((0,(0,1)),(0,(3,1)),(0,(1,1))):
            r=self.report(goals=goals,score=score)['report'];a=self.render(r)
            self.assertFalse(a['mentions_player']);self.assertNotIn('PLAYER UNIQUE',' '.join(a['paragraphs']))

    def test_standout_brace_lone_winner_or_actual_late_equaliser_mentions_player(self):
        for kwargs in (dict(goals=2,score=(2,1)),dict(goals=1,score=(1,0)),dict(goals=1,score=(1,1),moments=[dict(kind='equaliser',minute=89,outcome='goal')]),dict(goals=2,score=(0,2),away=True)):
            a=self.render(self.report(**kwargs)['report']);self.assertTrue(a['mentions_player']);self.assertIn('PLAYER UNIQUE',' '.join(a['paragraphs']))
        lost=self.report(goals=1,score=(1,2),moments=[dict(kind='lead',minute=85,outcome='goal')])['report']
        self.assertTrue(self.render(lost)['mentions_player'])

    def test_negative_mentions_start_at_three_actual_failed_appearances(self):
        state=fresh_state()
        for count in range(1,6):
            state=self.report(state=state,score=(0,1))
            a=self.render(state['report']);self.assertEqual(a['mentions_player'],count>=3)
            self.assertEqual(state['negative_run'],count)
        state=self.report(state=state,goals=1,score=(3,0));self.assertEqual(state['negative_run'],0)
        for _ in range(2):state=self.report(state=state,score=(0,1))
        state=self.report(state=state,goals=0,misses=0);self.assertEqual(state['negative_run'],0)

    def test_five_photos_rotate_only_on_new_report_without_rng_or_read_changes(self):
        state=fresh_state();photos=[]
        for _ in range(7):
            state=self.report(state=state);before=copy.deepcopy(state);photos.append(self.render(state['report'])['photo'])
            self.render(state['report']);self.assertEqual(state,before)
        self.assertEqual(photos,list(PHOTOS)+list(PHOTOS[:2]))
        for photo in PHOTOS:self.assertTrue(Path(photo).is_file())

    def test_headline_scores_and_names_follow_actual_home_away_result(self):
        for score,winner in (((2,0),'Home'),((0,2),'Away'),((0,0),'Home'),((2,2),'Home')):
            a=self.render(self.report(score=score)['report']);self.assertIn(winner,a['headline'])
            self.assertIn(f'{score[0]}-{score[1]}',a['paragraphs'][0])
        self.assertIn('goalless',self.render(self.report(score=(0,0))['report'])['headline'])

    def test_legacy_history_can_report_score_without_invented_personal_performance(self):
        c=NS(press_state=fresh_state(),fixture_history=[dict(date='2026-10-10',home='Home',away='Away',competition='Cup',status='2-1 (aet)',played=True)])
        r=current_report(c);self.assertEqual(r['score'],[2,1]);self.assertFalse(self.render(r)['mentions_player'])
        c.fixture_history=[];self.assertIsNone(current_report(c))

    def test_corrupted_optional_report_is_bounded(self):
        state=self.report();self.assertEqual(clean_state(state),state)
        for patcher in (lambda r:r.update(photo=5),lambda r:r.update(standout=1),lambda r:r.update(score=[True,0]),lambda r:r.update(home='x'*257)):
            bad=copy.deepcopy(state);patcher(bad['report']);self.assertIsNone(clean_state(bad)['report'])
        self.assertEqual(clean_state([]),fresh_state())

    def test_real_match_and_report_reload_preserve_score_stats_and_photo(self):
        with tempfile.TemporaryDirectory() as d,patch.dict(os.environ,STRIKER_SAVE_DIR=d):
            c=CareerMode(autoload=False);c.accept_starting_offer(c.offers[0]);h,a=c.next_fixture();own=0 if h.uid==c.club.uid else 1
            score=[0,0];score[own]=2;c.finish_match(h,a,2,0,forced_score=tuple(score))
            report=copy.deepcopy(c.press_state);loaded=CareerMode();self.assertEqual(loaded.press_state,report)
            self.assertEqual(loaded.goals,2);self.assertTrue(report['report']['standout'])
            data=json.loads(c.save_path.read_text());data['career'].pop('press_state');c.save_path.write_text(json.dumps(data));self.assertTrue(loaded.load())
            self.assertIsNotNone(current_report(loaded));self.assertFalse(current_report(loaded)['standout'])

    def test_recorded_goal_chronology_must_match_final_score(self):
        from newspaper import clean_events
        events=[dict(minute=46,half=1,side='away'),dict(minute=89,half=2,side='home')]
        self.assertEqual(clean_events(events,[1,1]),events)
        self.assertEqual(clean_events(events,[2,1]),[])
        r=self.report()['report'];r['events']=events;a=self.render(r)
        text=' '.join(a['paragraphs']);self.assertIn("45+1'",text);self.assertIn('Away opened the scoring',text);self.assertIn("89'",text);self.assertIn('Home equalised',text)
        self.assertNotIn('PLAYER UNIQUE',text)

    def test_unobserved_extra_time_goals_are_not_invented_in_chronology(self):
        from newspaper import clean_events
        events=[dict(minute=88,half=2,side='home')]
        self.assertEqual(clean_events(events,[2,0]),[])
        self.assertEqual(clean_events([dict(minute=999,half=2,side='home')],[1,0]),[])


    def test_every_goal_is_reported_with_its_correct_changing_score(self):
        from newspaper import goal_ledger
        r=self.report(score=(3,1))['report']
        r['events']=[dict(minute=m,half=1 if m<46 else 2,side=s) for m,s in ((32,'home'),(51,'away'),(67,'home'),(90,'home'))]
        a=self.render(r);self.assertEqual(len(a['goals']),4)
        self.assertEqual([g['score'] for g in a['goals']],[[1,0],[1,1],[2,1],[3,1]])
        for minute in ('32','51','67','90'):self.assertTrue(any(g['minute']==minute for g in a['goals']))
        self.assertIn('regained the lead',a['goals'][2]['text']);self.assertIn('extended the lead',a['goals'][3]['text'])

    def test_summary_recognises_comeback_and_late_equaliser(self):
        r=self.report(score=(1,2))['report'];r['events']=[dict(minute=m,half=2,side=s) for m,s in ((50,'home'),(60,'away'),(89,'away'))]
        self.assertIn('recovered from a deficit',self.render(r)['summary'])
        r['score']=[1,1];r['events']=r['events'][:2];r['events'][-1]['minute']=89
        self.assertIn('late equaliser',self.render(r)['summary'])

    def test_missing_historic_minutes_use_totals_without_fabricated_events(self):
        a=self.render(self.report(score=(3,1))['report'])
        self.assertEqual(len(a['goals']),2);self.assertTrue(all(g['minute'] is None for g in a['goals']))
        self.assertIn('3 goals',' '.join(g['text'] for g in a['goals']))

    def test_every_recorded_goal_gets_headline_and_body_even_after_defeat_or_reload(self):
        from newspaper import brief_article
        for away in (False,True):
            for score in ((1,1),(1,3),(3,1)):
                r=self.report(goals=1,score=score,away=away)['report']
                r['standout']=False # previous releases omitted ordinary goals
                restored=clean_state(dict(fresh_state(),report=r))['report']
                a=self.render(restored)
                self.assertTrue(a['mentions_player']);self.assertIn('PLAYER UNIQUE',a['headline'])
                self.assertIn('PLAYER UNIQUE',a['mention'])
                self.assertNotIn('crucial',a['mention'])
                self.assertIn('PLAYER UNIQUE',brief_article(restored,Localizer(False).tr,'PLAYER UNIQUE'))
