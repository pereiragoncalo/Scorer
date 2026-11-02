import json
from pathlib import Path
from tests import test_two_divisions as helpers
from career import hex_rgba
from club_kits import catalogue

import unittest

class KitTests(unittest.TestCase):
    setUp=helpers.TwoDivisionTests.setUp
    career=helpers.TwoDivisionTests.career
    # Reuse isolated career helper, not the inherited test suite.
    def test_all_pack_clubs_have_uid_palettes_without_importing_names(self):
        c=self.career();pack=json.loads((Path(__file__).resolve().parents[1]/'docs/data/name-packs/Scorer-World-Real-Names-Two-Divisions-2026.json').read_text());by_uid={x.uid:x for l in c.leagues.values() for x in l.clubs}
        self.assertFalse(c.display_aliases['clubs']);self.assertEqual(set(pack['clubs']),set(catalogue()))
        before={uid:c.kit_for_club(by_uid[uid]) for uid in pack['clubs']}
        c.apply_names(pack)
        for uid,colours in before.items():self.assertEqual(c.kit_for_club(by_uid[uid]),colours)
        c.display_aliases['clubs'].clear()
        for uid,colours in before.items():
            club=by_uid[uid];club.name='Custom club';club.tier=1;club.country='Argentina'
            self.assertEqual(c.kit_for_club(club),colours)
    def test_reference_colours_and_save_reload(self):
        c=self.career();proof=json.loads((Path(__file__).resolve().parents[1]/'docs/data/club_kits.provenance.json').read_text())['clubs'];clubs={x.uid:x for l in c.leagues.values() for x in l.clubs}
        for country,name,shirt,trim in [('Portugal','Benfica','FE0000','FFFFFF'),('Portugal','Sporting CP','FFFFFF','008000'),('Portugal','Porto','0122EB','FFFFFF'),('Brazil','Flamengo','FF0000','000000'),('Argentina','Boca Juniors','000080','FFDD00')]:
            uid=next(uid for uid,r in proof.items() if r['country']==country and r['club']==name);kit=c.kit_for_club(clubs[uid]);self.assertEqual(kit[0],hex_rgba(shirt));self.assertEqual(kit[3],hex_rgba(trim))
        expected=c.kit_for_club(c.club);c.save();self.assertTrue(c.load());self.assertEqual(c.kit_for_club(c.club),expected)
    def test_colours_follow_reserve_rotation_and_transfers(self):
        from two_divisions import rotate_reserve
        c=self.career();lower=c.leagues['Portugal|2'];archive=c.leagues['Portugal|3'];queue=c.relegation_pools['Portugal'];up=next(x for x in archive.clubs if x.uid==queue[0]);before=c.kit_for_club(up)
        c.relegation_pools['Portugal'],_=rotate_reserve(lower,archive,queue)
        self.assertIn(up,lower.clubs);self.assertEqual(c.kit_for_club(up),before)
        c.week=0;c.agent_offers=[(up.name,lower.key)];c.accept_transfer(up.name,lower.key);self.assertEqual(c.club.uid,up.uid);self.assertEqual(c.kit_for_club(c.club),before)
    def test_offline_data_rebuilds_and_corruption_falls_back_safely(self):
        from tools.build_club_kits import build
        from unittest.mock import patch
        from club_kits import home_colours
        self.assertEqual(build(),json.loads((Path(__file__).resolve().parents[1]/'assets/data/club_kits.json').read_text()))
        c=self.career();catalogue.cache_clear()
        try:
            with patch('club_kits.Path.read_text',return_value='{"version":1,"clubs":{"bad":{"home":["oops"]}}}'):
                self.assertIsNone(home_colours(c.club));self.assertEqual(len(c.kit_for_club(c.club)),4)
        finally:catalogue.cache_clear()
