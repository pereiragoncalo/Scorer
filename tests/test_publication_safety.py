import copy,http.client,json,os,sqlite3,tempfile,threading,unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
from online_safety import FamilyControls
from anonymous_stats import create_statistics
from career import CareerMode
from career_transfer import export_career,import_career,validated_import
from server.usage_collector import Collector
from server import moderation
from server.maintenance import backup,maintain

class FamilyTests(unittest.TestCase):
    def test_unknown_child_cannot_enable_and_birth_not_stored(self):
        with tempfile.TemporaryDirectory() as t:
            f=FamilyControls(t);self.assertFalse(f.social);self.assertFalse(f.notice_seen)
            self.assertFalse(f.configure(date.today().isoformat(),'123456','123456'))
            self.assertFalse(f.configure('1990-01-01','123','123'))
            self.assertFalse(f.configure('1990-01-01','123456','654321'))
            self.assertTrue(f.configure('1990-01-01','123456','123456'))
            raw=f.path.read_text();self.assertNotIn('1990-01-01',raw);self.assertNotIn('123456',raw)
            self.assertTrue(FamilyControls(t).social)
    def test_pin_lockout_survives_restart_and_wrong_pin_does_not_enable(self):
        with tempfile.TemporaryDirectory() as t:
            f=FamilyControls(t,clock=lambda:1000);f.configure('1990-01-01','123456','123456')
            self.assertTrue(f.set_social(False,'123456'))
            for _ in range(3):self.assertFalse(f.unlock('654321'))
            again=FamilyControls(t,clock=lambda:1001);self.assertFalse(again.unlock('123456'));self.assertFalse(again.social)
            after=FamilyControls(t,clock=lambda:1301);self.assertTrue(after.set_social(True,'123456'))
    def test_optional_delivery_requires_choice_and_notice(self):
        with tempfile.TemporaryDirectory() as t:
            u=create_statistics(False,t,endpoint='https://stats.example.com/v1/usage');u.begin_session();u._sender=lambda *_:self.fail('Sent before notice')
            self.assertFalse(u.enabled);self.assertFalse(u.delivery_ready);self.assertFalse(u.flush_async());self.assertTrue(u.set_enabled(True));self.assertFalse(u.flush_async());self.assertTrue(u.set_enabled(False))
            f=FamilyControls(t);f.acknowledge();self.assertFalse(create_statistics(False,t,endpoint='').delivery_ready)

class TransferTests(unittest.TestCase):
    def test_real_roundtrip_backup_and_no_credentials_exported(self):
        with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,STRIKER_SAVE_DIR=t):
            c=CareerMode(autoload=False,save_slot='free');c.accept_starting_offer(c.offers[0]);c.set_player_name('My Player');c.goals=9;c.save()
            text=export_career(c);self.assertNotIn('"token":',text);self.assertNotIn('pin_hash',text)
            c.goals=20;c.save();before=c.save_path.read_bytes();import_career(c,text)
            self.assertEqual(c.goals,9);self.assertEqual(c.save_path.with_suffix('.previous.json').read_bytes(),before)
            self.assertEqual(CareerMode(autoload=True,save_slot='free').goals,9)
    def test_bad_imports_and_world_boundary_leave_save_and_live_state_untouched(self):
        with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,STRIKER_SAVE_DIR=t):
            c=CareerMode(autoload=False,save_slot='free');c.accept_starting_offer(c.offers[0]);c.goals=7;c.save();before=c.save_path.read_bytes();good=json.loads(export_career(c))
            other=copy.deepcopy(good);other['edition']='WORLD'
            invalid=copy.deepcopy(good);invalid['save']['career']['clubs']='bad'
            for text in ('[]','{bad',json.dumps(other),json.dumps(invalid)):
                with self.assertRaises(ValueError):import_career(c,text)
                self.assertEqual(c.goals,7);self.assertEqual(c.save_path.read_bytes(),before)
    def test_world_roundtrip_and_failed_write_is_atomic(self):
        import edition
        with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,STRIKER_SAVE_DIR=t),patch('edition.WORLD_BUILD',True):
            c=CareerMode(edition.entitlement_provider(),autoload=False,starter_country='Portugal',save_slot='world');c.accept_starting_offer(c.offers[0]);c.goals=11;c.save()
            text=export_career(c);self.assertEqual(validated_import(c,text).goals,11)
            before=c.save_path.read_bytes()
            with patch.object(CareerMode,'save',return_value=False):
                with self.assertRaises(OSError):import_career(c,text)
            self.assertEqual(c.save_path.read_bytes(),before)

class ModerationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.service=Collector(('127.0.0.1',0),self.root/'data.sqlite','owner-secret',self.root/'public.json')
        self.thread=threading.Thread(target=self.service.serve_forever,daemon=True);self.thread.start()
        self.row=dict(edition='free',country='Scorer',division=1,season=2026,player='Safe Nickname',team='Test Team',matches=46,goals=20)
    def tearDown(self):self.service.shutdown();self.service.server_close();self.thread.join();self.temp.cleanup()
    def req(self,method,path,data=None,admin=False):
        c=http.client.HTTPConnection(*self.service.server_address,timeout=3);h={'Content-Type':'application/json'}
        if admin:h['Authorization']='Bearer owner-secret'
        c.request(method,path,None if data is None else json.dumps(data),h);r=c.getresponse();body=r.read();status=r.status;c.close()
        try:body=json.loads(body)
        except ValueError:pass
        return status,body
    def submit(self,**changes):
        row=dict(self.row);row.update(changes)
        return self.req('POST','/v3/records',dict(token='a'*64,record=row,terms_version=1))
    def board(self):return self.req('GET','/v3/records?edition=free&country=Scorer&division=1')[1]['entries']
    def test_pending_approval_public_ids_no_tokens_and_report_block_ban(self):
        self.assertEqual(self.submit()[0],204);self.assertEqual(self.board(),[])
        q=self.req('GET','/v1/moderation',admin=True)[1];publisher=q['entries'][0]['publisher']
        self.assertNotIn('a'*64,json.dumps(q));self.assertEqual(len(publisher),32)
        self.assertEqual(self.req('POST','/v1/moderation',dict(publisher=publisher,action='approve'),True)[0],204)
        self.assertEqual(len(self.board()),1);self.assertEqual(self.board()[0]['publisher'],publisher)
        from online_leaderboard import Leaderboard,valid_public_entry
        self.assertTrue(valid_public_entry(self.board()[0]))
        b=Leaderboard(self.root/'client');b.entries=self.board();self.assertTrue(b.block(publisher));self.assertFalse(b.entries);self.assertIn(publisher,Leaderboard(self.root/'client').blocked)
        self.assertEqual(self.req('POST','/v3/reports',dict(token='b'*64,publisher=publisher,reason='abuse'))[0],204)
        self.assertEqual(self.req('GET','/v1/moderation',admin=True)[1]['reports'][0]['count'],1)
        self.assertEqual(self.req('POST','/v1/moderation',dict(publisher=publisher,action='ban'),True)[0],204)
        self.assertFalse(self.board());self.assertEqual(self.submit(goals=21)[0],403)
    def test_terms_legacy_bypass_admin_auth_and_reapproval_after_change(self):
        self.assertEqual(self.req('POST','/v2/records',dict(token='a'*64,record=self.row))[0],426)
        self.assertEqual(self.req('POST','/v3/records',dict(token='a'*64,record=self.row,terms_version=0))[0],400)
        self.assertEqual(self.req('GET','/v1/moderation')[0],404)
        self.assertEqual(self.submit()[0],204);publisher=self.req('GET','/v1/moderation',admin=True)[1]['entries'][0]['publisher']
        self.assertEqual(self.req('POST','/v1/moderation',dict(publisher=publisher,action='approve'))[0],404)
        self.req('POST','/v1/moderation',dict(publisher=publisher,action='approve'),True);self.assertEqual(len(self.board()),1)
        self.submit(goals=22,player='Another Nickname');self.assertFalse(self.board())
    def test_withdraw_removes_reports_and_pending_legacy_tables(self):
        self.submit();publisher=self.req('GET','/v1/moderation',admin=True)[1]['entries'][0]['publisher']
        self.req('POST','/v3/reports',dict(token='b'*64,publisher=publisher,reason='personal_info'))
        self.assertEqual(self.req('POST','/v3/records/withdraw',dict(token='a'*64))[0],204)
        q=self.req('GET','/v1/moderation',admin=True)[1];self.assertFalse(q['entries']);self.assertFalse(q['reports'])
    def test_aggregate_only_backup_and_retention_without_new_posts(self):
        self.submit()
        with self.service.db() as db:
            db.execute("INSERT INTO totals VALUES('2000-01-01','sessions',1)");db.execute("INSERT INTO totals VALUES(?,'sessions',2)",(date.today().isoformat(),))
        target=self.root/'backup.sqlite';backup(self.service.database,target)
        with sqlite3.connect(target) as db:
            dump='\n'.join(db.iterdump());self.assertNotIn('Safe Nickname',dump);self.assertNotIn('season_records',dump)
        self.assertEqual(self.req('GET','/v1/totals',admin=True)[1]['totals'],[dict(day=date.today().isoformat(),event='sessions',count=2)])
    def test_public_policy_requires_completed_configuration_and_escapes_content(self):
        self.assertEqual(self.req('GET','/privacy')[0],503)
        d=dict(developer_name='<Test Owner>',support_email='support@example.com',effective_date='2026-10-31',legal_basis='Reviewed legal basis for this test',provider_practices='Test only',children_practices='Test only',international_transfers='Test only')
        (self.root/'public.json').write_text(json.dumps(d))
        status,body=self.req('GET','/privacy');self.assertEqual(status,200);self.assertIn(b'&lt;Test Owner&gt;',body);self.assertNotIn(b'<Test Owner>',body)
        self.assertEqual(self.req('GET','/terms')[0],200);self.assertEqual(self.req('GET','/delete')[0],200)

