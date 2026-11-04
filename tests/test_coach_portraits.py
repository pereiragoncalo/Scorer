import hashlib,json,os,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch
from career import CareerMode
from coach import PORTRAITS,appearance_for,clean_appearance


class CoachPortraitTests(unittest.TestCase):
    def test_ten_distinct_bundled_original_portraits_and_bounded_selection(self):
        self.assertEqual(len(PORTRAITS),10)
        self.assertEqual(len({hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in PORTRAITS}),10)
        state=clean_appearance(None)
        for i in range(100):
            previous=state;state=appearance_for(str(i),previous)
            self.assertTrue(0<=state['portrait']<10)
            if previous['club']:self.assertNotEqual(previous['portrait'],state['portrait'])
            self.assertEqual(state,appearance_for(str(i),state))

    def test_hash_collision_cannot_reuse_previous_coach_appearance(self):
        uid='new-club';base=appearance_for(uid,None)['portrait']
        actual=appearance_for(uid,dict(club='old-club',portrait=base))
        self.assertNotEqual(actual['portrait'],base)

    def test_real_transfer_and_reload_keep_new_face_and_preserve_rng(self):
        with tempfile.TemporaryDirectory() as directory,patch.dict(os.environ,STRIKER_SAVE_DIR=directory):
            access=NS(has_world_access=lambda:True)
            c=CareerMode(access,autoload=False,save_slot='world');c.accept_starting_offer(c.offers[0])
            old=c.coach_portrait;state=c.rng.getstate()
            self.assertEqual(old,c.coach_portrait);self.assertEqual(c.rng.getstate(),state)
            other=next(cl for cl in c.current_league.clubs if cl.uid!=c.club.uid)
            c.agent_offers=[(other.name,c.league_key)];c.accept_transfer(other.name,c.league_key)
            self.assertNotEqual(c.coach_portrait,old);new=c.coach_portrait
            d=CareerMode(access,save_slot='world');self.assertEqual(d.coach_portrait,new)
            self.assertEqual(d.coach_appearance['club'],d.club.uid)

    def test_legacy_and_invalid_appearance_data_never_reset_career(self):
        with tempfile.TemporaryDirectory() as directory,patch.dict(os.environ,STRIKER_SAVE_DIR=directory):
            c=CareerMode(autoload=False);c.accept_starting_offer(c.offers[0]);c.goals=23;c.save()
            for raw in (None,[],dict(club='x',portrait=True),dict(club='x',portrait=10),dict(club='../x',portrait=-1)):
                data=json.loads(c.save_path.read_text());data['career']['coach_appearance']=raw;c.save_path.write_text(json.dumps(data))
                d=CareerMode();self.assertTrue(d.load());self.assertEqual(d.goals,23);self.assertIn(d.coach_portrait,PORTRAITS)
            data=json.loads(c.save_path.read_text());data['career'].pop('coach_appearance');c.save_path.write_text(json.dumps(data))
            d=CareerMode();self.assertTrue(d.load());self.assertEqual(d.goals,23);self.assertIn(d.coach_portrait,PORTRAITS)
