import unittest
from unittest.mock import patch
from kivy.uix.button import Button
from kivy.uix.label import Label
from test_menus import isolated_game,settle
from two_divisions import RELEGATED_MESSAGE

class TwoDivisionUITests(unittest.TestCase):
    def test_free_agent_can_load_find_offers_sign_and_exit_without_a_hub_loop(self):
        with patch('edition.WORLD_BUILD',True),isolated_game(saved=True) as g:
            g.career.accept_starting_offer(g.career.offers[0]);g._career_started=True;g.career._release_contract(RELEGATED_MESSAGE);g.career.save();g.view='start';g._load_career();settle()
            self.assertEqual(g.view,'agent');self.assertTrue(g._career_started)
            self.assertIn('FREE AGENT',{w.text for w in g._menu.walk() if isinstance(w,Label)})
            g.career.week=12;g._activate_ui('agent_refresh');self.assertEqual(len(g.career.agent_offers),5)
            g._request_exit();settle();self.assertIsNotNone(g._exit_popup);g._exit_popup.dismiss();settle()
            name,key=g.career.agent_offers[0];g._activate_ui('transfer',(name,key));settle();self.assertFalse(g.career.free_agent);self.assertEqual(g.view,'hub');self.assertEqual(g.career.club.name,name)
    def test_country_page_only_opens_two_leagues_and_displays_ten_reserve_names(self):
        with patch('edition.WORLD_BUILD',True),isolated_game(saved=True) as g:
            g._activate_ui('world_country','Portugal');settle();self.assertEqual(g.view,'world_country')
            names={w.text for w in g._menu.walk() if isinstance(w,Label)}
            for club in g.career.reserve_clubs('Portugal'):self.assertIn(g.career.display_club(club),names)
            self.assertEqual(len(g.career.domestic_leagues('Portugal')),2)
            g._activate_ui('world_league','Portugal|3');self.assertEqual(g.view,'world_country')
            g._activate_ui('world_league','Portugal|2');self.assertEqual(g.view,'world_league')

    def test_play_at_completed_season_routes_released_player_to_agent(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=g.career;c.accept_starting_offer(c.offers[0]);g._career_started=True;c.club.points=-100000;c.week=45;c.last_training_week=45;c.current_league.round_index=c.current_league.total_rounds;c._ensure_competitions();c.world_competitions.complete()
            g.view='hub';g.start_career_match();settle();self.assertEqual(g.view,'agent');self.assertTrue(c.free_agent);self.assertEqual(c.message,RELEGATED_MESSAGE);self.assertEqual(len(c.agent_offers),5)
