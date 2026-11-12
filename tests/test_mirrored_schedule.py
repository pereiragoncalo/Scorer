import unittest,random
from collections import Counter
from career import CareerClub,WorldLeague
from mirrored_schedule import supported,upgrade_if_compatible
class MirroredLeague(unittest.TestCase):
 def test_all_supported_sizes_mirror_order_venues_and_two_game_streaks(self):
  before=random.getstate()
  for n in range(2,65):
   if n==4:continue
   with self.subTest(teams=n):
    clubs=[CareerClub(str(i),'Test','Test',1,60,uid=str(i)) for i in range(n)];l=WorldLeague('Test','Test',1,clubs);half=l.total_rounds//2
    seen=Counter();venues={c.uid:'' for c in clubs}
    for r in range(half):
     first=l.pairings(r);second=l.pairings(r+half)
     self.assertEqual([(h.uid,a.uid) for h,a in first],[(a.uid,h.uid) for h,a in second])
     self.assertEqual(len({c.uid for pair in first for c in pair}),2*len(first))
     for h,a in first:seen[tuple(sorted((h.uid,a.uid)))]+=1
    self.assertEqual(len(seen),n*(n-1)//2);self.assertEqual(set(seen.values()),{1})
    for r in range(l.total_rounds):
     for h,a in l.pairings(r):venues[h.uid]+='H';venues[a.uid]+='A'
    for v in venues.values():
     self.assertLessEqual(abs(v[:n-1].count('H')-v[:n-1].count('A')),1);self.assertNotIn('HHH',v);self.assertNotIn('AAA',v);self.assertEqual(v.count('H'),n-1);self.assertEqual(v.count('A'),n-1)
  self.assertEqual(before,random.getstate())
 def test_early_old_seasons_upgrade_without_changing_played_fixtures(self):
  for n in (10,12,16,18,20,22,24):
   for played in (0,1,2):
    clubs=[CareerClub(str(i),'Test','Test',1,60,uid=str(i)) for i in range(n)];l=WorldLeague('Test','Test',1,clubs,schedule_version=2,round_index=played)
    before=[l.pairings(r) for r in range(played)];self.assertTrue(upgrade_if_compatible(l));self.assertEqual(l.schedule_version,3)
    self.assertEqual(before,[l.pairings(r) for r in range(played)])
 def test_four_team_exception_retains_existing_balanced_schedule(self):
  self.assertFalse(supported(4))
  clubs=[CareerClub(str(i),'Test','Test',1,60) for i in range(4)]
  a=WorldLeague('Test','Test',1,clubs,schedule_version=2);b=WorldLeague('Test','Test',1,clubs,schedule_version=3)
  self.assertEqual([a.pairings(r) for r in range(6)],[b.pairings(r) for r in range(6)])

 def test_version3_fixture_identity_is_frozen_for_saved_careers(self):
  import hashlib,json
  from mirrored_schedule import PATTERNS
  self.assertEqual(hashlib.sha256(json.dumps(PATTERNS,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'b6567c6fdd9d75ed5103b0993638b7f9f7e11c16365d3ff0b7111f236cba78e8')
