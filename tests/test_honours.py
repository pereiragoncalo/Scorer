import os,tempfile,unittest,copy
from unittest.mock import patch
from types import SimpleNamespace as NS
from career import CareerMode
from world_competitions import Tournament
import honours
class HonoursTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);e=patch.dict(os.environ,STRIKER_SAVE_DIR=t.name);e.start();self.addCleanup(e.stop)
    def signed(self):
        c=CareerMode(autoload=False);c.accept_starting_offer(c.offers[0]);return c
    def test_league_trophy_requires_actual_participation_and_win_and_survives_reload(self):
        c=self.signed();club=c.club;l=c.current_league
        for x in l.clubs:x.points=0
        club.points=999;l.round_index=l.total_rounds
        honours.collect(c,league=l);self.assertEqual(c.honours['trophies'],[])
        honours.participate(c,'league:'+l.key,l.name,club.uid,club.name,l.country)
        honours.collect(c,league=l);honours.collect(c,league=l)
        self.assertEqual(len(c.honours['trophies']),1);c.save()
        d=CareerMode();self.assertEqual(d.honours,c.honours)
    def test_cup_and_national_titles_deduplicate_and_exclude_qualification_and_playoffs(self):
        c=self.signed();teams=[dict(uid=str(i),name='Club '+str(i),country='England',tier=1,rating=70) for i in range(2)]
        for key,kind in (('cup','knockout'),('national','knockout'),('qualifier','qualifying'),('playoff:test','knockout')):
            cup=Tournament(key,'Title '+key,teams,'seed',kind='knockout');cup.finish();cup.kind=kind
            winner=cup.teams[cup.champion]
            honours.participate(c,key,cup.title,winner['uid'],winner['name'],'England')
            honours.collect(c,NS(tournaments={key:cup}))
        self.assertEqual(len(c.honours['trophies']),2)
        c.season+=1;honours.collect(c,NS(tournaments={}));self.assertEqual(len(c.honours['trophies']),2)
    def test_optional_corrupt_honours_are_bounded_and_cannot_damage_career(self):
        c=self.signed();self.assertEqual(honours.clean(None),honours.fresh())
        row=dict(season=2026,competition='cup',title='Cup',team_uid='uid',team='Team',country='England')
        raw=dict(version=1,trophies=[row]*600,campaigns=[dict(row,season=True)])
        self.assertEqual(honours.clean(raw)['trophies'],[row]);self.assertEqual(honours.clean(raw)['campaigns'],[])

    def test_actual_final_league_game_awards_title_and_boot_before_reset(self):
        c=self.signed();l=c.current_league;l.round_index=l.total_rounds-1
        for club in l.clubs:club.points=0
        c.club.points=999;l.scorer_goals[c.player_name]=99
        h,a=c.next_fixture();c.finish_match(h,a,0,0,forced_score=(1,0))
        trophies=c.honours['trophies'];self.assertTrue(any(t['competition']=='league:'+l.key for t in trophies))
        self.assertTrue(any(t['competition']=='scorer:'+l.key for t in trophies))
        self.assertEqual(CareerMode().honours,c.honours)

    def test_actual_legacy_cup_final_awards_once_and_preserves_club_after_transfer(self):
        from career import CUP_ROUNDS
        c=self.signed();c.cup_round_index=len(CUP_ROUNDS)-1;c.week=c.cup_weeks[c.cup_round_index]
        h,a=c.next_fixture();score=(1,0) if h.uid==c.club.uid else (0,1)
        c.finish_match(h,a,0,0,forced_score=score,competition='cup')
        self.assertTrue(any(x['competition'].startswith('domestic:') for x in c.honours['trophies']))
        old=copy.deepcopy(c.honours['trophies']);c.club_name=next(x.name for x in c.current_league.clubs if x.name!=c.club_name)
        c.save();self.assertEqual(CareerMode().honours['trophies'],old)
