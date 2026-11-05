import json,unittest
from pathlib import Path
from types import SimpleNamespace
from club_profiles import catalogue,profile,stadium_capacity,ground,career_titles
ROOT=Path(__file__).resolve().parents[1]

class ClubProfiles(unittest.TestCase):
    def test_profiles_cover_current_real_identities_and_keep_historical_facts(self):
        pack=json.loads((ROOT/'docs/data/name-packs/Scorer-World-Real-Names-0.9.10.json').read_text())['clubs']
        data=catalogue();self.assertEqual(set(data),set(pack))
        for uid,row in data.items():
            self.assertEqual(row['club'],pack[uid]);self.assertTrue(1800<=row['founded']<=2026)
            self.assertTrue(row['stadium']);self.assertTrue(row['source'].startswith('https://'))
            self.assertTrue(250<=row['capacity']<=150000)
            for award in row['honours']:
                self.assertIs(type(award['count']),int);self.assertTrue(0<award['count']<1000)
                self.assertTrue(award['title']);self.assertNotIn(award['title'].casefold(),('winners','champions','runners-up','titles'))
        v=profile(SimpleNamespace(uid='f9554f2ce1ab5ff99892'))
        self.assertEqual((v['founded'],v['stadium'],v['capacity']),(1899,'Barradão',35618))
        self.assertIn(dict(title='Campeonato Brasileiro Série B',count=1),v['honours'])
        self.assertEqual(v['supporters'],'Os Imbatíveis')

    def test_missing_identity_does_not_invent_history_and_uses_separate_ground_model(self):
        club=SimpleNamespace(uid='not-a-real-reference',rating=60)
        row=profile(club);self.assertIsNone(row['founded']);self.assertIsNone(row['capacity']);self.assertEqual(row['honours'],[])
        self.assertGreater(stadium_capacity(club),0);self.assertIsNone(profile(club)['capacity'])

    def test_second_tier_threshold_is_strict_and_sizes_increase(self):
        self.assertEqual(ground(40000).tiers,1);self.assertEqual(ground(40001).tiers,2)
        samples=[ground(n) for n in (2500,8000,16000,35000,40000,50000,80000,100000)]
        self.assertEqual([s.lower_rows+s.upper_rows for s in samples],sorted(s.lower_rows+s.upper_rows for s in samples))
        self.assertLess(ground(8000).lower_rows,ground(35000).lower_rows)

    def test_career_trophies_are_team_specific_and_exclude_personal_golden_boot(self):
        c=SimpleNamespace(honours=dict(trophies=[dict(team_uid='a',competition='league:Brazil|1'),dict(team_uid='a',competition='scorer:Brazil|1'),dict(team_uid='b',competition='cup')]))
        self.assertEqual(career_titles(c,'a'),[c.honours['trophies'][0]])
