import copy,os,tempfile,unittest
from collections import Counter
from datetime import date
from unittest.mock import patch
from career import CareerMode
from world_competitions import CompetitionBook
from international_calendar import window_spans,window_dates
from national_campaigns import carried
from club_calendar import blocked,remaining_dates
class Access:
 def has_world_access(self):return True
class InternationalCampaigns(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();cls.env=patch.dict(os.environ,STRIKER_SAVE_DIR=cls.tmp.name);cls.env.start();cls.c=CareerMode(Access(),autoload=False)
 @classmethod
 def tearDownClass(cls):cls.env.stop();cls.tmp.cleanup()
 def play(self,b):
  games=[]
  for _ in range(80):
   pending=b.next_fixture(200,'','Portugal',True)
   if not pending:break
   key,f,_,_,_=pending;games.append((key,f['date']));b.record(key,f['id'],[5,0]if f['home']=='nation:Portugal'else[0,5])
  else:self.fail('National season did not terminate')
  return games
 def test_fifa_windows_have_four_or_two_slots_and_nations_real_round_dates(self):
  for season in range(2025,2034):
   days=window_dates(season)
   for a,b in window_spans(season):self.assertEqual(sum(a<=d<=b for d in days),4 if(b-a).days>=14 else 2)
  b=CompetitionBook(2026,36,self.c.leagues);games=self.play(b)
  self.assertEqual([d for k,d in games if k=='nations_a'],['2026-09-25','2026-09-29','2026-10-02','2026-10-06','2026-11-13','2026-11-17','2027-03-26','2027-03-30','2027-06-09','2027-06-13'])
 def test_euro_and_world_qualifiers_survive_july_and_finals_are_playable(self):
  for first,event,finalyear in ((2026,'euro',2028),(2028,'world_cup',2030)):
   b=CompetitionBook(first,36,self.c.leagues);self.play(b);b.complete();snapshot=carried(b)
   self.assertIn(event,[p['key']for p in snapshot['paths']]);before=copy.deepcopy(snapshot['tournaments'])
   after=CompetitionBook(first+1,36,self.c.leagues,b.entrants_for_next_season(self.c.leagues),national_state=snapshot)
   self.assertEqual({k:v.to_dict()for k,v in after.tournaments.items()if k in before},before)
   saved=CompetitionBook.from_dict(after.to_dict());games=self.play(saved)
   self.assertTrue(any(k.startswith(event+'_q')for k,d in games));self.assertTrue(any(k==event for k,d in games));self.assertEqual(saved.tournaments[event].champion,'nation:Portugal')
   if event=='euro':self.assertEqual([d for k,d in games if k==event][-1],'2028-07-09')
 def test_non_nations_a_qualifiers_begin_in_spring_and_all_national_caps_hold(self):
  b=CompetitionBook(2026,37,self.c.leagues);b.complete();q=b.tournaments['euro_q0'];self.assertTrue(any(f['date'].startswith('2027-03')for f in q.fixtures))
  seen=Counter()
  for cup in b.tournaments.values():
   if cup.national:
    for f in cup.fixtures:
     d=date.fromisoformat(f['date'])
     for uid in (f['home'],f['away']):
      for a,z in window_spans(2026)+window_spans(2027):
       if a<=d<=z:seen[uid,a,z]+=1
  for (uid,a,z),count in seen.items():self.assertLessEqual(count,(4 if(z-a).days>=14 else 2))
 def test_club_rounds_fit_with_breaks_midweeks_and_no_duplicate_dates(self):
  for season in range(2026,2032):
   for count in (30,34,38,46):
    days=remaining_dates(season,count,date(season,7,12),'Portugal')
    self.assertEqual(len(days),count);self.assertEqual(len(set(days)),count);self.assertEqual(tuple(sorted(days)),days)
    self.assertTrue(all(not blocked(d,season,'Portugal')for d in days));self.assertLessEqual(max(days),date(season+1,5,15))
    self.assertTrue(all((z-a).days>=3 for a,z in zip(days,days[1:])))
 def test_career_save_reload_carries_campaign_and_preserves_played_results(self):
  c=CareerMode(Access(),autoload=False);c.accept_starting_offer(c.offers[0]);c._ensure_competitions();c.world_competitions.complete();c._finish_season();before=copy.deepcopy(c.qualification_snapshot['national']);c.save();d=CareerMode(Access());self.assertEqual(d.qualification_snapshot['national'],before);d._ensure_competitions();self.assertIn('euro_q0',d.world_competitions.tournaments)

 def test_calendar_open_and_twelve_actual_games_are_chronological_and_reload_stable(self):
  c=CareerMode(Access(),autoload=False);c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting()
  entries=c.calendar_entries();future=[r for r in entries if not r.get('played')and r['competition']==c.current_league.name]
  self.assertTrue(future);self.assertTrue(all(not blocked(date.fromisoformat(r['date']),c.season,c.club.country)for r in future))
  days=[]
  for i in range(12):
   token,h,a=c.next_match();c.finish_match(h,a,0,0,competition=token,forced_score=(0,0));record=c.fixture_history[-1];day=date.fromisoformat(record['date']);days.append(day)
   if record['club_match']:self.assertFalse(blocked(day,c.season,c.club.country))
   if i==5:
    self.assertTrue(c.save());before=copy.deepcopy(c.world_competitions.to_dict());history=copy.deepcopy(c.fixture_history);self.assertTrue(c.load());self.assertEqual(c.fixture_history,history);self.assertEqual(c.world_competitions.to_dict(),before)
  self.assertEqual(days,sorted(days));self.assertEqual(len(days),len(set(days)))
 def test_legacy_dates_upgrade_keeps_scores_caps_and_fixture_identity(self):
  c=CareerMode(Access(),autoload=False);c.accept_starting_offer(c.offers[0]);c._ensure_competitions();b=c.world_competitions
  # Exact national fixture data generated by shipped source cded1dd (1030035).
  import gzip,json
  from pathlib import Path
  data=json.loads(gzip.decompress(Path('tests/fixtures/international-v1030035.json.gz').read_bytes()))
  c.world_competitions=b=CompetitionBook.from_dict(data)
  f=b.tournaments['nations_a'].fixtures[0];f['score']=[2,0]
  c.international_caps=7;c.international_goals=3
  from national_campaigns import upgrade
  played={f['id']:copy.deepcopy(f)for cup in b.tournaments.values()for f in cup.fixtures if f['score']is not None}
  before={k:[(f['id'],f['home'],f['away'],f['score'])for f in cup.fixtures]for k,cup in b.tournaments.items()}
  upgrade(c);self.assertEqual((c.international_caps,c.international_goals),(7,3))
  for cup in c.world_competitions.tournaments.values():
   for f in cup.fixtures:
    if f['id']in played:self.assertEqual(f,played[f['id']])
  for key,rows in before.items():self.assertEqual([(f['id'],f['home'],f['away'],f['score'])for f in c.world_competitions.tournaments[key].fixtures],rows)
 def test_corrupt_campaign_cannot_replace_the_saved_qualification(self):
  from national_campaigns import validate
  b=CompetitionBook(2026,36,self.c.leagues);b.complete();state=carried(b);bad=copy.deepcopy(state);bad['paths'][0]['groups']=True
  with self.assertRaises(ValueError):validate(bad,2027)
  bad=copy.deepcopy(state);bad['tournaments'][next(iter(bad['tournaments']))]['fixtures'][0]['date']='2099-01-01'
  with self.assertRaises(ValueError):validate(bad,2027)

 def test_retiming_next_game_retains_in_progress_training(self):
  c=CareerMode(Access(),autoload=False);c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();c._ensure_competitions()
  self.assertTrue(c.begin_training());self.assertTrue(c.record_training_shot(True,True));before=copy.deepcopy(c.development['session'])
  c.next_match();self.assertFalse(c.coach_meeting_required);self.assertEqual(c.training_session_week,c.week);self.assertEqual((c.training_shots_taken,c.training_session_goals),(1,1));self.assertEqual(c.development['session'],before)
