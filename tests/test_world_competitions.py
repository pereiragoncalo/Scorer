import copy,json,os,tempfile,unittest
from unittest.mock import patch
from collections import Counter
from career import CareerMode,CareerClub
from world_competitions import Tournament,CompetitionBook,round_robin
from season_transitions import promotion_format,exchange_pyramid
class Access:
    def has_world_access(self):return True

def teams(n):return [dict(uid=str(i),name='Club '+str(i),country='England',rating=70,tier=1) for i in range(n)]

class TournamentTests(unittest.TestCase):
    def test_odd_and_two_leg_schedules_no_duplicate_or_self_opponents(self):
        for n in (7,12,36):
            schedule=round_robin([str(i) for i in range(n)],2);pairs=[p for r in schedule for p in r]
            self.assertEqual(len(pairs),n*(n-1));self.assertEqual(len(set(pairs)),len(pairs));self.assertTrue(all(a!=b for a,b in pairs))
    def test_swiss_each_team_plays_eight_four_home_four_away_and_full_bracket(self):
        cup=Tournament('ucl','Test',teams(36),'seed',kind='swiss',rounds=8)
        home=Counter(f['home'] for f in cup.fixtures);away=Counter(f['away'] for f in cup.fixtures)
        self.assertEqual(set(home.values()),{4});self.assertEqual(set(away.values()),{4})
        cup.finish();self.assertEqual(len(cup.fixtures),189);self.assertTrue(all(f['score'] is not None for f in cup.fixtures));self.assertTrue(cup.champion)
        restored=Tournament.from_dict(cup.to_dict());self.assertEqual(restored.to_dict(),cup.to_dict())
    def test_non_power_of_two_field_and_byes_finishes_without_losing_teams(self):
        for n in (6,27,72,110):
            cup=Tournament('cup','Test',teams(n),'seed',kind='knockout',knockout_legs=1);cup.finish()
            self.assertEqual(len(cup.fixtures),n-1);self.assertTrue(all(f['winner'] in cup.teams for f in cup.fixtures))
    def test_two_leg_tie_uses_aggregate_and_pens_only_after_second_leg(self):
        cup=Tournament('cup','Test',teams(4),'seed',kind='knockout',knockout_legs=2)
        first=[f for f in cup.fixtures if f['tie']=='1:0'];cup.record(first[0],[2,0]);cup.record(first[1],[2,0])
        self.assertIsNone(first[0]['penalties']);cup.advance(200)
        self.assertIsNotNone(first[1]['penalties']);self.assertEqual(first[0]['winner'],first[1]['winner'])
    def test_qualified_nations_have_actual_results_and_world_cup_has_bronze(self):
        with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,STRIKER_SAVE_DIR=t):
            c=CareerMode(Access(),autoload=False);book=CompetitionBook(2025,17,c.leagues)
            self.assertNotIn('world_cup',book.tournaments);book.complete();cup=book.tournaments['world_cup']
            self.assertEqual(len(cup.teams),48);self.assertEqual(len(cup.fixtures),104)
            for path in book.qualification_paths:
                for key in path['qualifiers']:
                    q=book.tournaments[key];self.assertTrue(all(f['score'] is not None for f in q.fixtures));self.assertTrue(set(q.qualified)<=set(cup.teams))
            CompetitionBook.from_dict(book.to_dict())
    def test_corrupt_fixture_and_false_champion_rejected(self):
        cup=Tournament('cup','Test',teams(4),'seed');data=cup.to_dict()
        for mutate in (lambda d:d.update(champion='unknown'),lambda d:d['fixtures'][0].update(home='unknown'),lambda d:d['fixtures'][0].update(score=[True,0]),lambda d:d['active'].append('missing')):
            bad=copy.deepcopy(data);mutate(bad)
            with self.assertRaises((ValueError,TypeError)):Tournament.from_dict(bad)

class CareerCompetitionTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup);self.env=patch.dict(os.environ,STRIKER_SAVE_DIR=self.t.name);self.env.start();self.addCleanup(self.env.stop)
    def career(self,country='Portugal'):
        c=CareerMode(Access(),autoload=False,starter_country=country,save_slot='world');c.accept_starting_offer(c.offers[0]);return c
    def test_mid_tournament_save_export_reload_and_no_replayed_fixture(self):
        from career_transfer import export_career,validated_import
        c=self.career();c.week=20;c._ensure_competitions();pending=c.next_match();kind,h,a=pending
        if kind.startswith('world|'):
            uid=kind;c.finish_match(h,a,0,0,forced_score=(1,0),competition=kind);self.assertNotEqual(c.next_match()[0],uid)
            with self.assertRaises(ValueError):c.finish_match(h,a,0,0,forced_score=(1,0),competition=uid)
        c.save();d=CareerMode(Access(),save_slot='world');self.assertEqual(d.world_competitions.to_dict(),c.world_competitions.to_dict())
        restored=validated_import(c,export_career(c));self.assertEqual(restored.world_competitions.to_dict(),c.world_competitions.to_dict())
    def test_old_save_bootstrap_preserves_personal_goals_caps_and_aliases(self):
        c=self.career();c.matches=8;c.goals=5;c.international_caps=2;c.international_goals=1;c.week=12;c.save()
        data=json.loads(c.save_path.read_text());data['career'].pop('world_competitions');c.save_path.write_text(json.dumps(data));d=CareerMode(Access(),save_slot='world');d.next_match()
        self.assertEqual((d.matches,d.goals,d.international_caps,d.international_goals),(8,5,2,1))
    def test_nationality_away_goals_only_update_national_counters(self):
        c=self.career('Brazil');c.league_key='Brazil|1';c.club_name=c.current_league.clubs[0].name;c.matches=10;c.form_goals=[1]*8;c.morale=19;c.nationality='Argentina';c._ensure_competitions()
        book=c.world_competitions;other='nation:Brazil';actor='nation:Argentina';f={'id':'friendly:manual','home':other,'away':actor,'week':0,'stage':'International friendly','score':None};book.friendlies[f['id']]=f
        before=c.matches,c.goals;c._finish_world_fixture('world|friendly|'+f['id'],c._competition_club(book.nations[other]),c._competition_club(book.nations[actor]),2,0,(1,2))
        self.assertEqual((c.matches,c.goals),before);self.assertEqual((c.international_caps,c.international_goals),(1,2))
    def test_season_honours_moves_qualifies_and_roundtrips_global_memberships(self):
        c=self.career();from domestic_playoffs import eligible_table
        c.club_name=eligible_table(c.current_league)[0].name;c._ensure_competitions();uid=c.club.uid;c.club.points=999
        c._finish_season();self.assertEqual(c.season,2027);self.assertEqual(c.league_key,'Portugal|1');self.assertEqual(c.club.uid,uid)
        self.assertTrue(c.competition_archive[-1]['winners']);self.assertTrue(c.competition_archive[-1]['movements'])
        self.assertEqual(c.qualification_snapshot['season'],2027);self.assertEqual(len(c.qualification_snapshot['entries']['ucl']),36)
        c.save();d=CareerMode(Access(),save_slot='world');self.assertEqual(d.club.uid,uid);self.assertEqual(d.world_membership,c.world_membership)
        d._ensure_competitions();self.assertEqual(set(d.world_competitions.tournaments['ucl'].teams),{t['uid'] for t in c.qualification_snapshot['entries']['ucl']})
    def test_corrupt_new_state_cannot_replace_career_or_import_partial_history(self):
        from career_transfer import export_career,validated_import
        c=self.career();c.next_match();before=c.club.uid;c.save();original=c.save_path.read_bytes()
        save=json.loads(original);save['career']['competition_archive']=[{'season':2026,'winners':{'ucl':{'name':7}}}]
        c.save_path.write_text(json.dumps(save));self.assertFalse(c.load());self.assertEqual(c.club.uid,before)
        c.save_path.write_bytes(original);doc=json.loads(export_career(c));doc['save']['career']['world_competitions']['tournaments']['ucl']['champion']='missing'
        with self.assertRaises(ValueError):validated_import(c,json.dumps(doc))
        self.assertEqual(c.club.uid,before)
    def test_legacy_import_clears_previous_tournament_book_instead_of_reusing_it(self):
        from career_transfer import export_career,validated_import
        c=self.career();doc=json.loads(export_career(c));doc['save']['career'].pop('world_competitions',None)
        c.next_match();self.assertIsNotNone(c.world_competitions)
        restored=validated_import(c,json.dumps(doc));self.assertIsNone(restored.world_competitions)

    def test_third_place_requires_actual_playoff_and_reloads(self):
        from domestic_playoffs import eligible_table
        c=self.career();league=c.current_league;ranked=eligible_table(league);c.club_name=ranked[2].name;uid=c.club.uid
        for i,team in enumerate(ranked):team.points=100000-i*1000
        league.round_index=league.total_rounds;c.week=45;c._ensure_competitions()
        f=c.next_match()
        for _ in range(24):
            if f[0].startswith('world|playoff:Portugal:2|'):break
            score=(2,0) if f[1].uid==uid else (0,2);c.finish_match(f[1],f[2],0,0,competition=f[0],forced_score=score);f=c.next_match()
        self.assertEqual(c.season,2026);self.assertEqual(c.club.uid,uid);self.assertTrue(f[0].startswith('world|playoff:Portugal:2|'))
        c.save();d=CareerMode(Access(),save_slot='world');self.assertEqual(d.next_match()[0],f[0]);self.assertEqual(d.club.uid,uid)

    def test_transferred_country_cup_simulates_past_dates_without_personal_credit(self):
        c=self.career();c._ensure_competitions();c.week=20;c.league_key='Argentina|1';c.club_name=c.current_league.clubs[0].name
        before=c.matches,c.goals;c._ensure_competitions();cup=c.world_competitions.tournaments['domestic:Argentina']
        self.assertTrue(all(f['score'] is not None for f in cup.fixtures if f['week']<20))
        self.assertEqual((c.matches,c.goals),before)

    def test_global_pyramid_sizes_and_unique_ids_are_preserved(self):
        c=self.career('England');c._ensure_competitions();before={k:len(l.clubs) for k,l in c.leagues.items()};ids={x.uid for l in c.leagues.values() for x in l.clubs};c._finish_season()
        self.assertEqual(before,{k:len(l.clubs) for k,l in c.leagues.items()});after=[x.uid for l in c.leagues.values() for x in l.clubs];self.assertEqual(set(after),ids);self.assertEqual(len(after),len(ids))
