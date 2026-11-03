import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from career import CareerMode
from domestic_playoffs import build_tournament,movements,reserve_movements,catalogue,profile
from world_competitions import Tournament,CompetitionBook
from international_calendar import match_date,window_dates,prepare_friendlies
from two_divisions import rotate_reserve
class Access:
    def has_world_access(self):return True
class PlayoffTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);env=patch.dict(os.environ,STRIKER_SAVE_DIR=t.name);env.start();self.addCleanup(env.stop)
        self.c=CareerMode(Access(),autoload=False,starter_country='France',save_slot='world');self.c.accept_starting_offer(self.c.offers[0])
    def cup(self,country='France',reserve=False):
        c=self.c;return build_tournament(country,c.leagues[country+'|1'],c.leagues[country+'|2'],41,48,reserve=reserve,queue=c.reserve_clubs(country))
    def play(self,cup,winner):
        for f in [f for f in cup.fixtures if f['id'] in cup.active]:
            # No aggregate tie, keeping the desired winner independent of ET.
            score=[4,0] if f['home']==winner else [0,4];cup.record(f,score)
        cup.advance(cup.last_week,tuple(cup.teams))
    def test_french_ladder_reloads_between_every_round_and_upper_club_can_survive(self):
        cup=self.cup();lower=self.c.leagues['France|2'].table();upper=self.c.leagues['France|1'].table();fourth=lower[3].uid
        self.assertEqual((cup.fixtures[0]['home'],cup.fixtures[0]['away']),(fourth,lower[4].uid));self.play(cup,fourth)
        cup=Tournament.from_dict(cup.to_dict());self.assertEqual(cup.fixtures[-1]['home'],lower[2].uid);self.play(cup,fourth)
        cup=Tournament.from_dict(cup.to_dict());final=[f for f in cup.fixtures if f['id'] in cup.active];self.assertEqual(len(final),2);self.assertEqual({final[0]['home'],final[0]['away']},{fourth,upper[-3].uid})
        self.play(cup,upper[-3].uid);self.assertEqual(cup.qualified,[upper[-3].uid]);self.c._ensure_competitions();self.c.world_competitions.tournaments[cup.key]=cup
        up,down=movements(self.c.leagues['France|1'],self.c.leagues['France|2'],self.c.world_competitions);self.assertEqual(len(up),2);self.assertEqual(len(down),2);self.assertNotIn(upper[-3],down)
    def test_brazil_has_two_independent_promotion_ties_and_no_final(self):
        cup=self.cup('Brazil');self.assertEqual(len(cup.plan),1);self.assertEqual(len(cup.fixtures),4);cup.finish();self.assertEqual(len(cup.qualified),2)
        self.c._ensure_competitions();self.c.world_competitions.tournaments[cup.key]=cup
        up,down=movements(self.c.leagues['Brazil|1'],self.c.leagues['Brazil|2'],self.c.world_competitions);self.assertEqual(len(up),4);self.assertEqual(len(down),4)
    def test_england_six_clubs_byes_two_leg_semis_one_final_and_draw_decision(self):
        cup=self.cup('England');self.assertEqual(len(cup.teams),6);self.assertEqual([len(r) for r in cup.plan],[2,2,1]);self.assertEqual([g['legs'] for r in cup.plan for g in r],[1,1,2,2,1]);cup.finish();self.assertEqual(len(cup.fixtures),7);self.assertEqual(len(cup.qualified),1)
    def test_reserve_survival_does_not_rotate_losing_challenger(self):
        c=self.c;cup=self.cup('France',True);lower=c.leagues['France|2'];survivor=lower.table()[-3];queue=c.reserve_clubs('France');self.play(cup,survivor.uid);c._ensure_competitions();c.world_competitions.tournaments[cup.key]=cup
        down,up=reserve_movements(lower,queue,c.world_competitions);self.assertEqual(len(down),2);self.assertEqual(up,queue[:2]);ids,_=rotate_reserve(lower,c.leagues['France|3'],c.relegation_pools['France'],down,up);self.assertEqual(ids[:8],[x.uid for x in queue[2:]]);self.assertIn(survivor,lower.clubs)
    def test_every_profile_bracket_completes_roundtrips_and_preserves_identities(self):
        c=self.c;c._ensure_competitions();c._prepare_world_run_in();c.world_competitions.complete()
        for key,cup in c.world_competitions.tournaments.items():
            if key.startswith('playoff:'):self.assertEqual(Tournament.from_dict(cup.to_dict()).to_dict(),cup.to_dict(),key)
        ids={x.uid for l in c.leagues.values() for x in l.clubs};sizes={k:len(l.clubs) for k,l in c.leagues.items()};c._finish_season();self.assertEqual({x.uid for l in c.leagues.values() for x in l.clubs},ids);self.assertEqual({k:len(l.clubs) for k,l in c.leagues.items()},sizes);self.assertTrue(c.save());self.assertTrue(c.load())
    def test_third_place_hero_must_play_portugal_tie_before_rollover(self):
        c=self.c;league=c.leagues['Portugal|2'];eligible=[x for x in league.clubs if x.uid not in catalogue()['ineligible_for_first_division']];hero=eligible[2]
        c.league_key=league.key;c.club_name=hero.name
        for i,club in enumerate(eligible):club.points=100000-i*1000
        league.round_index=league.total_rounds;c.week=45
        f=c.next_match()
        for _ in range(24):
            if f[0].startswith('world|playoff:Portugal:2|'):break
            score=(4,0) if f[1].uid==c.club.uid else (0,4);c.finish_match(f[1],f[2],0,0,competition=f[0],forced_score=score);f=c.next_match()
        self.assertEqual(c.season,2026);self.assertTrue(f[0].startswith('world|playoff:Portugal:2|'));uid=c.club.uid;c.save();self.assertTrue(c.load());self.assertEqual(c.next_match()[0],f[0]);self.assertEqual(c.club.uid,uid)
    def test_b_clubs_cannot_take_first_division_places(self):
        from domestic_playoffs import direct_up
        l=self.c.leagues['Portugal|2'];blocked=next(c for c in l.clubs if c.uid in catalogue()['ineligible_for_first_division']);blocked.points=100000;self.assertNotIn(blocked,direct_up(l));self.assertNotIn(blocked.uid,self.cup('Portugal').teams)
    def test_corrupt_playoff_references_and_winner_cannot_be_loaded(self):
        cup=self.cup();data=cup.to_dict()
        for change in [lambda d:d['plan'][0][0].update(home='win:missing'),lambda d:d.update(results={'unknown':'unknown'})]:
            bad=copy.deepcopy(data);change(bad)
            with self.assertRaises(ValueError):Tournament.from_dict(bad)
    def test_italy_excludes_teams_beyond_points_threshold_and_final_venue_follows_seed(self):
        c=self.c;l=c.leagues['Italy|2'];ranked=l.table()
        for i,club in enumerate(ranked):club.points=100-i
        for i,club in enumerate(ranked[6:]):club.points=ranked[2].points-15-i
        cup=self.cup('Italy');self.assertEqual(len(cup.teams),4);self.assertEqual(len(cup.plan),2)
        # Force the worst semifinal seed through; the best surviving seed still
        # hosts the second leg of the final, regardless of the bracket branch.
        for f in [f for f in cup.fixtures if f['id'] in cup.active]:
            winner=max((f['home'],f['away']),key=lambda uid:cup.ranks[uid]);cup.record(f,[4,0] if f['home']==winner else [0,4])
        cup.advance(cup.last_week,tuple(cup.teams));final=[f for f in cup.fixtures if f['id'] in cup.active]
        better=min((final[0]['home'],final[0]['away']),key=lambda uid:cup.ranks[uid]);self.assertEqual(final[1]['home'],better)
    def test_german_upper_division_hosts_first_leg(self):
        cup=self.cup('Germany');self.assertEqual(cup.teams[cup.fixtures[0]['home']]['tier'],1);self.assertEqual(cup.teams[cup.fixtures[1]['home']]['tier'],2)
    def test_neutral_final_has_no_home_advantage(self):
        c=self.c;cup=self.cup('England');cup.finish();final=[f for f in cup.fixtures if f.get('neutral')];self.assertEqual(len(final),1)
        f=final[0];c._ensure_competitions();c.world_competitions.tournaments[cup.key]=cup;home=c._competition_club(cup.teams[f['home']]);away=c._competition_club(cup.teams[f['away']]);home.rating=away.rating=75
        a,b=c.world_fixture_goal_means('world|'+cup.key+'|'+f['id'],home,away);self.assertAlmostEqual(a,b)
