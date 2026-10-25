import os
import json
import tempfile
import unittest
from unittest.mock import patch

from career import CareerMode, EUROPE_PYRAMID_DEPTH
from domestic_rules import division_depth, exchange_three, standing_zone


class Access:
    def has_world_access(self):
        return True


class SimplifiedDomesticTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        env = patch.dict(os.environ, STRIKER_SAVE_DIR=tmp.name)
        env.start()
        self.addCleanup(env.stop)

    def career(self, country='Yemen'):
        c = CareerMode(Access(), autoload=False, starter_country=country, save_slot='world')
        c.accept_starting_offer(c.offers[0])
        return c

    def rank(self, league):
        for index, club in enumerate(league.clubs):
            club.points = 100 - index * 4
            club.rating = 40 + index  # Rating must not override the table.
        return league.table()

    def test_new_world_uses_two_divisions_except_priority_countries(self):
        c = self.career()
        self.assertEqual(c.league_key, 'Yemen|2')
        for country in ('Yemen', 'United States', 'Japan', 'New Zealand'):
            self.assertEqual([l.tier for l in c.domestic_leagues(country)], [1, 2])
            self.assertNotIn(country+'|3', c.leagues)
        for country in ('Brazil', 'Argentina', 'Mexico'):
            self.assertEqual(division_depth(country, EUROPE_PYRAMID_DEPTH), 4)
        self.assertEqual(division_depth('England', EUROPE_PYRAMID_DEPTH), 5)
        self.assertEqual(division_depth('Portugal', EUROPE_PYRAMID_DEPTH), 4)

    def test_exact_three_ranked_clubs_move_with_identities_and_sizes_preserved(self):
        c = self.career()
        upper, lower = c.leagues['Yemen|1'], c.leagues['Yemen|2']
        top, bottom = self.rank(lower), self.rank(upper)
        promoted, relegated = {x.uid for x in top[:3]}, {x.uid for x in bottom[-3:]}
        original = {x.uid: x for x in upper.clubs + lower.clubs}
        counts = len(upper.clubs), len(lower.clubs)
        up, down = exchange_three(upper, lower)
        self.assertEqual((up, down), (promoted, relegated))
        self.assertEqual((len(upper.clubs), len(lower.clubs)), counts)
        self.assertEqual({x.uid for x in upper.clubs + lower.clubs}, set(original))
        for league in (upper, lower):
            for club in league.clubs:
                self.assertIs(club, original[club.uid])
                self.assertEqual((club.tier, club.league), (league.tier, league.name))

    def test_duplicate_identity_rejected_before_any_mutation(self):
        c = self.career()
        upper, lower = c.leagues['Yemen|1'], c.leagues['Yemen|2']
        lower.clubs[0].uid = upper.clubs[0].uid
        before = list(upper.clubs), list(lower.clubs)
        with self.assertRaises(ValueError):
            exchange_three(upper, lower)
        self.assertEqual((upper.clubs, lower.clubs), before)

    def test_season_moves_hero_by_table_and_reload_preserves_all_clubs(self):
        c = self.career()
        upper, lower = c.leagues['Yemen|1'], c.leagues['Yemen|2']
        self.rank(upper)
        self.rank(lower)
        c.club_name = lower.table()[1].name
        uid = c.club.uid
        before = {x.uid for x in upper.clubs + lower.clubs}
        c._finish_season()
        self.assertEqual(c.league_key, 'Yemen|1')
        self.assertEqual(c.club.uid, uid)
        self.assertEqual(before, {x.uid for x in upper.clubs + lower.clubs})
        self.assertTrue(c.save())
        restored = CareerMode(Access(), save_slot='world')
        self.assertEqual(restored.club.uid, uid)
        self.assertEqual(restored.league_key, 'Yemen|1')
        for key in ('Yemen|1', 'Yemen|2'):
            self.assertEqual({x.uid for x in c.leagues[key].clubs},
                             {x.uid for x in restored.leagues[key].clubs})

    def test_historical_tier_four_save_survives_then_migrates_at_season_boundary(self):
        c = self.career()
        c._build_world({'Yemen': 4})
        c.league_key = c.free_start_key = 'Yemen|4'
        c.club_name = c.current_league.clubs[0].name
        uid = c.club.uid
        self.assertTrue(c.save())
        restored = CareerMode(Access(), save_slot='world')
        self.assertEqual((restored.league_key, restored.club.uid), ('Yemen|4', uid))
        self.assertEqual([x.tier for x in restored.domestic_leagues('Yemen')], [1, 2])
        self.assertFalse(restored.is_league_playable('Yemen|3'))
        self.assertTrue(restored.is_league_playable('Yemen|4'))
        all_ids = {x.uid for l in restored.leagues.values() for x in l.clubs}
        restored._finish_season()
        self.assertEqual((restored.league_key, restored.club.uid), ('Yemen|2', uid))
        self.assertFalse(restored.is_league_playable('Yemen|4'))
        self.assertEqual(all_ids, {x.uid for l in restored.leagues.values() for x in l.clubs})
        self.assertTrue(restored.save())
        again = CareerMode(Access(), save_slot='world')
        self.assertEqual((again.league_key, again.club.uid), ('Yemen|2', uid))

    def test_zone_boundaries_no_playoffs_or_third_tier(self):
        for tier, pos, expected in ((2, 3, 'Promotion'), (2, 4, ''),
                                    (1, 9, ''), (1, 10, 'Relegation'),
                                    (2, 12, ''), (1, 1, ''), (3, 1, '')):
            self.assertEqual(standing_zone(tier, pos, 12), expected)

    def test_older_world_save_preserves_aliases_for_unvisited_archived_divisions(self):
        c = self.career()
        c._build_world({'Japan': 4})
        club = c.leagues['Japan|4'].clubs[0]
        c.apply_names({'version': 1, 'clubs': {club.uid: 'My Old Japanese Club'}})
        self.assertTrue(c.save())
        raw = json.loads(c.save_path.read_text())
        raw['career'].pop('domestic_model_version')
        raw['career'].pop('legacy_domestic_depths')
        c.save_path.write_text(json.dumps(raw))
        restored = CareerMode(Access(), save_slot='world')
        self.assertIsNotNone(restored.club)
        self.assertEqual(restored.display_aliases['clubs'][club.uid], 'My Old Japanese Club')
        self.assertEqual(len(restored.domestic_leagues('Japan')), 2)
        self.assertFalse(restored.is_league_playable('Japan|4'))
        self.assertTrue(restored.save())
        again = CareerMode(Access(), save_slot='world')
        self.assertEqual(again.display_aliases['clubs'][club.uid], 'My Old Japanese Club')

    def test_invalid_archive_metadata_does_not_replace_current_career(self):
        c = self.career()
        self.assertTrue(c.save())
        before = c.club.uid
        raw = json.loads(c.save_path.read_text())
        raw['career']['legacy_domestic_depths'] = {'Yemen': 999999}
        c.save_path.write_text(json.dumps(raw))
        self.assertFalse(c.load())
        self.assertEqual(c.club.uid, before)
