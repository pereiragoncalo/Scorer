import unittest
from types import SimpleNamespace as NS
from match_moments import late_opportunity, chance_moment, match_stakes, clean_moments, DERBIES, TEXT


class MatchMomentsTests(unittest.TestCase):
    def test_late_chance_preserves_count_order_identity_and_difficulty_index(self):
        changed = 0
        for seed in range(300):
            original = [12, 36, 64]
            result = late_opportunity(original, 4, 102, seed)
            self.assertEqual(original, [12, 36, 64])
            self.assertEqual(result[:2], original[:2])
            self.assertEqual(len(set(result)), 3)
            self.assertEqual(result, sorted(result))
            self.assertTrue(64 <= result[-1] < 102)
            self.assertEqual(result, late_opportunity(original, 4, 102, seed))
            changed += result != original
        self.assertTrue(90 < changed < 180)
        self.assertEqual(late_opportunity([], 1, 92, 'x'), [])
        self.assertEqual(late_opportunity([89], 4, 102, 'x'), [89])

    def test_actual_score_and_home_away_orientation_never_promise_a_winner(self):
        self.assertEqual(chance_moment({}, 85, 0, 1, True), 'equaliser')
        self.assertEqual(chance_moment({}, 85, 1, 0, False), 'equaliser')
        self.assertEqual(chance_moment({}, 88, 2, 2, False), 'lead')
        for score in ((0,2),(2,0)):
            self.assertEqual(chance_moment({}, 88, *score, True), '')
        self.assertEqual(chance_moment({}, 84, 0, 1, True), '')
        self.assertEqual(chance_moment({'kind':'derby'}, 88, 0, 1, True, True), '')
        self.assertEqual(chance_moment({'kind':'final'}, 28, 0, 0, True), 'final')

    def test_exact_final_and_playoff_context_no_semifinal_misclassification(self):
        h,a=NS(uid='h'),NS(uid='a')
        for key, stage, expected in [('cup','Final','final'),('cup','Last 4',''),('playoff:Italy','Final','playoff')]:
            f=dict(id='f',stage=stage,tie='t',leg=1,home='h',away='a',score=None)
            career=NS(world_competitions=NS(tournaments={key:NS(fixtures=[f])}))
            self.assertEqual(match_stakes(career,'world|'+key+'|f',h,a)['kind'],expected)

    def test_two_legs_never_confuse_leg_score_with_aggregate(self):
        first=dict(id='first',stage='Final',tie='t',leg=1,home='a',away='h',score=[3,1])
        second=dict(id='second',stage='Final',tie='t',leg=2,home='h',away='a',score=None)
        career=NS(world_competitions=NS(tournaments={'cup':NS(fixtures=[first,second])}))
        ctx=match_stakes(career,'world|cup|second',NS(uid='h'),NS(uid='a'))
        self.assertEqual(ctx['prior'],(1,3));self.assertFalse(ctx['late_allowed'])
        self.assertEqual(chance_moment(ctx,89,1,1,True),'final')

    def test_derby_uses_uids_not_aliases(self):
        uids=tuple(next(iter(DERBIES)))
        c=NS(world_unlocked=False)
        self.assertEqual(match_stakes(c,'league',NS(uid=uids[0]),NS(uid=uids[1]))['kind'],'derby')
        self.assertEqual(match_stakes(c,'league',NS(uid='other',name='Benfica'),NS(uid='fake',name='Sporting CP'))['kind'],'')

    def test_history_validation_and_legacy_defaults(self):
        self.assertEqual(clean_moments(None),[])
        for e in ({'kind':'x','minute':90,'outcome':'goal'},{'kind':'lead','minute':True,'outcome':'goal'},{'kind':'lead','minute':111,'outcome':'goal'}):
            self.assertEqual(clean_moments([e]),[])
        event=dict(kind='lead',minute=89,outcome='goal',unused='ignored')
        self.assertEqual(clean_moments([event,event]),[dict(kind='lead',minute=89,outcome='goal')])

    def test_survival_is_close_to_actual_direct_drop_line_near_season_end(self):
        from unittest.mock import patch
        rows=[NS(uid=str(i),points=50-i) for i in range(10)]
        league=NS(total_rounds=18,round_index=15,tier=1,country='Test',clubs=rows,table=lambda:rows)
        c=NS(world_unlocked=True,current_league=league,domestic_leagues=lambda country:[NS(tier=1),NS(tier=2)],club=rows[7])
        with patch('domestic_rules.table_zones',return_value=NS(relegation=(8,9,10))):
            self.assertEqual(match_stakes(c,'league',rows[7],rows[4])['kind'],'survival')
            league.round_index=5
            self.assertEqual(match_stakes(c,'league',rows[7],rows[4])['kind'],'')
            league.round_index=15;rows[7].points=0
            self.assertEqual(match_stakes(c,'league',rows[7],rows[4])['kind'],'')
        with patch('domestic_rules.table_zones',return_value=NS(relegation=())):
            self.assertEqual(match_stakes(c,'league',rows[7],rows[4])['kind'],'')

    def test_world_national_moment_history_saved_before_reload_and_sanitized(self):
        import os, tempfile, json
        from unittest.mock import patch
        from career import CareerMode
        access=NS(has_world_access=lambda:True)
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ,STRIKER_SAVE_DIR=directory):
            c=CareerMode(access,autoload=False,starter_country='Brazil',save_slot='world')
            c.accept_starting_offer(c.offers[0]);c.nationality='Argentina';c._ensure_competitions()
            book=c.world_competitions
            f=dict(id='friendly:moment',home='nation:Brazil',away='nation:Argentina',week=0,stage='International friendly',score=None)
            book.friendlies[f['id']]=f
            event=dict(kind='equaliser',minute=89,outcome='goal')
            c.finish_match(c._competition_club(book.nations[f['home']]),c._competition_club(book.nations[f['away']]),1,0,True,(1,1),'world|friendly|'+f['id'],moments=[event])
            d=CareerMode(access,save_slot='world')
            self.assertEqual(d.fixture_history[-1]['moments'],[event])
            self.assertEqual(d.international_goals,1)
            data=json.loads(c.save_path.read_text());data['career']['fixture_history'][-1]['moments']=[dict(kind='lead',minute=-1,outcome='goal')]
            c.save_path.write_text(json.dumps(data));self.assertTrue(d.load());self.assertEqual(d.fixture_history[-1]['moments'],[])
