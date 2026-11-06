import unittest
from unittest.mock import patch
from test_menus import isolated_game,settle
from international_calendar import window_dates

class PlayoffCallupUITests(unittest.TestCase):
    def test_standings_show_promotion_and_both_playoff_boundaries(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True;c.league_key='France|2';c.club_name=c.current_league.clubs[0].name
            g.view='standings';g.draw();settle();zones=g._menu._table_zones(c.current_league)
            self.assertEqual(zones.promotion,(1,2));self.assertEqual(zones.playoff,(3,4,5,16));self.assertEqual(zones.relegation,(17,18))
            g.view='calendar';g.draw();settle();self.assertTrue(any('nation:'+c.nationality in (e.get('home_uid'),e.get('away_uid')) for e in c.calendar_entries()))
    def test_foreign_league_top_scorer_can_start_actual_national_match(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True;c.league_key='Brazil|1';c.club_name=c.current_league.clubs[0].name;c.nationality='Argentina';c.current_league.scorer_goals={c.player_name:8};c._ensure_competitions()
            c.week=15
            for cup in c.world_competitions.tournaments.values():
                if not cup.national:cup.advance(15)
            c.last_training_week=c.week;c.attend_coach_meeting();g.view='hub';g.start_career_match();settle();self.assertTrue(g.match_is_international);self.assertIn('Argentina',(g.match_home.name,g.match_away.name));self.assertTrue(g.match_competition.startswith('world|'))

    def test_match_ai_uses_the_scheduled_neutral_venue_means(self):
        from domestic_playoffs import build_tournament
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True;c._ensure_competitions()
            cup=build_tournament('England',c.leagues['England|1'],c.leagues['England|2'],11,48);cup.finish();f=next(f for f in cup.fixtures if f.get('neutral'))
            home=c._competition_club(cup.teams[f['home']]);away=c._competition_club(cup.teams[f['away']]);c.league_key='England|2';c.club_name=home.name;c.last_training_week=c.week;c.attend_coach_meeting();c.world_competitions.tournaments[cup.key]=cup
            token='world|'+cup.key+'|'+f['id'];g.view='hub'
            with patch.object(c,'next_match',return_value=(token,home,away)),patch.object(c,'world_fixture_goal_means',wraps=c.world_fixture_goal_means) as means:
                g.start_career_match();settle();means.assert_called_with(token,home,away)
