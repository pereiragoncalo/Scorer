"""World presentation must not re-key teams, leak into Free, or bypass ownership."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from career import CareerMode, CareerClub, club_kit, hex_rgba
from world_clubs import catalogue


class Access:
    def has_world_access(self):return True


class WorldPresentationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        env=patch.dict(os.environ,STRIKER_SAVE_DIR=self.temp.name);env.start();self.addCleanup(env.stop)

    def test_morale_floors_apply_at_strict_boundaries_even_against_elite_sides(self):
        for provider in (None,Access()):
            c=CareerMode(provider,autoload=False)
            strong=CareerClub('Strong opponent','England','Test',1,95)
            for morale,floor in ((10,0),(10.001,2),(15,2),(15.001,3),(20,3)):
                c.morale=morale
                with patch.object(c.rng,'gauss',return_value=-100):self.assertEqual(c.chance_count(strong),floor)
                with patch.object(c.rng,'gauss',return_value=100):self.assertLessEqual(c.chance_count(strong),3)
                self.assertEqual(c.opponent_chance_profile(strong).clear_chance_probability,0)

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
        world=CareerMode(Access(),autoload=False)
        data=catalogue();self.assertEqual(len(data),9896)
        all_uids={c.uid for league in world.leagues.values() for c in league.clubs}
        self.assertEqual(set(data),all_uids)
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
            with patch('world_clubs.Path.open',side_effect=OSError('unavailable')) as reader:
                self.assertEqual(world.display_club(club),club.name)
                self.assertEqual(world.display_club(club),club.name)
                self.assertEqual(world.kit_for_club(club),club_kit(club.name))
                self.assertEqual(reader.call_count,1)
        finally:catalogue.cache_clear()

    def test_reference_palette_and_user_alias_follow_uid_through_promotion_and_reload(self):
        world=CareerMode(Access(),autoload=False,starter_country='Portugal',save_slot='world')
        porto=next(c for c in world.leagues['Portugal|1'].clubs if c.name=='Porto Dragons')
        self.assertEqual(world.display_club(porto),'GD Porto')
        self.assertEqual(world.kit_for_club(porto)[0],hex_rgba('#005CA9'))
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
