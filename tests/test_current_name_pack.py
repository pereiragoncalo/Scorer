import copy,gzip,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from career import CareerMode
from tools.build_current_name_pack import build,BASE,MANIFEST
from tools.build_division_name_pack import load_registry,normalize

ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'docs/data/name-packs/Scorer-World-Real-Names-0.9.10.json'
COMPATIBLE=ROOT/'docs/data/name-packs/Scorer-World-Real-Names-Compatible.json'
class Access:
    def has_world_access(self):return True


class CurrentNamePackTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.env=patch.dict(os.environ,STRIKER_SAVE_DIR=self.t.name);self.env.start();self.addCleanup(self.env.stop)

    def test_complete_current_supported_slots_real_divisions_and_unique_identities(self):
        c=CareerMode(Access(),autoload=False,save_slot='world');pack=json.loads(PACK.read_text());c.preview_names(PACK.read_text())
        registry,lookups=load_registry(MANIFEST);seen=set()
        countries={k.split('|')[0] for k in pack['leagues']};self.assertEqual(len(countries),8)
        for country in countries:
            for tier in (1,2,3):
                clubs=c.reserve_clubs(country) if tier==3 else c.leagues[f'{country}|{tier}'].clubs
                for club in clubs:
                    team=lookups[country][normalize(pack['clubs'][club.uid])]
                    self.assertIn(team,registry[country,tier]['teams'])
                    key=country,team['identity'];self.assertNotIn(key,seen);seen.add(key)
        self.assertEqual(len(seen),378);self.assertLessEqual(PACK.stat().st_size,262144)
        self.assertLessEqual(sum(len(pack[k]) for k in ('clubs','players','leagues')),4096)

    def test_previous_club_and_player_aliases_all_preserved(self):
        old=json.loads(BASE.read_text());new=json.loads(PACK.read_text());compatible=json.loads(COMPATIBLE.read_text())
        self.assertEqual(compatible,old)
        for section in ('clubs','players','leagues'):
            self.assertTrue(set(old[section])<=set(new[section]))
            for key,value in old[section].items():self.assertEqual(new[section][key],value)
        self.assertEqual(len(new['clubs'])-len(old['clubs']),26)

    def test_compatible_imports_in_both_models_current_pack_needs_current_ids(self):
        for modern in (True,False):
            c=CareerMode(Access(),autoload=False,save_slot='world',domestic_formats=modern)
            c.preview_names(COMPATIBLE.read_text())
            if modern:c.preview_names(PACK.read_text())
            else:
                with self.assertRaisesRegex(ValueError,'Unknown name identifier'):c.preview_names(PACK.read_text())

    def test_apply_backup_reload_preserves_progress_ids_results_and_competitions(self):
        c=CareerMode(Access(),autoload=False,save_slot='world');c.accept_starting_offer(c.offers[0]);c.goals=17;c._ensure_competitions();c.apply_names(BASE.read_text())
        before=c.save_path.read_bytes();data=json.loads(before)['career'];c.apply_names(PACK.read_text());after=json.loads(c.save_path.read_text())['career']
        self.assertEqual([k for k in data if data[k]!=after[k]],['display_aliases'])
        self.assertEqual(c.save_path.with_suffix('.names-backup.json').read_bytes(),before)
        d=CareerMode(Access(),save_slot='world');self.assertEqual(d.display_aliases,json.loads(PACK.read_text()));self.assertEqual(d.goals,17)

    def test_new_player_slots_have_sourced_names_only_and_match_report(self):
        report=json.loads(PACK.with_suffix('.provenance.json').read_text());pack=json.loads(PACK.read_text());old=json.loads(BASE.read_text())
        for row in report['assignments']:
            if row['uid'] in old['clubs']:continue
            for i in range(12):
                key=f"{row['uid']}:{i}"
                if i<len(row['real_player_names']):self.assertEqual(pack['players'][key],row['real_player_names'][i])
                else:self.assertNotIn(key,pack['players'])

    def test_generator_is_stable_when_league_and_reserve_order_change(self):
        with tempfile.TemporaryDirectory() as folder:
            clubs=Path(folder)/'clubs.csv.gz';players=Path(folder)/'players.csv.gz'
            with gzip.open(clubs,'wt') as f:f.write('club_id,name,domestic_competition_id\n')
            with gzip.open(players,'wt') as f:f.write('player_id,name,last_season,position,current_club_id,market_value_in_eur\n')
            expected,_,_=build(players,clubs)
            original=CareerMode
            def reverse(*args,**kwargs):
                c=original(*args,**kwargs)
                for league in c.leagues.values():league.clubs.reverse()
                for country in c.relegation_pools:c.relegation_pools[country].reverse()
                return c
            with patch('career.CareerMode',side_effect=reverse):actual,_,_=build(players,clubs)
            self.assertEqual(actual,expected)