class ModerationPagingTests(unittest.TestCase):
    def test_all_pending_entries_remain_reachable_and_legacy_names_need_reconsent(self):
        from server import season_records as records
        with tempfile.TemporaryDirectory() as t:
            service=Collector(('127.0.0.1',0),Path(t)/'data.sqlite')
            try:
                with service.db() as db:
                    row=dict(edition='free',country='Scorer',division=1,season=2026,player='Legacy Name',team='Team',matches=46,goals=20)
                    for number in range(205):records.submit(db,dict(token=('%064x'%number),record=row))
                    moderation.initialize(db)
                    self.assertEqual(moderation.queue(db,0)['total'],205)
                    self.assertEqual(len(moderation.queue(db,200)['entries']),5)
                    self.assertEqual(moderation.leaders(db,'free','Scorer',1)['entries'],[])
                    changed=dict(row,player='Reconfirmed Nickname')
                    moderation.submit(db,dict(token='0'*64,record=changed,terms_version=1))
                    publisher=moderation.public_id(records.identity('0'*64))
                    moderation.moderate(db,dict(publisher=publisher,action='approve'))
                    self.assertEqual(moderation.leaders(db,'free','Scorer',1)['entries'][0]['player'],'Reconfirmed Nickname')
            finally:service.server_close()

class StagingTests(unittest.TestCase):
    def test_world_only_production_launch_keeps_editor_and_free_cannot_be_staged_for_play(self):
        from tools.prepare_editions import prepare_edition
        from tools.play.publication import validate_publication
        from tools.play.prepare import ROOT
        import configparser
        config=json.loads((ROOT/'release/play.example.json').read_text());config['version_code']=1030000
        self.assertTrue(validate_publication(None));self.assertTrue(validate_publication({}))
        review={k:True for k in ('automatic_usage_legal_review','children_social_review','moderation_operator_ready','public_policy_live','cloudflare_practices_reviewed')};review['legal_basis']='Synthetic test review only, not an actual legal approval'
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError):prepare_edition('world',Path(t)/'unreviewed',channel='production',config=config)
            with self.assertRaisesRegex(ValueError,'Only Scorer World'):prepare_edition('free',Path(t)/'free',channel='production',config=config,publication=review)
            with self.assertRaisesRegex(ValueError,'above the 0.9'):
                prepare_edition('world',Path(t)/'stale-code',channel='production',config=dict(config,version_code=1026906),publication=review)
            stage=prepare_edition('world',Path(t)/'world',channel='production',config=config,publication=review)
            spec=configparser.ConfigParser();spec.read(stage/'buildozer.spec')
            self.assertEqual(spec['app']['package.name'],'scorerworld')
            self.assertEqual(spec['app']['version'],'1.0');self.assertEqual(spec['app']['android.numeric_version'],'1030000')
            default_stage=prepare_edition('world',Path(t)/'production-default',channel='production',publication=review)
            default_spec=configparser.ConfigParser();default_spec.read(default_stage/'buildozer.spec')
            self.assertEqual(default_spec['app']['version'],'1.0');self.assertEqual(default_spec['app']['android.numeric_version'],str(json.loads((ROOT/'release/play.production.example.json').read_text())['version_code']))
            ns={};exec((stage/'release_settings.py').read_text(),ns)
            self.assertEqual(ns['VERSION_NAME'],'1.0')
            self.assertEqual(ns['CHANNEL'],'production');self.assertEqual(ns['SUPPORT_EMAIL'],'goncalo@clemir.com');self.assertFalse(ns['WORLD_LISTING_READY'])
            e={};exec((stage/'edition.py').read_text(),e);self.assertTrue(e['WORLD_BUILD']);self.assertFalse(e['WORLD_PREVIEW'])
            self.assertTrue((stage/'name_packs.py').is_file());self.assertTrue((stage/'android/worldsrc/com/clemir/striker/files/LocalNameFiles.java').is_file())
            self.assertNotIn('android.gradle_dependencies',spec['app']);self.assertFalse((stage/'server').exists())