class CallupTests(PlayoffTests):
    # Standalone test helper methods, not inheritance of the playoff suite.
    def test_top_three_any_first_division_and_ties_without_morale_or_recent_form_gates(self):
        c=self.c;c.league_key='Brazil|1';c.club_name=c.current_league.clubs[0].name;c.nationality='Portugal';c.morale=0;c.matches=1;c.form_goals=[]
        for goals,expected in [(0,False),(5,False),(6,True),(7,True)]:
            c.current_league.scorer_goals={'A':10,'B':8,'C':6,c.player_name:goals};self.assertEqual(c.national_team_eligible,expected)
        c.club.tier=2;self.assertFalse(c.national_team_eligible)
    def test_foreign_first_division_player_gets_dated_national_matches_and_caps_only(self):
        c=self.c;c.league_key='Brazil|1';c.club_name=c.current_league.clubs[0].name;c.nationality='Portugal';c.current_league.scorer_goals={c.player_name:8,'Other':9};c.week=0;c._ensure_competitions();c.week=15
        # Other club cups can occur before the same window's national fixture.
        for cup in c.world_competitions.tournaments.values():
            if not cup.national:cup.advance(15)
        before=c.matches,c.goals;fixture=c.next_match();self.assertTrue(fixture[0].startswith('world|'));self.assertIn('nation:Portugal',(fixture[1].uid,fixture[2].uid));self.assertTrue(c.called_up)
        actor='nation:Portugal';score=(1,0) if fixture[1].uid==actor else (0,1);c.finish_match(fixture[1],fixture[2],1,0,competition=fixture[0],forced_score=score)
        self.assertEqual((c.matches,c.goals),before);self.assertEqual((c.international_caps,c.international_goals),(1,1));history=c.fixture_history[-1];self.assertIn(history['date'],[d.isoformat() for d in window_dates(c.season)])
        decisions=dict(c.world_competitions.callups);c.current_league.scorer_goals[c.player_name]=0;c.save();self.assertTrue(c.load());self.assertEqual(c.world_competitions.callups,decisions);self.assertTrue(c.next_match()[0].startswith('world|'))
    def test_calendar_shows_nation_before_eligibility_and_no_duplicate_country_dates(self):
        c=self.c;c._ensure_competitions();entries=c.calendar_entries();self.assertTrue(any('nation:'+c.nationality in (e.get('home_uid'),e.get('away_uid')) for e in entries))
        for year in (2025,2026,2027,2028):
            book=CompetitionBook(year,17,c.leagues);book.complete();seen=set()
            for cup in book.tournaments.values():
                if not cup.national:continue
                for f in cup.fixtures:
                    self.assertIn('date',f)
                    for uid in (f['home'],f['away']):self.assertNotIn((uid,f['date']),seen);seen.add((uid,f['date']))
            self.assertEqual(CompetitionBook.from_dict(book.to_dict()).to_dict(),book.to_dict())
