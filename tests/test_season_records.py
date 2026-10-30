import json,sqlite3,tempfile,threading,unittest,http.client
from pathlib import Path
from unittest.mock import patch
from season_records import completed_snapshot,keep_best,valid_record
from server import season_records as server
from server.usage_collector import Collector
from career import CareerMode

class SeasonRecordTests(unittest.TestCase):
    def row(self,**kw):
        r=dict(edition='world',country='Portugal',division=4,season=2026,player='João Silva',team='União Lisboa',matches=38,goals=27);r.update(kw);return r
    def test_best_season_preserves_historical_player_team_and_division(self):
        first=self.row();records=keep_best([],first)
        self.assertEqual(keep_best(records,self.row(goals=10,season=2027,team='Other')),records)
        changed=keep_best(records,self.row(goals=30,season=2027,team='Another Team'))
        self.assertEqual(changed[0]['team'],'Another Team')
        self.assertEqual(len(keep_best(changed,self.row(division=3))),2)
    def test_actual_career_rollover_snapshots_before_reset_and_save_reload(self):
        with tempfile.TemporaryDirectory() as t,patch.dict(__import__('os').environ,STRIKER_SAVE_DIR=t):
            c=CareerMode();c.accept_starting_offer(c.offers[0]);c.set_player_name('João Silva')
            team=c.display_club(c.club);c.goals=23;c.matches=46;c._finish_season()
            self.assertEqual((c.goals,c.matches,c.season),(0,0,2027))
            record=c.completed_records[0];self.assertEqual(record['player'],'João Silva');self.assertEqual(record['team'],team)
            self.assertEqual((record['goals'],record['season'],record['country'],record['division']),(23,2026,'Scorer',1))
            c.save();again=CareerMode();self.assertEqual(again.completed_records,c.completed_records)
            data=json.loads(c.save_path.read_text());data['career'].pop('completed_records');c.save_path.write_text(json.dumps(data));self.assertTrue(again.load());self.assertEqual(again.completed_records,[])
    def test_unicode_names_validation_and_private_best_board_isolation(self):
        with sqlite3.connect(':memory:') as db:
            from server.leaderboard import initialize
            initialize(db);server.initialize(db)
            for changes in ({'goals':True},{'player':'<script>'},{'team':'x\n'},{'matches':0},{'edition':'free'},{'division':-1}):self.assertFalse(valid_record(self.row(**changes)))
            token='a'*64
            for row in (self.row(),self.row(division=3,goals=31),self.row(country='England',goals=40)):
                server.submit(db,dict(token=token,record=row))
            result=server.leaders(db,'world','Portugal',4)
            self.assertEqual(len(result['entries']),1);self.assertEqual(result['entries'][0]['player'],'João Silva')
            server.submit(db,dict(token=token,record=self.row(goals=9,season=2027)))
            self.assertEqual(server.leaders(db,'world','Portugal',4)['entries'][0]['goals'],27)
            self.assertEqual(server.leaders(db,'free','Scorer',1)['entries'],[])
            server.withdraw(db,token);self.assertEqual(server.leaders(db,'world','Portugal',4)['entries'],[])
    def test_legacy_consent_does_not_authorize_name_publication(self):
        from online_leaderboard import Leaderboard
        with tempfile.TemporaryDirectory() as t:
            Path(t,'leaderboard.json').write_text(json.dumps(dict(token='a'*64,alias='Striker-123',enabled=True,origin='https://stats.example.com')))
            b=Leaderboard(t,'https://stats.example.com');self.assertFalse(b.enabled)
            b.enabled=True;b.save();self.assertTrue(Leaderboard(t,b.origin).enabled)
    def test_v2_http_filters_and_legacy_tables_survive(self):
        with tempfile.TemporaryDirectory() as t:
            service=Collector(('127.0.0.1',0),Path(t)/'stats.sqlite','secret')
            worker=threading.Thread(target=service.serve_forever,daemon=True);worker.start()
            def request(method,path,data=None):
                c=http.client.HTTPConnection(*service.server_address,timeout=3)
                c.request(method,path,None if data is None else json.dumps(data),{'Content-Type':'application/json'})
                r=c.getresponse();body=r.read();status=r.status;c.close();return status,body
            try:
                self.assertEqual(request('POST','/v2/records',dict(token='a'*64,record=self.row()))[0],204)
                self.assertEqual(len(json.loads(request('GET','/v2/records?edition=world&country=Portugal&division=4')[1])['entries']),1)
                self.assertEqual(json.loads(request('GET','/v2/records?edition=world&country=Portugal&division=3')[1])['entries'],[])
                self.assertEqual(request('GET','/v2/records?edition=world&country=Portugal&division=x')[0],400)
                self.assertEqual(request('GET','/v1/leaderboard')[0],200)
                self.assertEqual(request('POST','/v2/records/withdraw',{'token':'a'*64})[0],204)
            finally:service.shutdown();service.server_close();worker.join()
    def test_client_never_posts_partial_season_then_retries_saved_record(self):
        from online_leaderboard import Leaderboard
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as t:
            b=Leaderboard(t,'https://stats.example.com');b.enabled=True
            c=SimpleNamespace(completed_records=[],goals=50,matches=20)
            done=threading.Event()
            with patch.object(b,'request',return_value={'schema':2,'entries':[]}) as request:
                b.sync(c,False,done.set);self.assertTrue(done.wait(3));self.assertEqual(request.call_count,1)
            c.completed_records=[self.row(edition='free',country='Scorer',division=1)];done.clear()
            with patch.object(b,'request',return_value={'schema':2,'entries':[]}) as request:
                b.sync(c,False,done.set);self.assertTrue(done.wait(3));self.assertEqual(request.call_args_list[0].args[0],'/v2/records')
                done.clear();b.sync(c,False,done.set);self.assertTrue(done.wait(3));self.assertEqual(request.call_count,3)

    def test_world_season_record_keeps_old_division_when_promoted(self):
        import os,edition
        with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,STRIKER_SAVE_DIR=t),patch('edition.WORLD_BUILD',True):
            c=CareerMode(edition.entitlement_provider(),autoload=False,starter_country='Portugal',save_slot='world')
            c.accept_starting_offer(c.offers[0]);old=c.current_league.tier
            c.club.points=999;c.goals=37;c.matches=40;c._finish_season()
            record=c.completed_records[0]
            self.assertEqual((record['country'],record['division'],record['edition'],record['goals']),('Portugal',old,'world',37))
            self.assertEqual(c.current_league.tier,old-1)
