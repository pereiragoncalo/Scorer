import copy,os,tempfile,unittest
from unittest.mock import patch
from career import CareerMode
from world_competitions import CompetitionBook
from international_calendar import prepare_friendlies
class Access:
 def has_world_access(self):return True
class NoFriendliesTests(unittest.TestCase):
 def setUp(self):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);p=patch.dict(os.environ,STRIKER_SAVE_DIR=t.name);p.start();self.addCleanup(p.stop)
  self.c=CareerMode(Access(),autoload=False,save_slot='world');self.c.accept_starting_offer(self.c.offers[0]);self.c._ensure_competitions()
 def fixtures(self):
  book=self.c.world_competitions;own='nation:'+self.c.nationality;other=next(uid for uid in book.nations if uid!=own)
  return dict(id='friendly:future',home=own,away=other,week=0,stage='International friendly',score=None)
 def test_no_generation_and_scheduler_cannot_choose_legacy_friendly(self):
  c=self.c;b=c.world_competitions
  for nationality in ('Portugal','Brazil','Argentina'):prepare_friendlies(b,nationality)
  self.assertEqual(b.friendlies,{})
  f=self.fixtures();b.friendlies[f['id']]=f;next_game=b.next_fixture(0,c.club.uid,c.nationality,True)
  self.assertNotIn(f['id'],b.friendlies);self.assertTrue(next_game is None or next_game[0]!='friendly')
 def test_legacy_reload_removes_only_unplayed_and_keeps_results_and_officials(self):
  c=self.c;b=c.world_competitions;f=self.fixtures();played=dict(f,id='friendly:played',score=[2,1]);b.friendlies={f['id']:f,played['id']:played}
  before=copy.deepcopy(b.to_dict()['tournaments']);c.international_caps=7;c.international_goals=4
  self.assertTrue(c.save());self.assertTrue(c.load());b=c.world_competitions
  self.assertEqual(b.friendlies,{'friendly:played':played});self.assertEqual(b.to_dict()['tournaments'],before);self.assertEqual((c.international_caps,c.international_goals),(7,4))
  self.assertEqual(CompetitionBook.from_dict(b.to_dict()).to_dict(),b.to_dict())
 def test_calendar_does_not_advertise_pending_friendly(self):
  c=self.c;f=self.fixtures();c.world_competitions.friendlies[f['id']]=f
  self.assertFalse(any(e['competition']=='International friendly' for e in c.calendar_entries()))
  self.assertTrue(any(t.national for t in c.world_competitions.tournaments.values()))

 def test_old_friendly_results_are_hidden_without_rewriting_personal_totals(self):
  c=self.c;c.international_caps=7;c.international_goals=4
  c.fixture_history=[dict(date=c.current_date.isoformat(),competition='International friendly',home='Portugal',away='Brazil',status='1-0',played=True),dict(date=c.current_date.isoformat(),competition='International Friendlies',home='Portugal',away='Argentina',status='1-1',played=True)]
  self.assertTrue(c.save());self.assertTrue(c.load())
  self.assertEqual(len(c.fixture_history),2);self.assertEqual((c.international_caps,c.international_goals),(7,4))
  self.assertFalse(any('friendl' in str(e['competition']).lower() for e in c.calendar_entries()))
 def test_obsolete_friendly_newspaper_is_not_queued_after_reload(self):
  import newspaper
  c=self.c;_,h,a=c.next_match();entry=dict(date=c.current_date.isoformat(),competition='International friendly',status='1-0')
  c.press_state=newspaper.make_report(c.press_state,entry,h,a,c.club.uid,(1,0),1,0,[]);c.post_match_stage='newspaper'
  self.assertTrue(c.save());self.assertTrue(c.load());self.assertEqual(c.post_match_stage,'')