# Avoid running the inherited playoff methods twice.
for name in list(PlayoffTests.__dict__):
    if name.startswith('test_') and name not in CallupTests.__dict__:setattr(CallupTests,name,None)

class CalendarSourceTests(unittest.TestCase):
    def test_published_march_and_june_dates_do_not_use_fixed_month_projection(self):
        from international_calendar import window_dates,finals_dates,window_key
        from datetime import date
        self.assertIn(date(2026,3,24),window_dates(2025));self.assertNotIn(date(2026,3,17),window_dates(2025))
        self.assertIn(date(2028,5,30),window_dates(2027));self.assertEqual(finals_dates(2026,'asian')[0],date(2027,1,7))
        self.assertNotEqual(window_key(2026,date(2027,1,10)),window_key(2026,date(2027,6,10)))
    def test_future_friday_national_match_does_not_preempt_thursday_club_match(self):
        from world_competitions import Tournament
        from datetime import date
        teams=[dict(uid='a',name='A',country='A',rating=70),dict(uid='b',name='B',country='B',rating=70)]
        cup=Tournament('n','National',teams,1,kind='knockout',national=True);f=cup.fixtures[0];f['week']=10;f['date']='2026-09-25'
        self.assertIsNone(cup.advance(10,('a',),until='2026-09-24'));self.assertIsNone(f['score']);self.assertIs(cup.advance(11,('a',),until='2026-10-01'),f)

class NationalMembershipTests(unittest.TestCase):
    def test_nations_league_membership_survives_a_year_without_the_tournament(self):
        with tempfile.TemporaryDirectory() as directory,patch.dict(os.environ,STRIKER_SAVE_DIR=directory):
            c=CareerMode(Access(),autoload=False);c.accept_starting_offer(c.offers[0]);book=CompetitionBook(2026,31,c.leagues);book.complete();entries=book.entrants_for_next_season(c.leagues)
            old={k:v for k,v in entries.items() if k.startswith('nations_')};self.assertEqual(len(old),4)
            off_year=CompetitionBook(2027,31,c.leagues,entries);self.assertNotIn('nations_a',off_year.tournaments);off_year.complete();restored=CompetitionBook.from_dict(off_year.to_dict())
            following=restored.entrants_for_next_season(c.leagues)
            self.assertEqual({k:v for k,v in following.items() if k.startswith('nations_')},old)
            next_cycle=CompetitionBook(2028,31,c.leagues,following)
            self.assertEqual(set(next_cycle.tournaments['nations_a'].teams),{t['uid'] for t in old['nations_a']})
