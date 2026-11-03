"""Regression checks for real structures and honest research/runtime separation."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('format_catalogue', ROOT / 'tools/build_domestic_format_catalogue.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class DomesticFormatCatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = module.build()
        cls.definitions = json.loads((module.DATA / 'reviewed.json').read_text())['definitions']
        cls.sources = {s['id']: s for s in json.loads((module.DATA / 'source-index.json').read_text())['sources']}

    def definition(self, country, tier=1):
        return next(d for d in self.definitions if d['country'] == country and d['tier'] == tier)

    def test_unequal_split_schedules_and_new_season_changes(self):
        for country, tier, games in [('Finland', 1, [27, 32]), ('Wales', 1, [33, 35]),
                                     ('Northern Ireland', 2, [37]), ('Switzerland', 1, [38]),
                                     ('Scotland', 1, [38]), ('Argentina', 1, [32]),
                                     ('Argentina', 2, [36]), ('Paraguay', 1, [44])]:
            with self.subTest(country=country, tier=tier):
                self.assertEqual(self.definition(country, tier)['regular_games_per_club'], games)

    def test_split_cannot_duplicate_a_rank_or_lose_a_team(self):
        d = copy.deepcopy(self.definition('Wales'))
        p = next(p for p in d['phases'] if p['kind'] == 'split_round_robin')
        p['rank_ranges'][1] = [6, 9]
        self.assertTrue(any('partition' in e for e in module.validate_definition(d, self.sources)))
        d = copy.deepcopy(self.definition('Finland'))
        d['phases'][1]['group_sizes'] = [6, 5]
        self.assertTrue(any('cover' in e for e in module.validate_definition(d, self.sources)))

    def test_knockout_byes_must_conserve_entrants(self):
        d = copy.deepcopy(self.definition('England', 2))
        p = next(p for p in d['phases'] if p['kind'] == 'knockout')
        self.assertEqual(p['field'], 6)
        self.assertEqual(p['rounds'][0]['byes'], 2)
        p['rounds'][0]['byes'] = 0
        self.assertTrue(any('conserved' in e for e in module.validate_definition(d, self.sources)))

    def test_evidence_and_totals_are_required_to_agree(self):
        d = copy.deepcopy(self.definition('Finland'))
        d['regular_games_per_club'] = [32]
        self.assertTrue(any('totals' in e for e in module.validate_definition(d, self.sources)))
        d['source_ids'] = ['invented:league']
        self.assertTrue(any('source' in e for e in module.validate_definition(d, self.sources)))

    def test_averaging_is_not_annual_relegation(self):
        for tier, count in [(1, 2), (2, 3)]:
            movement = self.definition('Paraguay', tier)['movement']
            self.assertEqual(movement['relegation']['count'], count)
            self.assertEqual(movement['relegation']['basis'], 'three_season_points_per_game')
            self.assertNotIn('direct_relegation', movement)

    def test_unknown_and_absent_are_not_fabricated_leagues(self):
        rows = self.catalogue['countries']
        self.assertEqual(len(rows), len(module.WORLD_COUNTRIES))
        self.assertEqual(len({r['country'] for r in rows}), len(rows))
        liechtenstein = next(r for r in rows if r['country'] == 'Liechtenstein')
        self.assertEqual(liechtenstein['domestic_league'], 'absent')
        for division in liechtenstein['divisions']:
            self.assertEqual(division['status'], 'not_applicable')
            self.assertEqual(division['definitions'], [])
        bulgaria = self.definition('Bulgaria')
        self.assertEqual(bulgaria['teams'], 14)
        self.assertEqual(bulgaria['definition_status'], 'partially_defined')
        self.assertNotIn('regular_games_per_club', bulgaria)
        for row in rows:
            self.assertFalse(row['full_country_model_implemented'])
            for division in row['divisions']:
                if division['status'] == 'needs_review':
                    self.assertEqual(division['definitions'], [])
        self.assertTrue(all(d['runtime_status'] == 'not_integrated' for d in self.definitions))

    def test_false_identities_cannot_be_current_candidates(self):
        for s in self.sources.values():
            if 'femenina' in s['title'].lower() or s['title'] == 'New Zealand Football Championship':
                self.assertTrue(s['excluded_from_current_identities'])
        for d in self.definitions:
            self.assertTrue(d['source_ids'])
            self.assertTrue(all(self.sources[s]['url'].startswith('https://') for s in d['source_ids']))


if __name__ == '__main__':
    unittest.main()
