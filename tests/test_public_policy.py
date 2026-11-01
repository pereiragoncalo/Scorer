"""Public legal-document content, transparency and policy-only deployment safety."""
import json,os,stat,tempfile,threading,http.client,unittest
from pathlib import Path
from unittest.mock import Mock
from server.public_pages import page,load_config,TERMS_PT
from server.install_public_policy import apply,check,ROOT,FILES
from server.usage_collector import Collector
from online_safety import TERMS_TEXT
from tools.play.publication import validate_publication

class PublicPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.config=self.root/'public.json'
        self.data=json.loads((ROOT/'server/public.policy.review.json').read_text());self.write(self.data)
    def tearDown(self):self.temp.cleanup()
    def write(self,data):self.config.write_text(json.dumps(data,ensure_ascii=False),encoding='utf8')
    def test_complete_review_facts_render_bilingual_and_explicit_draft(self):
        d=load_config(self.config);self.assertEqual(d['publication_status'],'draft')
        status,body=page('/privacy',self.config);text=body.decode();self.assertEqual(status,200)
        for expected in ('data-publication-status="draft"','PROPOSTA EM REVISÃO','DRAFT UNDER REVIEW','goncalo@clemir.com','Gonçalo Pereira','lang="pt-PT"','lang="en"','não constitui consentimento','is not consent'):
            self.assertIn(expected,text)
        self.assertNotIn('Operator review pending',text);self.assertNotIn('[OWNER',text)
    def test_terms_and_removal_are_available_with_identity_before_privacy_finalization(self):
        self.write(dict(developer_name='Gonçalo Pereira',support_email='goncalo@clemir.com'))
        for path in ('/terms','/delete'):
            status,body=page(path,self.config);self.assertEqual(status,200);self.assertIn(b'mailto:goncalo@clemir.com',body)
        self.assertEqual(page('/privacy',self.config)[0],503)
    def test_legacy_configuration_is_available_but_missing_status_does_not_imply_final_review(self):
        data=dict(self.data);data.pop('publication_status');self.write(data)
        status,body=page('/privacy',self.config);self.assertEqual(status,200);self.assertIn(b'data-publication-status="draft"',body)
    def test_explicit_completed_policy_has_no_draft_banner(self):
        self.write(dict(self.data,publication_status='published'))
        status,body=page('/privacy',self.config);self.assertEqual(status,200);self.assertIn(b'data-publication-status="published"',body);self.assertNotIn(b'DRAFT UNDER REVIEW',body)
    def test_malformed_missing_and_oversized_configuration_fail_closed(self):
        for value in ([],{},None,dict(self.data,support_email='invalid'),dict(self.data,publication_status='approved-by-google'),dict(self.data,legal_basis=''),dict(self.data,legal_basis_en=4)):
            self.write(value);self.assertEqual(page('/privacy',self.config)[0],503)
        self.config.write_text('x'*65537);self.assertEqual(page('/privacy',self.config)[0],503)
        self.config.unlink();self.assertEqual(page('/privacy',self.config)[0],503)
        self.assertEqual(page('/unknown',self.config)[0],404)
    def test_operator_text_is_escaped_and_public_pages_use_no_javascript(self):
        self.write(dict(self.data,developer_name='<script>alert(1)</script>',legal_basis='<img src=x onerror=alert(1)>'))
        text=page('/privacy',self.config)[1].decode();self.assertNotIn('<script>',text);self.assertIn('&lt;script&gt;',text);self.assertNotIn('<img',text)
        for path in ('/privacy','/terms','/delete'):self.assertNotIn(b'<script',page(path,self.config)[1])
    def test_terms_match_the_existing_portuguese_app_catalogue(self):
        catalogue=json.loads((ROOT/'assets/i18n/pt.json').read_text());self.assertEqual(catalogue[TERMS_TEXT],TERMS_PT)
    def test_draft_does_not_complete_production_review_flags(self):
        review=json.loads((ROOT/'release/publication.example.json').read_text());self.assertTrue(validate_publication(review))
        self.assertIs(review['automatic_usage_legal_review'],False);self.assertIs(review['public_policy_live'],False)
    def test_real_http_routes_and_private_totals_stay_private(self):
        service=Collector(('127.0.0.1',0),self.root/'data.sqlite','test-only-admin',self.config)
        thread=threading.Thread(target=service.serve_forever,daemon=True);thread.start()
        try:
            for path in ('/privacy','/terms','/delete','/health','/v1/totals'):
                client=http.client.HTTPConnection(*service.server_address,timeout=3);client.request('GET',path);r=client.getresponse();body=r.read();client.close()
                self.assertEqual(r.status,404 if path=='/v1/totals' else 200)
                if path=='/privacy':self.assertIn(b'data-publication-status="draft"',body)
            with service.db() as db:self.assertEqual(db.execute('SELECT COUNT(*) FROM totals').fetchone()[0],0)
        finally:service.shutdown();service.server_close();thread.join()

class PolicyDeploymentTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.target=Path(self.temp.name);(self.target/'server').mkdir()
        for name in ('public_pages.py','configure_public.py','usage_collector.py'):(self.target/'server'/name).write_text('# original '+name)
        self.config=ROOT/'server/public.policy.review.json'
    def tearDown(self):self.temp.cleanup()
    def test_only_public_files_change_and_service_is_verified(self):
        sentinel=self.target/'online.env';sentinel.write_text('private test sentinel');sentinel.chmod(0o600)
        database=self.target/'online.sqlite';database.write_bytes(b'not touched')
        stop,start,verify=Mock(),Mock(),Mock()
        apply(ROOT,self.config,self.target,stop,start,verify)
        stop.assert_called_once();start.assert_called_once();verify.assert_called_once()
        self.assertEqual(sentinel.read_text(),'private test sentinel');self.assertEqual(stat.S_IMODE(sentinel.stat().st_mode),0o600);self.assertEqual(database.read_bytes(),b'not touched')
        self.assertEqual(load_config(self.target/'public.json')['publication_status'],'draft');self.assertEqual(stat.S_IMODE((self.target/'public.json').stat().st_mode),0o644)
    def test_failed_running_service_check_restores_previous_renderer_and_configuration(self):
        original={name:(self.target/name).read_bytes() for name in FILES[:-1]}
        (self.target/'public.json').write_text('{invalid old config')
        stop,start=Mock(),Mock();verify=Mock(side_effect=RuntimeError('test failure'))
        with self.assertRaises(RuntimeError):apply(ROOT,self.config,self.target,stop,start,verify)
        self.assertEqual(stop.call_count,2);self.assertEqual(start.call_count,2)
        for name,data in original.items():self.assertEqual((self.target/name).read_bytes(),data)
        self.assertEqual((self.target/'public.json').read_text(),'{invalid old config')
    def test_failed_update_removes_new_config_that_did_not_exist_previously(self):
        with self.assertRaises(RuntimeError):apply(ROOT,self.config,self.target,Mock(),Mock(),Mock(side_effect=RuntimeError()))
        self.assertFalse((self.target/'public.json').exists())
    def test_refuses_to_replace_a_completed_policy_or_follow_symlinks(self):
        data=json.loads(self.config.read_text());data['publication_status']='published';(self.target/'public.json').write_text(json.dumps(data))
        stop=Mock()
        with self.assertRaises(ValueError):apply(ROOT,self.config,self.target,stop,Mock(),Mock())
        stop.assert_not_called()
        data.pop('publication_status');(self.target/'public.json').write_text(json.dumps(data))
        with self.assertRaises(ValueError):apply(ROOT,self.config,self.target,stop,Mock(),Mock())
        stop.assert_not_called();(self.target/'public.json').unlink()
        original=self.target/'original.py';original.write_text('keep');p=self.target/'server/public_pages.py';p.unlink();p.symlink_to(original)
        with self.assertRaises(ValueError):apply(ROOT,self.config,self.target,stop,Mock(),Mock())
        self.assertEqual(original.read_text(),'keep')
