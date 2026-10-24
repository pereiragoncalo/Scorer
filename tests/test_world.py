import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from career import CareerMode, WORLD_COUNTRIES, FREE_LEAGUE_KEY
from device_locale import country_from_locale


class PreviewAccess:
    def has_world_access(self): return True
    def restore_world_access(self): return True


class WorldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.env = patch.dict(os.environ, STRIKER_SAVE_DIR=self.temp.name)
        self.env.start(); self.addCleanup(self.env.stop)

    def world(self, country='Portugal'):
        c = CareerMode(PreviewAccess(), autoload=False, starter_country=country)
        c.accept_starting_offer(c.offers[0])
        return c

    def test_locale_uses_region_then_language_with_safe_english_fallback(self):
        for tag, country in [('pt_PT','Portugal'),('pt-BR','Brazil'),('en-US','United States'),
                             ('en-GB','England'),('fr-CA','Canada'),('zh-Hant-TW','Chinese Taipei'),
                             ('pt','Portugal'),('cy-GB','Wales'),('gd-GB','Scotland'),
                             ('en-u-ca-gregory','England'),('xx-ZZ','England'),(None,'England')]:
            self.assertEqual(country_from_locale(tag), country, tag)

    def test_free_country_start_preserves_one_league_and_english_four_option(self):
        c = CareerMode(autoload=False, starter_country='Portugal')
        self.assertEqual(c.league_key, 'Portugal|4')
        self.assertTrue(c.choose_start_country('England'))
        self.assertEqual(c.league_key, FREE_LEAGUE_KEY)
        self.assertTrue(c.choose_start_country('Portugal'))
        c.accept_starting_offer(c.offers[0])
        self.assertFalse(c.choose_start_country('Brazil'))
        self.assertEqual(sum(c.is_league_playable(key) for key in c.leagues), 1)
        old = c.club_name
        restored = CareerMode()
        self.assertEqual(restored.club_name, old)
        self.assertEqual(restored.league_key, 'Portugal|4')
        self.assertFalse(restored.world_unlocked)
        self.assertTrue(all(key == 'Portugal|4' for _,key in restored.generate_agent_offers(True)))

    def test_world_covers_every_region_and_keeps_visited_tables_across_reload(self):
        c = self.world()
        self.assertEqual({v.country for v in c.leagues.values()}, set(WORLD_COUNTRIES))
        self.assertEqual(c.leagues['England|4'].name, 'England Division 4')
        self.assertEqual(len([v for v in c.leagues.values() if v.country == 'Brazil']), 4)
        self.assertEqual(len([v for v in c.leagues.values() if v.country == 'Yemen']), 4)
        self.assertEqual(len({club.uid for league in c.leagues.values() for club in league.clubs}), sum(len(v.clubs) for v in c.leagues.values()))
        kind,h,a=c.next_match();c.finish_match(h,a,0,1,forced_score=(0,0),competition=kind)
        c.activate_world_country('Brazil');c.save()
        before=[(v.key,v.round_index,[(x.uid,x.points,x.goals_for) for x in v.clubs],dict(v.scorer_goals)) for v in c.leagues.values() if v.country in ('Portugal','Brazil')]
        restored=CareerMode(PreviewAccess())
        after=[(v.key,v.round_index,[(x.uid,x.points,x.goals_for) for x in v.clubs],dict(v.scorer_goals)) for v in restored.leagues.values() if v.country in ('Portugal','Brazil')]
        self.assertEqual(before,after)
        free=CareerMode()
        self.assertFalse(free.world_unlocked)
        self.assertIsNotNone(free._locked_world_career)

    def test_names_import_changes_display_only_and_survives_reload(self):
        c=self.world();league=c.current_league;club=c.club
        original=club.name;uid=club.uid
        league.scorer_goals[f'{league.squad_names(original)[0]} ({original})']=5
        fixture=tuple(x.name for x in c.next_fixture())
        pack={'version':1,'clubs':{uid:'My Local Club'},'leagues':{league.key:'My Local League'},'players':{uid+':0':'Custom Scorer'}}
        preview=c.preview_names(json.dumps(pack))
        self.assertEqual(club.name,original)
        c.apply_names(preview)
        self.assertEqual(club.name,original)
        self.assertEqual(tuple(x.name for x in c.next_fixture()),fixture)
        self.assertEqual(sum(league.scorer_goals.values()),5)
        self.assertEqual(c.display_text(original),'My Local Club')
        self.assertEqual(c.display_scorer(next(iter(league.scorer_goals))),'Custom Scorer (My Local Club)')
        restored=CareerMode(PreviewAccess())
        self.assertEqual(restored.display_text(original),'My Local Club')
        self.assertEqual(sum(restored.current_league.scorer_goals.values()),5)
        self.assertTrue(c.save_path.with_suffix('.names-backup.json').exists())
        template=c.names_template();self.assertEqual(len(template['players']),12*len(league.clubs))

    def test_season_change_preserves_free_country_and_world_club_identity(self):
        free=CareerMode(autoload=False,starter_country='Portugal')
        free.accept_starting_offer(free.offers[0]);free.club.points=999
        free._finish_season()
        self.assertEqual(free.league_key,'Portugal|4')
        c=self.world();club=c.club;uid=club.uid;old_key=c.league_key
        c.apply_names({'version':1,'clubs':{uid:'Promotion Alias'}})
        c.club.points=999;c._finish_season()
        self.assertEqual(c.league_key,'Portugal|3')
        self.assertEqual(c.club.uid,uid)
        self.assertEqual(c.display_text(c.club_name),'Promotion Alias')
        self.assertEqual(sum(x.uid==uid for v in c.leagues.values() for x in v.clubs),1)
        self.assertEqual(len(c.leagues[old_key].clubs),18)
        self.assertEqual(len(c.current_league.clubs),18)

    def test_shorter_local_league_reaches_all_cup_rounds_before_new_season(self):
        import career
        c=self.world();season=c.season;rounds=[];league_games=0
        for _ in range(70):
            if c.season != season:break
            kind,h,a=c.next_match()
            if kind=='cup':rounds.append(c.cup_round_label)
            else:league_games+=1
            score=(1,0) if h.name==c.club_name else (0,1)
            c.finish_match(h,a,1,0,forced_score=score,competition=kind)
        self.assertEqual(rounds,list(career.CUP_ROUNDS))
        self.assertEqual(league_games,34)
        self.assertEqual(c.season,season+1)

    def test_same_name_in_other_country_never_receives_another_clubs_alias(self):
        c=self.world();seen={};pair=None
        for league in c.leagues.values():
            for club in league.clubs:
                if club.name in seen and seen[club.name].country != club.country:
                    pair=(seen[club.name],club);break
                seen[club.name]=club
            if pair:break
        self.assertIsNotNone(pair)
        first,second=pair
        c.apply_names({'version':1,'clubs':{first.uid:'One Club Only'}})
        self.assertEqual(c.display_club(first),'One Club Only')
        self.assertEqual(c.display_club(second),second.name)
        self.assertEqual(c.display_text(second.name,second.country),second.name)

    def test_invalid_or_failed_names_import_never_partially_changes_names(self):
        c=self.world();uid=c.club.uid
        before=c.save_path.read_bytes()
        for pack in [{'version':1,'clubs':{uid:'Valid Name','unknown':'Bad Name'}},
                     {'version':1,'clubs':{uid:'https://example.com'}},
                     {'version':1,'clubs':{uid:'[color=red]Bad'}},
                     {'version':1,'clubs':{uid:'Line\nBreak'}},
                     {'version':1,'clubs':{uid:'x'*57}},
                     {'version':True,'clubs':{uid:'Valid Name'}}]:
            with self.assertRaises(ValueError):c.apply_names(pack)
            self.assertEqual(c.save_path.read_bytes(),before)
        with self.assertRaises(ValueError):c.preview_names('x'*262145)
        with patch.object(c,'save',return_value=False):
            with self.assertRaises(ValueError):c.apply_names({'version':1,'clubs':{uid:'Valid Name'}})
        self.assertEqual(c.display_text(c.club_name),c.club_name)
        free=CareerMode(autoload=False)
        with self.assertRaises(ValueError):free.preview_names({'version':1,'clubs':{uid:'Valid Name'}})
