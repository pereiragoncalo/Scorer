import os,tempfile,unittest,copy
from unittest.mock import patch
from career import CareerMode
from world_competitions import Tournament
from competition_views import involved_competitions
import honours
class Access:
    def has_world_access(self):return True
class MembershipTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);p=patch.dict(os.environ,STRIKER_SAVE_DIR=self.tmp.name);p.start();self.addCleanup(p.stop)
        self.c=CareerMode(Access(),autoload=False,save_slot='world');self.c.accept_starting_offer(self.c.offers[0]);self.c._ensure_competitions()
    def test_only_involved_cups_and_read_only_membership(self):
        c=self.c;book=c.world_competitions;before=copy.deepcopy(book.to_dict());state=c.rng.getstate()
        keys={key for key,_ in involved_competitions(c)}
        self.assertIn('league:'+c.league_key,keys);self.assertIn('domestic:'+c.current_league.country,keys)
        for k,cup in book.tournaments.items():self.assertEqual(k in keys,not cup.national and c.club.uid in cup.teams)
        self.assertEqual(book.to_dict(),before);self.assertEqual(c.rng.getstate(),state)
    def test_played_former_club_and_national_campaign_stay_available(self):
        c=self.c;book=c.world_competitions;key='domestic:'+c.current_league.country;own=c.club
        honours.participate(c,key,book.tournaments[key].title,own.uid,own.name,own.country)
        oldleague=c.league_key;honours.participate(c,'league:'+oldleague,c.current_league.name,own.uid,own.name,own.country)
        c.league_key='Brazil|1';c.club_name=c.current_league.clubs[0].name
        national=next((k,v) for k,v in book.tournaments.items() if v.national and 'nation:'+c.nationality in v.teams)
        honours.participate(c,national[0],national[1].title,'nation:'+c.nationality,c.nationality,c.nationality)
        keys={k for k,_ in involved_competitions(c)}
        self.assertTrue({key,'league:'+oldleague,national[0]}<=keys)
        c.honours['campaigns']=[];keys={k for k,_ in involved_competitions(c)};self.assertNotIn(key,keys);self.assertNotIn(national[0],keys)
    def test_selected_nation_and_eliminated_cup_are_included(self):
        c=self.c;book=c.world_competitions;book.callups[c.nationality+':autumn']=True
        key='domestic:'+c.current_league.country;book.tournaments[key].finish()
        keys={k for k,_ in involved_competitions(c)};self.assertIn(key,keys)
        self.assertTrue(any(getattr(cup,'national',False) for k,cup in involved_competitions(c)))
