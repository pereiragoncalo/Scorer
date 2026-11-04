"""Regression checks for real structures and honest research/runtime separation."""
import copy
import itertools
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

    def test_peruvian_repechage_preserves_two_distinct_promoted_clubs(self):
        graph = next(p for p in self.definition('Peru', 2)['phases'] if p['kind'] == 'bracket_graph')
        self.assertEqual(len(graph['matches']), 5)
        for outcomes in itertools.product((0, 1), repeat=len(graph['matches'])):
            resolved = {'seed:' + seed: seed for seed in graph['seeds']}
            for match, winner_index in zip(graph['matches'], outcomes):
                clubs = [resolved[ref] for ref in match['inputs']]
                self.assertNotEqual(*clubs)
                resolved['winner:' + match['id']] = clubs[winner_index]
                resolved['loser:' + match['id']] = clubs[1 - winner_index]
            promoted = [resolved[ref] for ref in graph['outputs']['promotion']]
            self.assertEqual(len(set(promoted)), 2)
            self.assertIn(resolved['winner:final'], promoted)
            # Losing the title final alone must never award the second place.
            self.assertEqual(promoted[1], resolved['winner:runner_up_playoff'])
        self.assertEqual(graph['matches'][-1]['host'], 'loser:final')
        self.assertEqual(graph['matches'][-1]['decision'], 'penalties')

    def test_graph_rejects_forward_references_and_repeated_inputs(self):
        d = copy.deepcopy(self.definition('Peru', 2))
        graph = next(p for p in d['phases'] if p['kind'] == 'bracket_graph')
        graph['matches'][0]['inputs'][0] = 'winner:final'
        self.assertTrue(any('forward' in e for e in module.validate_definition(d, self.sources)))
        graph['matches'][0]['inputs'] = ['seed:qualifier_1', 'seed:qualifier_1']
        self.assertTrue(any('repeated' in e for e in module.validate_definition(d, self.sources)))

    def test_qualified_groups_do_not_add_games_to_eliminated_clubs(self):
        d = copy.deepcopy(self.definition('Colombia'))
        self.assertNotIn('regular_games_per_club', d)
        d['regular_games_per_club'] = [44]
        self.assertTrue(any('path-specific' in e for e in module.validate_definition(d, self.sources)))
        d.pop('regular_games_per_club')
        d['definition_status'] = 'structure_reviewed'
        self.assertTrue(any('point carry' in e for e in module.validate_definition(d, self.sources)))

    def test_current_transition_and_access_changes(self):
        self.assertEqual(self.definition('South Korea', 2)['regular_games_per_club'], [32])
        self.assertEqual(self.definition('Indonesia', 2)['regular_games_per_club'], [27])
        self.assertEqual(self.definition('Uruguay')['regular_games_per_club'], [37])
        self.assertEqual(self.definition('Uruguay', 2)['regular_games_per_club'], [32])
        self.assertEqual(self.definition('Ecuador')['regular_games_per_club'], [36, 40])
        cpl = next(p for p in self.definition('Canada')['phases'] if p['kind'] == 'knockout')
        self.assertEqual(cpl['field'], 4)
        self.assertEqual([r['legs'] for r in cpl['rounds']], [2, 1])
        sweden = self.definition('Sweden', 2)
        self.assertEqual(sweden['movement']['promotion_playoff'], [3, 4])

    def test_mls_best_of_three_is_not_aggregate_or_three_required_legs(self):
        d = copy.deepcopy(self.definition('United States'))
        self.assertEqual(d['regular_games_per_club'], [34])
        self.assertEqual(d['phases'][0]['kind'], 'scheduled_league')
        p = next(p for p in d['phases'] if p['kind'] == 'knockout')
        self.assertEqual(p['field'], 18)
        self.assertEqual(p['rounds'][0]['byes'], 14)
        self.assertEqual(p['rounds'][1]['format'], 'best_of')
        self.assertEqual(p['rounds'][1]['wins_required'], 2)
        self.assertEqual(p['rounds'][1]['decision'], 'penalties')
        p['rounds'][1].pop('format')
        self.assertTrue(any('tie rules' in e for e in module.validate_definition(d, self.sources)))

    def test_only_senior_tiers_are_created(self):
        for country in ('Gibraltar', 'San Marino'):
            row = next(r for r in self.catalogue['countries'] if r['country'] == country)
            tier2 = row['divisions'][1]
            self.assertEqual(tier2['status'], 'not_applicable')
            self.assertEqual(tier2['definitions'], [])
            self.assertTrue(tier2['absence']['source_ids'])
        self.assertEqual(self.definition('San Marino')['movement']['promotion_relegation'], 'only senior tier; none')

    def test_source_geography_does_not_match_a_country_substring(self):
        expected = {'Papua New Guinea Premier Soccer League': ['Papua New Guinea'],
                    'Campeonato Nacional da Guiné-Bissau': ['Guinea-Bissau'],
                    'South Sudan Premier League': ['South Sudan'],
                    'FFAS Senior League': ['American Samoa']}
        for source in self.sources.values():
            if source['title'] in expected:
                self.assertEqual(source['countries'], expected[source['title']])

    def test_ghana_four_playing_groups_have_three_promotion_zones(self):
        d = self.definition('Ghana', 2)
        self.assertEqual(d['teams'], 48)
        regular = d['phases'][0]
        self.assertEqual(regular['group_sizes'], [8, 8, 16, 16])
        self.assertEqual(regular['legs'], [4, 4, 2, 2])
        self.assertEqual(d['regular_games_per_club'], [28, 30])
        self.assertIn('not one from each subzone', d['movement']['direct_promotion'])
        self.assertEqual(d['movement']['relegation']['baseline'], {'Zone1': 3, 'Zone2': 2, 'Zone3': 2})
        self.assertTrue(d['movement']['relegation']['additional'])
        premier = self.definition('Ghana')['ranking_rules']
        self.assertNotEqual(premier['interim_order'], premier['final_order'])
        self.assertEqual(premier['final_order'][1], 'head_to_head_points')

    def test_south_african_survival_is_three_clubs_not_a_two_team_tie(self):
        for tier in (1, 2):
            d = self.definition('South Africa', tier)
            self.assertEqual(d['regular_games_per_club'], [30])
            cross = next(p for p in d['phases'] if p['kind'] == 'external_playoff')
            self.assertEqual(cross['entrants'], ['tier1:15', 'tier2:2', 'tier2:3'])
            self.assertNotIn('legs', cross)  # separate detailed competition rules not yet verified
            self.assertIn('psl:handbook-2025-12-02', d['source_ids'])

    def test_unknown_group_rules_cannot_silently_change_the_field(self):
        d = copy.deepcopy(self.definition('Nigeria', 2))
        phase = d['phases'][0]
        self.assertEqual(d['definition_status'], 'partially_defined')
        self.assertNotIn('regular_games_per_club', d)
        phase['proposed_group_sizes'] = [9, 9, 9, 9]
        self.assertTrue(any('cardinalities' in e for e in module.validate_definition(d, self.sources)))
        d = copy.deepcopy(self.definition('Czechia'))
        phase = next(p for p in d['phases'] if p['kind'] == 'qualified_round_robin')
        phase['selection']['rank_range'] = [1, 8]
        self.assertTrue(any('rank count' in e for e in module.validate_definition(d, self.sources)))

    def test_transitional_schedule_is_not_the_old_generic_league(self):
        d = self.definition('Mongolia')
        self.assertEqual(d['season_scope'], 'one_off_transition')
        self.assertEqual(d['teams'], 9)
        self.assertEqual(d['regular_games_per_club'], [14, 16])
        self.assertEqual(self.definition('Cyprus', 2)['regular_games_per_club'], [29])

    def test_false_identities_cannot_be_current_candidates(self):
        for s in self.sources.values():
            if 'femenina' in s['title'].lower() or s['title'] == 'New Zealand Football Championship':
                self.assertTrue(s['excluded_from_current_identities'])
        for d in self.definitions:
            self.assertTrue(d['source_ids'])
            self.assertTrue(all(self.sources[s]['url'].startswith('https://') for s in d['source_ids']))


if __name__ == '__main__':
    unittest.main()
