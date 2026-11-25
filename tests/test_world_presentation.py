"""World presentation must not re-key teams, leak into Free, or bypass ownership."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from career import CareerMode, CareerClub, club_kit, hex_rgba
from world_clubs import catalogue
from club_kits import catalogue as kit_catalogue


class Access:
    def has_world_access(self):return True


class WorldPresentationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        env=patch.dict(os.environ,STRIKER_SAVE_DIR=self.temp.name);env.start();self.addCleanup(env.stop)

    def test_free_retains_legacy_morale_floors(self):
        career = CareerMode(autoload=False)
        strong = CareerClub('Strong opponent', 'England', 'Test', 1, 95)
        for morale, floor in ((10, 0), (10.001, 2), (15, 2), (15.001, 3), (20, 3)):
            career.morale = morale
            with patch.object(career.rng, 'gauss', return_value=-100):
                self.assertEqual(career.chance_count(strong), floor)

    def test_world_chance_limits_and_training_floor(self):
        career = CareerMode(Access(), autoload=False)
        weak = CareerClub('Weak opponent', 'England', 'Test', 1, 49)
        strong = CareerClub('Strong opponent', 'England', 'Test', 1, 95)
        career.morale = career.stamina = 20
        career.last_training_week = career.week
        with patch.object(career.rng, 'gauss', return_value=100):
            self.assertEqual(career.chance_count(strong), 3)
            self.assertEqual(career.chance_count(weak), 5)
            career.stamina = 18
            self.assertEqual(career.chance_count(weak), 4)
        with patch.object(career.rng, 'gauss', return_value=-100):
            self.assertEqual(career.chance_count(strong), 1)
        self.assertEqual(career.opponent_chance_profile(strong).clear_chance_probability, 0.08)

    def test_world_recent_goals_change_chance_distribution(self):
        career = CareerMode(Access(), autoload=False)
        career.morale = career.stamina = 15
        with patch.object(career.rng, 'gauss', side_effect=lambda centre, spread: centre):
            career.form_goals = [2, 2, 2, 2, 0, 0, 0, 0]
            drought = career.chance_count()
            career.form_goals.reverse()
            self.assertGreater(career.chance_count(), drought)

    def test_world_training_and_match_morale_can_recover(self):
        career = CareerMode(Access(), autoload=False)
        career.stamina, career.morale = 10, 10
        career.training_session_week = career.week
        career.training_shots_taken = 3
        with patch.object(career, 'save', return_value=False):
            self.assertEqual(career.complete_training(3), 0)
        self.assertEqual((career.stamina, career.morale), (10, 10))
        with patch.object(career, 'save', return_value=True):
            self.assertAlmostEqual(career.complete_training(3), -1.0)
            self.assertAlmostEqual(career.morale, 6.75)
            self.assertTrue(career.trained_this_week)
            self.assertEqual(career.complete_training(3), 0)
        morale, stamina = career.morale, career.stamina
        career._update_attributes(0, 1)
        self.assertAlmostEqual(morale - career.morale, 2.3275)
        self.assertAlmostEqual(stamina - career.stamina, 1.58)
        career._consume_match_training()
        career.training_session_week = career.week
        career.training_shots_taken = 3
        career.training_session_goals = 1
        morale = career.morale
        with patch.object(career, 'save', return_value=True):
            self.assertAlmostEqual(career.complete_training(1), -.35)
        self.assertAlmostEqual(morale - career.morale, 1.75)
        self.assertTrue(career.trained_this_week)
        with patch.object(career.rng, 'gauss', return_value=-100):
            self.assertEqual(career.chance_count(), 1)
        career._consume_match_training()
        career.training_session_week = career.week
        career.training_shots_taken = 3
        career.training_session_goals = 3
        with patch.object(career, 'save', return_value=True):
            self.assertAlmostEqual(career.complete_training(3), 3.6)

        career.morale = 0
        career._update_attributes(1, 1)
        self.assertGreater(career.morale, 2)

    def test_world_aim_speed_increases_after_each_promotion_and_free_is_unchanged(self):
        world=CareerMode(Access(),autoload=False,starter_country='England',save_slot='world')
        world.accept_starting_offer(world.offers[0]);world.last_training_week=world.week
        speeds=[]
        for tier in (5,4,3,2,1):
            world.club.tier=tier
            speeds.append(world.difficulty_profile()[1])
        self.assertEqual(speeds,sorted(set(speeds)))
        self.assertEqual(len(speeds),5)
        self.assertGreater(world.difficulty_profile(True)[1],speeds[-1])
        free=CareerMode(autoload=False,save_slot='free');free.accept_starting_offer(free.offers[0])
        self.assertEqual(free.difficulty_profile()[1],1.86)

    def test_catalogue_covers_stable_uids_with_unique_local_names_and_no_core_changes(self):
        world=CareerMode(Access(),autoload=False,domestic_formats=False)
        data=catalogue();self.assertEqual(len(data),10598)
        all_uids={c.uid for league in world.leagues.values() for c in league.clubs}
        self.assertTrue(all_uids <= set(data))  # Legacy-tier aliases remain available for old saves.
        for country in {l.country for l in world.leagues.values()}:
            clubs=[c for league in world.leagues.values() if league.country==country for c in league.clubs]
            before=[(c.uid,c.name,c.points,c.goals_for) for c in clubs]
            names=[world.display_club(c) for c in clubs]
            self.assertEqual(len(names),len(set(n.casefold() for n in names)))
            for club,name in zip(clubs,names):
                self.assertTrue(2<=len(name)<=56)
                self.assertIn(data[club.uid]['city'],name)
            self.assertEqual([(c.uid,c.name,c.points,c.goals_for) for c in clubs],before)
        free=CareerMode(autoload=False,save_slot='free')
        for club in free.current_league.clubs:
            self.assertEqual(free.display_club(club),club.name)
            self.assertEqual(free.kit_for_club(club),club_kit(club.name))

    def test_missing_presentation_file_falls_back_without_repeated_reads_or_losing_clubs(self):
        world=CareerMode(Access(),autoload=False);club=world.current_league.clubs[0]
        catalogue.cache_clear()
        try:
            kit_catalogue.cache_clear()
            with patch('world_clubs.Path.open',side_effect=OSError('unavailable')) as reader, patch('club_kits.Path.read_text',side_effect=OSError('unavailable')):
                self.assertEqual(world.display_club(club),club.name)
                self.assertEqual(world.display_club(club),club.name)
                self.assertEqual(world.kit_for_club(club),club_kit(club.name))
                self.assertEqual(reader.call_count,1)
        finally:
            catalogue.cache_clear();kit_catalogue.cache_clear()

    def test_reference_palette_and_user_alias_follow_uid_through_promotion_and_reload(self):
        world=CareerMode(Access(),autoload=False,starter_country='Portugal',save_slot='world')
        porto=next(c for c in world.leagues['Portugal|1'].clubs if c.name=='Porto Dragons')
        self.assertEqual(world.display_club(porto),'GD Porto')
        self.assertEqual(world.kit_for_club(porto)[0],hex_rgba('#0122EB'))
        world.accept_starting_offer(world.offers[0]);uid=world.club.uid
        name=world.display_club(world.club);kit=world.kit_for_club(world.club)
        world.club.points=999;world._finish_season()
        self.assertEqual(world.club.uid,uid)
        self.assertEqual((world.display_club(world.club),world.kit_for_club(world.club)),(name,kit))
        world.apply_names({'version':1,'clubs':{uid:'My Own Club'}})
        restored=CareerMode(Access(),save_slot='world')
        self.assertEqual(restored.display_club(restored.club),'My Own Club')
        self.assertEqual(restored.kit_for_club(restored.club),kit)
        template=restored.names_template();self.assertEqual(template['clubs'][uid],'My Own Club')
        restored.preview_names(json.dumps(template))


if __name__=='__main__':unittest.main()
