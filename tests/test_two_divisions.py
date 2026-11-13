import os,tempfile,unittest,json,copy
from unittest.mock import patch
from career import CareerMode,WORLD_COUNTRIES
from two_divisions import rotate_reserve
class Access:
    def has_world_access(self):return True
class TwoDivisionTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup);p=patch.dict(os.environ,STRIKER_SAVE_DIR=self.t.name);p.start();self.addCleanup(p.stop)
    def career(self):
        c=CareerMode(Access(),autoload=False,starter_country='Portugal',save_slot='world');c.accept_starting_offer(c.offers[0]);return c
    def test_every_country_has_two_destinations_and_ten_unplayable_reserves(self):
        c=self.career()
        for country in WORLD_COUNTRIES:
            self.assertEqual([l.tier for l in c.domestic_leagues(country)],[1,2]);self.assertEqual(len(c.reserve_clubs(country)),10)
            self.assertFalse(c.is_league_playable(country+'|3'))
            c.club_name='';c.choose_start_country(country);self.assertEqual(c.league_key,country+'|2')
    def test_fifo_survives_roundtrip_and_preserves_sizes_and_identities(self):
        c=self.career();lower=c.leagues['Portugal|2'];archive=c.leagues['Portugal|3'];before={x.uid for x in lower.clubs+archive.clubs};queue=list(c.relegation_pools['Portugal']);sizes=(len(lower.clubs),len(archive.clubs))
        down=[x.uid for x in lower.table()[-3:]];new,moves=rotate_reserve(lower,archive,queue);c.relegation_pools['Portugal']=new;c.world_membership={k:[x.uid for x in l.clubs] for k,l in c.leagues.items()}
        # Choose a surviving club so this isolated rotation tests only queue persistence.
        c.club_name=next(x.name for x in lower.clubs if x.uid not in queue);c.save();d=CareerMode(Access(),autoload=False,save_slot='world');self.assertTrue(d.load());self.assertEqual(d.relegation_pools['Portugal'],queue[3:]+down)
        self.assertEqual({x.uid for x in lower.clubs+archive.clubs},before);self.assertEqual((len(lower.clubs),len(archive.clubs)),sizes)
        q2,_=rotate_reserve(d.leagues['Portugal|2'],d.leagues['Portugal|3'],d.relegation_pools['Portugal']);self.assertEqual(q2[:4],queue[6:]);self.assertTrue(all(uid in q2 for uid in down))
    def test_free_agent_can_save_reload_export_and_sign_outside_window(self):
        from career_transfer import export_career,validated_import
        c=self.career();c.goals=7;uid=c.club.uid;c._release_contract('Released');self.assertTrue(c.save());d=CareerMode(Access(),autoload=False,save_slot='world');self.assertTrue(d.load());self.assertTrue(d.free_agent);self.assertEqual(d.released_club['uid'],uid);self.assertEqual(d.goals,7)
        text=export_career(d);restored=validated_import(d,text);self.assertTrue(restored.free_agent)
        d.week=12;self.assertTrue(d.transfer_window_open);name,key=d.agent_offers[0];d.accept_transfer(name,key);self.assertFalse(d.free_agent);self.assertEqual(d.club.name,name);self.assertEqual(d.goals,7)
    def test_full_rollover_drops_second_division_hero_and_rotates_all_countries(self):
        c=self.career();hero=c.club;uid=hero.uid;queue=list(c.relegation_pools['Portugal']);hero.points=-100000;c.goals=12;c.matches=30
        initial={country:(len(c.leagues[country+'|1'].clubs),len(c.leagues[country+'|2'].clubs)) for country in WORLD_COUNTRIES}
        c._finish_season();self.assertTrue(c.free_agent);self.assertEqual(c.released_club['uid'],uid);self.assertEqual(len(c.agent_offers),5);self.assertIn(uid,c.relegation_pools['Portugal']);remaining=[uid for uid in queue if uid in c.relegation_pools['Portugal']];self.assertEqual(c.relegation_pools['Portugal'][:len(remaining)],remaining);self.assertEqual(c.season,2027)
        for country in WORLD_COUNTRIES:
            self.assertEqual((len(c.leagues[country+'|1'].clubs),len(c.leagues[country+'|2'].clubs)),initial[country]);self.assertEqual(len(c.relegation_pools[country]),10)
        self.assertTrue(all((club.played,club.won,club.drawn,club.lost,club.points)==(0,0,0,0,0) for l in c.leagues.values() for club in l.clubs))
        self.assertTrue(c.save());d=CareerMode(Access(),autoload=False,save_slot='world');self.assertTrue(d.load());self.assertEqual(d.relegation_pools,c.relegation_pools);self.assertTrue(d.free_agent)
        self.assertEqual(d.season_review,c.season_review);self.assertIsNone(d.season_review['next_goal_target']);self.assertTrue(d.season_review['pending'])
    def test_bad_pool_fails_load_without_touching_career(self):
        c=self.career();c.save();data=json.loads(c.save_path.read_text());data['career']['relegation_pools']['Portugal'][0]=c.club.uid;c.save_path.write_text(json.dumps(data));name=c.club_name;self.assertFalse(c.load());self.assertEqual(c.club_name,name)
    def test_actual_v093_saves_migrate_with_history_and_first_write_backup(self):
        from pathlib import Path
        for name,released in [('world-v093-england4.json',True),('world-v093-portugal1.json',False)]:
            c=self.career();source=(Path(__file__).parent/'fixtures'/name).read_bytes();c.save_path.with_suffix('.two-divisions-backup.json').unlink(missing_ok=True);c.save_path.write_bytes(source);old=json.loads(source)['career']
            self.assertTrue(c.load());self.assertEqual(c.free_agent,released);self.assertEqual(c.goals,3);self.assertEqual(c.matches,4);self.assertEqual(c.week,8)
            self.assertEqual(c.fixture_history,old['fixture_history']);self.assertEqual(c.player_name,'Legacy Test');self.assertEqual(c.save_path.read_bytes(),source)
            self.assertEqual(c.world_competitions.to_dict(),old['world_competitions'])
            self.assertTrue(c.save());self.assertEqual(c.save_path.with_suffix('.two-divisions-backup.json').read_bytes(),source)
            again=CareerMode(Access(),autoload=False,save_slot='world');self.assertTrue(again.load());self.assertEqual(again.free_agent,released);self.assertEqual(again.relegation_pools,c.relegation_pools);self.assertEqual(again.message,c.message)

    def test_updated_name_pack_keeps_active_names_and_names_all_ten_reserves(self):
        from pathlib import Path
        root=Path(__file__).resolve().parents[1];old=json.loads((root/'docs/data/name-packs/Scorer-World-Real-Names-Divisions-2026.json').read_text());new=json.loads((root/'docs/data/name-packs/Scorer-World-Real-Names-Two-Divisions-2026.json').read_text())
        c=CareerMode(Access(),autoload=False,starter_country='Portugal',save_slot='world',domestic_formats=False);c.accept_starting_offer(c.offers[0]);c.apply_names(old);before=json.loads(c.save_path.read_text())['career'];c.apply_names(new);after=json.loads(c.save_path.read_text())['career']
        self.assertEqual([k for k in before if before[k]!=after[k]],['display_aliases']);self.assertEqual(len(new['clubs']),352);self.assertEqual(len(new['leagues']),16)
        for country in ('Portugal','England','Spain','Germany','Italy','France','Brazil','Argentina'):
            for l in c.domestic_leagues(country):
                for club in l.clubs:self.assertEqual(new['clubs'][club.uid],old['clubs'][club.uid])
            self.assertEqual(len({new['clubs'][club.uid] for club in c.reserve_clubs(country)}),10)

    def test_calendar_relegation_stops_before_requesting_a_fixture_for_a_free_agent(self):
        c=self.career();c.club.points=-100000;c.week=45;c.current_league.round_index=c.current_league.total_rounds;c._ensure_competitions();c.world_competitions.complete()
        self.assertIsNone(c.next_match());self.assertTrue(c.free_agent);self.assertIsNone(c.next_match())
        d=CareerMode(Access(),autoload=False,save_slot='world');self.assertTrue(d.load());self.assertTrue(d.free_agent);self.assertEqual(len(d.agent_offers),5)
        name,key=d.agent_offers[0];d.accept_transfer(name,key);d._ensure_competitions();self.assertIn(d.club.uid,d.world_competitions.tournaments['domestic:'+d.current_league.country].teams)
