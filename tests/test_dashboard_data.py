import os,tempfile,unittest
from unittest.mock import patch
from career import CareerMode
from dashboard_data import dashboard_data

class DashboardDataTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.env=patch.dict(os.environ,STRIKER_SAVE_DIR=self.tmp.name);self.env.start();self.addCleanup(self.env.stop)
        self.c=CareerMode(autoload=False);self.c.set_player_name('Dashboard Player');self.c.accept_starting_offer(self.c.offers[0])
    def test_fixtures_are_exact_current_pairings_and_read_only(self):
        c=self.c;c.save();before=c.save_path.read_bytes();rng=c.rng.getstate()
        data=dashboard_data(c)
        self.assertEqual([(r.home,r.away) for r in data.fixtures],[(c.display_club(a),c.display_club(b)) for a,b in c.current_league.pairings()])
        self.assertEqual(len(data.fixtures),len(c.current_league.clubs)//2)
        self.assertEqual(sum(r.focus for r in data.fixtures),1)
        self.assertEqual(c.rng.getstate(),rng);self.assertEqual(c.save_path.read_bytes(),before)
    def test_league_rank_uses_saved_totals_not_all_competition_hero_goals(self):
        c=self.c;c.goals=50;c.current_league.scorer_goals={'Zed Example (Test City)':3,c.player_name:2,'Aaron Example (Other City)':3}
        data=dashboard_data(c)
        self.assertEqual([(r.player,r.goals) for r in data.scorers],[('Aaron Example',3),('Zed Example',3),(c.player_name,2)])
        self.assertEqual(data.hero_rank,3);self.assertEqual(data.hero_league_goals,2)
        self.assertEqual(data.scorers[0].club,'Other City');self.assertTrue(data.scorers[-1].focus)
    def test_cup_next_match_keeps_distinct_next_league_jornada(self):
        c=self.c;c.week=c.cup_weeks[0];c.cup_round_index=0;c.cup_active=True
        round_before=c.current_league.round_index;data=dashboard_data(c)
        self.assertEqual(data.next_match[0],'cup');self.assertEqual(data.round_number,round_before+1)
        self.assertEqual(len(data.fixtures),len(c.current_league.clubs)//2);self.assertEqual(c.current_league.round_index,round_before)
    def test_finished_league_no_repeated_fake_round_and_zero_hero_not_invented_goals(self):
        c=self.c;c.current_league.round_index=c.current_league.total_rounds
        data=dashboard_data(c);self.assertEqual(data.fixtures,());self.assertEqual(data.hero_league_goals,0)
        self.assertEqual(c.current_league.scorer_goals,{})
