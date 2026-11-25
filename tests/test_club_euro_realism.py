import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from career import CareerMode, EUROPE_COUNTRIES, teammate_goal_mean
from contract_negotiation import SQUAD_INVESTMENT
from national_strength import EURO_RATINGS, euro_goal_means
from world_competitions import CompetitionBook


class WorldAccess:
    def has_world_access(self):
        return True


class WorldRealismTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        env = patch.dict('os.environ', STRIKER_SAVE_DIR=directory.name)
        env.start()
        self.addCleanup(env.stop)
        self.career = CareerMode(WorldAccess(), autoload=False)

    def test_renewal_improves_attack_and_defence_after_reload(self):
        career = self.career
        self.assertTrue(career.accept_starting_offer(career.offers[0]))
        club = career.club
        opponent = next(team for team in career.current_league.clubs if team != club)
        before = career.fixture_goal_means(club, opponent)
        terms = dict(years=2, salary=career.life['salary'], home='', car='', squad=True)
        with patch('contract_negotiation.renewal', return_value=True):
            with patch.object(career, 'save', return_value=False):
                self.assertFalse(career.accept_transfer(club.name, career.league_key, terms))
            self.assertEqual(career.life['squad_investments'], {})
            self.assertEqual(career.fixture_goal_means(club, opponent), before)
            self.assertTrue(career.accept_transfer(club.name, career.league_key, terms))

        # Simulate a save written by a version that lost the clause on reload.
        path = Path(career.save_path)
        payload = json.loads(path.read_text())
        payload['career']['life'].pop('squad_investments')
        path.write_text(json.dumps(payload))
        for _ in range(2):
            restored = CareerMode(WorldAccess())
            self.assertEqual(restored.life['squad_investments'], {club.uid: SQUAD_INVESTMENT})
            opponent = next(team for team in restored.current_league.clubs if team.uid == opponent.uid)
            after = restored.fixture_goal_means(restored.club, opponent)
            self.assertGreater(after[0], before[0])
            self.assertLess(after[1], before[1])
            self.assertTrue(restored.save())

    def test_world_teammates_keep_share_even_after_many_player_chances(self):
        self.assertAlmostEqual(teammate_goal_mean(.75, 1.2, world=True), .45)
        self.assertAlmostEqual(teammate_goal_mean(1.6, .2, world=True), 1.4)
        self.assertEqual(teammate_goal_mean(.75, 1.2, world=False), .05)

    def test_euro_draw_is_seeded_and_results_roundtrip(self):
        self.assertEqual(set(EURO_RATINGS), set(EUROPE_COUNTRIES))
        strong, weak = euro_goal_means('euro', 'Portugal', 'San Marino')
        self.assertGreater(strong, weak * 30)
        reversed_weak, reversed_strong = euro_goal_means('euro', 'San Marino', 'Portugal')
        self.assertAlmostEqual(reversed_weak, weak)
        self.assertAlmostEqual(reversed_strong, strong)
        book = CompetitionBook(2027, 36, self.career.leagues)
        euro = book.tournaments.get('euro')
        if euro is None:
            book.complete()
            euro = book.tournaments['euro']
        qualifiers = book.tournaments['euro_q0']
        self.assertEqual(len(qualifiers.qualified), 24)
        top = sorted(EUROPE_COUNTRIES, key=lambda country: (-EURO_RATINGS[country], 'nation:' + country))[:14]
        self.assertTrue(all(len({'nation:' + name for name in top}.intersection(group)) == 1
                            for group in qualifiers.groups))
        group_of = {uid: number for number, group in enumerate(euro.groups) for uid in group}
        round16 = [row for row in euro.fixtures if row['stage'] == 'Last 16']
        self.assertEqual(len(round16), 8)
        self.assertTrue(all(group_of[row['home']] != group_of[row['away']] for row in round16))
        restored = CompetitionBook.from_dict(book.to_dict())
        self.assertEqual(restored.tournaments['euro'].to_dict(), euro.to_dict())
