import copy,json,os,random,tempfile,unittest,hashlib
from collections import Counter
from unittest.mock import patch
from career import CareerClub,CareerMode,WorldLeague
from alternating_schedule import PATTERNS,PREFIX18,pairings,venues,repeats,upgrade_if_compatible

class AlternationTests(unittest.TestCase):
 def league(self,n=18,version=4,played=0):
  return WorldLeague('Portugal','Segunda Liga',2,[CareerClub(str(i),'Portugal','Segunda Liga',2,60,uid=str(i))for i in range(n)],schedule_version=version,round_index=played)
 def test_even_sizes_have_three_or_fewer_breaks_and_mirrored_opponents(self):
  state=random.getstate()
  for n in range(6,65,2):
   l=self.league(n);seen=Counter()
   for r in range(n-1):
    a=l.pairings(r);b=l.pairings(r+n-1)
    self.assertEqual([(h.uid,a.uid)for h,a in a],[(a.uid,h.uid)for h,a in b])
    self.assertEqual(len({c.uid for p in a for c in p}),n)
    seen.update(tuple(sorted((h.uid,a.uid)))for h,a in a)
   self.assertEqual(len(seen),n*(n-1)//2);self.assertEqual(set(seen.values()),{1})
   all_rows=venues(l)
   for rows in all_rows.values():
    seq=''.join(v for _,v in rows)
    self.assertNotIn('HHH',seq);self.assertNotIn('AAA',seq)
    self.assertEqual(seq.count('H'),n-1);self.assertEqual(seq.count('A'),n-1)
    self.assertLessEqual(repeats(rows),3)
   self.assertEqual(sum(repeats(rows)for rows in all_rows.values()),3*n-6)
  self.assertEqual(random.getstate(),state)
 def test_portugal2_reduces_repeated_venues_without_rewriting_played_prefix(self):
  for played in (0,*PREFIX18):
   l=self.league(version=3,played=played)
   past=[l.pairings(r)for r in range(played)];before=venues(l)
   self.assertTrue(upgrade_if_compatible(l))
   self.assertEqual([l.pairings(r)for r in range(played)],past)
   self.assertLess(sum(repeats(s,played)for s in venues(l).values()),sum(repeats(s,played)for s in before.values()))
 def test_return_leg_already_played_keeps_old_calendar_and_first_leg_unchanged(self):
  l=self.league(version=3,played=21);before=[l.pairings(r)for r in range(l.total_rounds)]
  self.assertFalse(upgrade_if_compatible(l));self.assertEqual(l.schedule_version,3)
  self.assertEqual([l.pairings(r)for r in range(l.total_rounds)],before)
 def test_world_portugal_save_migrates_once_and_roundtrips_variant(self):
  class Access:
   def has_world_access(self):return True
  with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,STRIKER_SAVE_DIR=tmp):
   c=CareerMode(Access(),autoload=False,save_slot='world');c.choose_start_country('Portugal');c.accept_starting_offer(c.offers[0]);l=c.current_league
   self.assertEqual(len(l.clubs),18);l.schedule_version=3;l.round_index=4
   old=venues(l);uid=max(old,key=lambda uid:repeats(old[uid],4));c.club_name=next(t.name for t in l.clubs if t.uid==uid)
   past=[[(h.uid,a.uid)for h,a in l.pairings(r)]for r in range(4)];points={t.uid:t.points for t in l.clubs}
   self.assertTrue(c.save());d=CareerMode(Access(),autoload=False,save_slot='world');self.assertTrue(d.load());new=d.current_league
   self.assertEqual(new.schedule_version,4);self.assertEqual(new.schedule_variant,4)
   self.assertEqual([[(h.uid,a.uid)for h,a in new.pairings(r)]for r in range(4)],past)
   self.assertEqual({t.uid:t.points for t in new.clubs},points)
   first=[[(h.uid,a.uid)for h,a in new.pairings(r)]for r in range(new.total_rounds)]
   self.assertTrue(d.save());e=CareerMode(Access(),autoload=False,save_slot='world');self.assertTrue(e.load())
   self.assertEqual(e.current_league.schedule_variant,4)
   self.assertEqual([[(h.uid,a.uid)for h,a in e.current_league.pairings(r)]for r in range(e.current_league.total_rounds)],first)

 def test_version4_orientation_identity_is_frozen(self):
  self.assertEqual(hashlib.sha256(json.dumps([PATTERNS,PREFIX18],sort_keys=True,separators=(',',':')).encode()).hexdigest(),'31bfc1f6b1b1b1d02f842a3b06397b50f27e28e7d618f334646882d0000b7613')
 def test_invalid_saved_variant_is_rejected_without_replacing_the_career(self):
  with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,STRIKER_SAVE_DIR=tmp):
   c=CareerMode(autoload=False);c.accept_starting_offer(c.offers[0]);self.assertTrue(c.save());original=c.save_path.read_text();before=c.club_name
   for variant in ('4',999,-1,True):
    data=json.loads(original);data['career']['schedule_version']=4;data['career']['schedule_variant']=variant;c.save_path.write_text(json.dumps(data))
    self.assertFalse(c.load());self.assertEqual(c.club_name,before)
