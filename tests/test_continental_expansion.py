"""Continental competition progression, persistence and upgrade regression tests."""
import copy,os,tempfile,unittest
from unittest.mock import patch
from career import CareerMode
from world_competitions import CompetitionBook,CLUB_FIELDS
from international_calendar import national_tournament_calendar
class Access:
    def has_world_access(self):return True

class ContinentalExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.env=patch.dict(os.environ,STRIKER_SAVE_DIR=cls.tmp.name);cls.env.start()
        cls.c=CareerMode(Access(),autoload=False,save_slot='world');cls.leagues=cls.c.leagues
    @classmethod
    def tearDownClass(cls):cls.env.stop();cls.tmp.cleanup()
    def test_fields_disjoint_regions_and_all_secondary_titles_complete(self):
        b=CompetitionBook(2026,29,self.leagues)
        for key,count in CLUB_FIELDS.items():self.assertEqual(len(b.tournaments[key].teams),count,key)
        for keys in [('ucl','uel','uecl'),('libertadores','sudamericana'),('caf_cl','caf_confederation'),('afc_elite','afc_two','afc_challenge')]:
            seen=set()
            for key in keys:
                ids=set(b.tournaments[key].teams);self.assertFalse(seen&ids,key);seen|=ids
        b.complete()
        for key in CLUB_FIELDS:self.assertTrue(b.tournaments[key].champion,key)
        self.assertEqual(len(b.tournaments['caf_confederation'].fixtures),62)
        for key in ('afc_two','afc_challenge'):
            cup=b.tournaments[key];west=set(x for g in cup.groups[:4 if key=='afc_two' else 3] for x in g)
            for f in cup.fixtures:
                if f['stage']!='Final':self.assertEqual(f['home'] in west,f['away'] in west)
        self.assertEqual(CompetitionBook.from_dict(b.to_dict()).to_dict(),b.to_dict())
    def test_sudamericana_draw_waits_for_libertadores_then_transfers_thirds_once(self):
        b=CompetitionBook(2026,30,self.leagues);s=b.tournaments['sudamericana'];l=b.tournaments['libertadores']
        s.advance(200);self.assertEqual(s.stage,'Awaiting Libertadores');self.assertFalse(b._continental_transfers())
        b=CompetitionBook.from_dict(b.to_dict());s=b.tournaments['sudamericana'];l=b.tournaments['libertadores'];l.advance(200)
        thirds={l.table(i)[2]['uid'] for i in range(8)}
        self.assertTrue(b._continental_transfers());self.assertFalse(b._continental_transfers())
        self.assertEqual(set(s.teams)&set(l.teams),thirds);self.assertEqual(len(s.direct),8)
        playoff=[f for f in s.fixtures if f['id'] in s.active]
        self.assertEqual(len(playoff),16)
        for f in playoff:self.assertNotEqual(f['home'] in thirds,f['away'] in thirds)
        b.complete();self.assertEqual(len(s.fixtures),141);self.assertTrue(s.champion)
    def test_existing_save_adds_only_missing_draws_without_personal_credit(self):
        c=CareerMode(Access(),autoload=False,save_slot='world');c.accept_starting_offer(c.offers[0]);c._ensure_competitions();b=c.world_competitions
        for key in ('sudamericana','caf_confederation','afc_two','afc_challenge'):del b.tournaments[key]
        b.tournaments['ucl'].advance(6);before=copy.deepcopy(b.tournaments['ucl'].to_dict());c.week=12;c.matches=7;c.goals=5
        c._ensure_competitions();self.assertEqual(b.tournaments['ucl'].to_dict(),before);self.assertEqual((c.matches,c.goals),(7,5))
        self.assertTrue(set(CLUB_FIELDS)<=set(b.tournaments));state=b.to_dict();c._ensure_competitions();self.assertEqual(b.to_dict(),state)
        self.assertTrue(c.save());d=CareerMode(Access(),save_slot='world');self.assertEqual(d.world_competitions.to_dict(),state)
    def test_secondary_qualification_snapshot_survives_reload_and_next_draw(self):
        c=CareerMode(Access(),autoload=False,save_slot='world');c.accept_starting_offer(c.offers[0]);c._ensure_competitions();c.world_competitions.complete()
        entries=c.world_competitions.entrants_for_next_season(c.leagues)
        c.season+=1;c.world_competitions=None;c.qualification_snapshot=dict(season=c.season,entries=entries)
        self.assertTrue(c.save());d=CareerMode(Access(),save_slot='world');self.assertEqual(d.qualification_snapshot,c.qualification_snapshot)
        d._ensure_competitions()
        for key in CLUB_FIELDS:self.assertEqual(set(d.world_competitions.tournaments[key].teams),{t['uid'] for t in entries[key]})
    def test_player_secondary_fixture_is_played_once_and_can_win_title(self):
        b=CompetitionBook(2026,32,self.leagues);actor=next(iter(b.tournaments['sudamericana'].teams));seen=set()
        for _ in range(24):
            found=b.next_fixture(100,actor,'Portugal',False)
            if not found:break
            key,f,home,away,national=found
            self.assertFalse(national);self.assertEqual(key,'sudamericana');self.assertNotIn(f['id'],seen);seen.add(f['id'])
            b.record(key,f['id'],[2,0] if home['uid']==actor else [0,2])
            b=CompetitionBook.from_dict(b.to_dict())
        self.assertEqual(b.tournaments['sudamericana'].champion,actor);self.assertGreaterEqual(len(seen),13)

    def test_same_week_national_fixtures_follow_dates_not_lexical_ids(self):
        from world_competitions import Tournament
        teams=[dict(uid=str(i),name=str(i),rating=70,country='Portugal',tier=1) for i in range(4)]
        cup=Tournament('copa','Test',teams,'date-order',groups=1,rounds=3,national=True)
        actor=cup.groups[0][0];own=[f for f in cup.fixtures if actor in (f['home'],f['away'])]
        early,late=own[:2];early.update(week=47,date='2028-06-07',id='copa:99');late.update(week=47,date='2028-06-11',id='copa:00')
        for f in cup.fixtures:
            if f not in (early,late):f['week']=50
        cup.active=[f['id'] for f in cup.fixtures]
        self.assertIs(cup.advance(47,[actor]),early)

    def test_all_seven_national_finals_and_copa_regional_places(self):
        completed=set()
        for year in range(2025,2029):
            b=CompetitionBook(year,31,self.leagues);b.complete()
            for key,title,final_year in national_tournament_calendar(year):
                if final_year==year+1:
                    cup=b.tournaments[key];self.assertTrue(cup.champion);completed.add(key)
                    if key=='copa':
                        from career import SOUTH_AMERICA_COUNTRIES
                        self.assertEqual(sum(t['country'] in SOUTH_AMERICA_COUNTRIES for t in cup.teams.values()),10)
        self.assertEqual(completed,{'world_cup','euro','copa','afcon','asian','gold','ofc_nations'})
