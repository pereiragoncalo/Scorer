import random,unittest
from unittest.mock import patch
from menu_ui import CompactTable
from test_menus import isolated_game,settle
class DomesticFormatUITests(unittest.TestCase):
    def test_split_group_markers_and_readonly_table_after_phase_transition(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as game:
            c=game.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();game._career_started=True
            c.league_key='Austria|1';c.club_name=c.current_league.clubs[0].name;league=c.current_league
            while league.round_index<22:
                for home,away in league.pairings():league.simulate_fixture(home,away,random.Random(3),forced_score=(1,0))
                league.advance_round()
            self.assertEqual([len(g) for g in league.format_groups],[6,6]);c.save();saved=c.save_path.read_bytes();rng=c.rng.getstate();points=[x.points for x in league.clubs]
            game.view='standings';game.draw();settle();table=next(w for w in game.walk() if isinstance(w,CompactTable))
            self.assertTrue(str(table.rows[0][0]).startswith('1A'));self.assertTrue(str(table.rows[6][0]).startswith('7B'))
            self.assertEqual([x.points for x in league.clubs],points);self.assertEqual(c.rng.getstate(),rng);self.assertEqual(c.save_path.read_bytes(),saved)
    def test_new_brazilian_capacity_is_visible_in_the_real_table(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as game:
            c=game.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();game._career_started=True;c.league_key='Brazil|2';c.club_name=c.current_league.clubs[0].name
            game.view='standings';game.draw();settle();table=next(w for w in game.walk() if isinstance(w,CompactTable));self.assertEqual(len(table.rows),20)
