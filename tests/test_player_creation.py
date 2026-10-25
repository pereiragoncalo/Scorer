import os,tempfile,unittest
from unittest.mock import patch
import edition
from career import CareerMode

class PlayerCreationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        p=patch.dict(os.environ,STRIKER_SAVE_DIR=self.temp.name);p.start();self.addCleanup(p.stop)
        p=patch('edition.WORLD_BUILD',True);p.start();self.addCleanup(p.stop)
    def world(self):return CareerMode(edition.entitlement_provider(),autoload=False,starter_country='Portugal',save_slot='world')
    def test_independent_nationality_start_country_and_reload(self):
        c=self.world();self.assertTrue(c.configure_new_player('marco costa','Brazil','Japan'))
        self.assertEqual((c.player_name,c.nationality,c.current_league.country),('Marco Costa','Brazil','Japan'))
        self.assertTrue(all(name in [club.name for club in c.current_league.clubs] for name in c.offers))
        c.accept_starting_offer(c.offers[0]);d=self.world();self.assertTrue(d.load())
        self.assertEqual((d.nationality,d.league_key,d.club_name),(c.nationality,c.league_key,c.club_name))
        self.assertEqual(c.suggested_country,'Portugal')
    def test_failed_save_rolls_back_fields_offers_rng_and_previous_file(self):
        previous=self.world();previous.accept_starting_offer(previous.offers[0])
        c=self.world();before=c.save_path.read_bytes()
        identity=(c.player_name,c.nationality,c.league_key,c.free_start_key,list(c.offers),set(c._active_world_countries),c.rng.getstate())
        with patch.object(c,'save',return_value=False):self.assertFalse(c.configure_new_player('Marco Costa','Brazil','Mexico'))
        self.assertEqual((c.player_name,c.nationality,c.league_key,c.free_start_key,c.offers,c._active_world_countries,c.rng.getstate()),identity)
        self.assertEqual(c.save_path.read_bytes(),before)
    def test_reject_invalid_choices_names_free_and_established_careers(self):
        c=self.world();before=(c.player_name,c.nationality,c.league_key,c.rng.getstate())
        for args in [('Marco Costa','../keys','Japan'),('Marco Costa','Brazil','unknown'),('', 'Brazil','Japan'),('Marco Costa',{},'Japan')]:
            with self.assertRaises(ValueError):c.configure_new_player(*args)
            self.assertEqual((c.player_name,c.nationality,c.league_key,c.rng.getstate()),before)
        free=CareerMode(autoload=False,save_slot='free')
        with self.assertRaises(ValueError):free.configure_new_player('Marco Costa','Brazil','Japan')
        self.assertFalse(free.world_unlocked)
        c.accept_starting_offer(c.offers[0]);before=c.save_path.read_bytes()
        with self.assertRaises(ValueError):c.configure_new_player('Another Player','Brazil','Japan')
        self.assertEqual(c.save_path.read_bytes(),before)
    def test_england_starts_in_fourth_division_without_changing_nationality(self):
        c=self.world();self.assertTrue(c.configure_new_player('Marco Costa','Portugal','England'))
        self.assertEqual((c.league_key,c.nationality),('England|4','Portugal'))
