import collections,copy,json,os,random,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from career import CareerMode
import domestic_formats as formats
class Access:
    def has_world_access(self):return True
class RuntimeDomesticTests(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory();self.addCleanup(self.folder.cleanup)
        p=patch.dict(os.environ,STRIKER_SAVE_DIR=self.folder.name);p.start();self.addCleanup(p.stop)
    def career(self,country='Scotland',**kwargs):
        c=CareerMode(Access(),autoload=False,save_slot='world',starter_country=country,**kwargs);c.accept_starting_offer(c.offers[0]);return c
    def advance(self,league,until):
        while league.round_index<until:
            for h,a in league.pairings():league.simulate_fixture(h,a,random.Random(league.round_index),forced_score=(1,0))
            league.round_index+=1
    def test_new_sizes_and_old_canonical_identities_and_reserves(self):
        old=self.career(domestic_formats=False);new=self.career()
        before={c.uid for l in old.leagues.values() for c in l.clubs};after=[c.uid for l in new.leagues.values() for c in l.clubs]
        self.assertTrue(before<=set(after));self.assertEqual(len(after),len(set(after)))
        for country,pair in formats.catalogue().items():
            for tier,spec in pair.items():self.assertEqual(len(new.leagues[country+'|'+tier].clubs),spec['teams'])
            self.assertEqual(new.relegation_pools[country],old.relegation_pools[country])
        self.assertEqual([len(l.clubs) for l in new.domestic_leagues('Spain')],[20,22])
        self.assertEqual([len(l.clubs) for l in new.domestic_leagues('Brazil')],[20,20])
    def test_four_legs_reverse_each_pair_and_conserve_home_games(self):
        c=self.career();l=c.leagues['Scotland|2'];pairs=collections.Counter();home=collections.Counter()
        for r in range(l.total_rounds):
            fixtures=l.pairings(r);self.assertEqual(len(fixtures),5);self.assertEqual(len({x.uid for pair in fixtures for x in pair}),10)
            for h,a in fixtures:pairs[h.uid,a.uid]+=1;home[h.uid]+=1
        self.assertEqual(set(pairs.values()),{2});self.assertEqual(set(home.values()),{18})
    def test_split_freezes_membership_and_group_order(self):
        c=self.career();l=c.leagues['Scotland|1'];self.advance(l,33);l.table();groups=copy.deepcopy(l.format_groups)
        self.assertEqual([len(g) for g in groups],[6,6]);by={x.uid:x for x in l.clubs}
        for uid in groups[1]:by[uid].points=10000
        self.assertEqual([x.uid for x in l.table()[:6]],groups[0])
        for r in range(33,38):
            for h,a in l.pairings(r):self.assertTrue(any(h.uid in group and a.uid in group for group in groups))
        self.advance(l,38);self.assertEqual({x.played for x in l.clubs},{38})
    def test_half_points_apply_once_and_reload_does_not_halve_again(self):
        c=self.career('Austria');l=c.leagues['Austria|1'];self.advance(l,22);before={x.uid:x.points for x in l.clubs};l.table()
        self.assertEqual({x.uid:x.points for x in l.clubs},{uid:p//2 for uid,p in before.items()})
        expected=formats.state(l);points={x.uid:x.points for x in l.clubs};c.league_key=l.key;c.club_name=l.clubs[0].name;c.save()
        d=CareerMode(Access(),autoload=False,save_slot='world');self.assertTrue(d.load());self.assertEqual(formats.state(d.current_league),expected);d.current_league.table();self.assertEqual({x.uid:x.points for x in d.current_league.clubs},points)
    def test_unequal_split_finishes_lower_group_at27_and_top_at32(self):
        c=self.career('Finland');l=c.leagues['Finland|1'];self.advance(l,22);l.table();bottom=l.format_groups[1][0];self.advance(l,27)
        self.assertTrue(formats.player_finished(l,bottom));self.assertFalse(formats.player_finished(l,l.format_groups[0][0]))
        self.advance(l,32);by={x.uid:x for x in l.clubs};self.assertEqual({by[uid].played for uid in l.format_groups[0]},{32});self.assertEqual({by[uid].played for uid in l.format_groups[1]},{27})
    def test_finnish_final_round_higher_half_get_five_home_games(self):
        c=self.career('Finland');l=c.current_league;self.advance(l,18);ranked=[x.uid for x in formats.raw_table(l.clubs)];l.table();home=collections.Counter(h.uid for r in range(18,27) for h,a in l.pairings(r))
        self.assertEqual({home[u] for u in ranked[:5]},{5});self.assertEqual({home[u] for u in ranked[5:]},{4})
    def test_calendar_preview_never_draws_groups_from_unfinished_table(self):
        c=self.career('Austria');l=c.leagues['Austria|1'];self.assertEqual(l.pairings(22),[]);self.assertIsNone(l.format_groups);self.assertTrue(all(x.points==0 for x in l.clubs))
    def test_undrawn_phase_dates_are_visible_without_invented_opponents(self):
        c=self.career('Austria');c.league_key='Austria|1';c.club_name=c.current_league.clubs[0].name
        rows=[row for row in c.calendar_entries() if row.get('pending')]
        self.assertEqual(len(rows),10);self.assertTrue(all(row['home']=='—' and row['away']=='—' for row in rows));self.assertIsNone(c.current_league.format_groups)

    def test_legacy_save_retains_sizes_progress_and_history(self):
        c=self.career('Spain',domestic_formats=False);l=c.current_league;self.advance(l,3);c.fixture_history=[{'date':'2026-07-16','competition':l.name,'home':'A','away':'B','score':[1,0]}];c.save();original=c.save_path.read_bytes();points=[x.points for x in l.clubs]
        d=self.career();c.save_path.write_bytes(original);self.assertTrue(d.load());self.assertEqual(d.domestic_format_version,0);self.assertEqual(len(d.current_league.clubs),18);self.assertEqual(d.current_league.round_index,3);self.assertEqual([x.points for x in d.current_league.clubs],points);self.assertEqual(d.fixture_history,c.fixture_history)
    def test_bad_split_membership_rejected_without_overwriting_original(self):
        c=self.career('Austria');l=c.current_league;c.league_key='Austria|1';c.club_name=c.current_league.clubs[0].name;l=c.current_league;self.advance(l,23);c.save();raw=json.loads(c.save_path.read_text());raw['career']['domestic_schedule']['groups'][0][0]='missing';c.save_path.write_text(json.dumps(raw));before=c.club.uid;self.assertFalse(c.load());self.assertEqual(c.club.uid,before)
    def test_new_access_fixes_are_played_and_persist_without_changing_legacy(self):
        from domestic_playoffs import build_tournament,profile,movements
        from world_competitions import Tournament,CompetitionBook
        c=self.career('South Africa');upper,lower=c.domestic_leagues('South Africa')
        cup=build_tournament('South Africa',upper,lower,7,48)
        self.assertEqual(len(cup.teams),3);self.assertEqual(len(cup.fixtures),6)
        self.assertEqual({row['p'] for row in cup.table()}, {0})
        cup.finish();self.assertEqual({row['p'] for row in cup.table()}, {4});self.assertEqual(len(cup.qualified),1)
        restored=Tournament.from_dict(cup.to_dict());self.assertEqual(restored.to_dict(),cup.to_dict())
        from types import SimpleNamespace
        up,down=movements(upper,lower,SimpleNamespace(tournaments={cup.key:cup}));self.assertEqual(len(up),len(down));self.assertIn(len(up),(1,2))
        upper,lower=c.domestic_leagues('Sweden');cup=build_tournament('Sweden',upper,lower,7,48)
        self.assertEqual([g['legs'] for row in cup.plan for g in row],[2,2]);cup.finish();self.assertEqual(len(cup.fixtures),4)
        self.assertEqual(profile('Sweden')['shape'],'parallel_cross')

    def test_two_season_rollover_export_and_membership_roundtrip(self):
        from career_transfer import export_career,validated_import
        c=self.career();before={x.uid for l in c.leagues.values() for x in l.clubs};sizes={k:len(l.clubs) for k,l in c.leagues.items()}
        for _ in range(2):
            c._finish_season()
            if c.free_agent:
                name,key=c.agent_offers[0];c.accept_transfer(name,key)
            self.assertEqual({k:len(l.clubs) for k,l in c.leagues.items()},sizes);self.assertEqual({x.uid for l in c.leagues.values() for x in l.clubs},before);self.assertTrue(c.save());d=CareerMode(Access(),autoload=False,save_slot='world');self.assertTrue(d.load());c=d
        self.assertEqual(validated_import(c,export_career(c)).domestic_format_version,1)
