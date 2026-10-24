"""Release gates, verified ownership, and same-app career preservation."""
import base64
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import uuid
from unittest.mock import patch

from billing import PlayWorldAccess
from career import CareerMode
from tools.play.prepare import validate, prepare
from server.world_licensing import LicenceService, Denied, Unavailable, GooglePlay, application

ROOT = Path(__file__).resolve().parents[1]


class Bridge:
    access = False
    def hasAccess(self, activity): return self.access
    def restore(self, activity): self.access = True
    def purchase(self, activity): pass


class ReleaseTests(unittest.TestCase):
    def config(self): return json.loads((ROOT/'release/play.example.json').read_text())

    def test_production_rejects_missing_identity_ads_and_billing(self):
        config = self.config()
        self.assertFalse(validate(config, 'rehearsal'))
        errors = '\n'.join(validate(config, 'production'))
        for required in ('developer', 'support', 'privacy', 'AdMob', 'World purchase'):
            self.assertIn(required, errors)
        config['billing']['enabled'] = True
        self.assertTrue(validate(config, 'rehearsal'))

    def test_staging_cannot_overwrite_source_or_leak_server_keys_or_saves(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base/'source'; source.mkdir()
            for name in ('assets', 'android', 'tools'): (source/name).mkdir()
            java = source/'android/src/com/clemir/striker'; (java/'ads').mkdir(parents=True); (java/'billing').mkdir()
            (source/'edition.py').write_text('WORLD_PREVIEW = False\n')
            (source/'main.py').write_text('print("game")\n')
            (source/'buildozer.spec').write_bytes((ROOT/'buildozer.spec').read_bytes())
            (source/'assets/private.jks').write_text('must not copy')
            (source/'assets/data').mkdir()
            (source/'assets/data/world_clubs.json').write_text('{"version":1,"clubs":{}}')
            (source/'assets/data/private.json').write_text('must not copy')
            (source/'android/secret.pem').write_text('must not copy')
            (source/'striker_career.json').write_text('must not copy')
            (source/'server').mkdir(); (source/'server/private.py').write_text('must not copy')
            target = prepare(self.config(), base/'stage', 'rehearsal', source)
            names = [str(p.relative_to(target)) for p in target.rglob('*')]
            self.assertFalse(any('private.jks' in n or 'secret.pem' in n or 'striker_career' in n or 'server/' in n for n in names))
            self.assertTrue((target/'assets/data/world_clubs.json').is_file())
            self.assertFalse((target/'assets/data/private.json').exists())
            self.assertIn('package.name = striker', (target/'buildozer.spec').read_text())
            self.assertIn('ENABLED = false', (target/'android/src/com/clemir/striker/billing/BillingConfig.java').read_text())
            with self.assertRaises(ValueError): prepare(self.config(), target, 'rehearsal', source)
            with self.assertRaises(ValueError): prepare(self.config(), source/'nested', 'rehearsal', source)

    def test_world_qa_uses_same_app_separate_slots_and_never_enables_billing(self):
        from tools.prepare_world_qa import prepare_qa
        before=(ROOT/'edition.py').read_bytes()
        with tempfile.TemporaryDirectory() as temp:
            target=prepare_qa(Path(temp)/'owner-qa')
            self.assertIn('WORLD_PREVIEW = True',(target/'edition.py').read_text())
            self.assertIn('package.name = striker',(target/'buildozer.spec').read_text())
            self.assertIn('package.domain = com.clemir',(target/'buildozer.spec').read_text())
            self.assertIn('ENABLED = false',(target/'android/src/com/clemir/striker/billing/BillingConfig.java').read_text())
            self.assertIn('qa-world',(target/'release_settings.py').read_text())
            self.assertTrue((target/'assets/data/world_clubs.json').is_file())
            self.assertFalse((target/'server').exists())
        self.assertEqual((ROOT/'edition.py').read_bytes(),before)

    def test_manifest_gate_rejects_debug_backup_cleartext_and_legacy_companion(self):
        from tools.play.verify import inspect_manifest
        base = '<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.clemir.striker" android:versionCode="1026625"><uses-sdk android:minSdkVersion="26" android:targetSdkVersion="36"/><uses-permission android:name="android.permission.INTERNET"/><uses-permission android:name="com.android.vending.BILLING"/><application android:allowBackup="false" android:usesCleartextTraffic="false"/></manifest>'
        inspect_manifest(base)
        for invalid in (base.replace('allowBackup="false"','allowBackup="true"'),
                        base.replace('usesCleartextTraffic="false"','usesCleartextTraffic="true"'),
                        base.replace('<application ','<application android:debuggable="true" '),
                        base.replace('</manifest>','<queries><package android:name="com.clemir.strikerworld.preview"/></queries></manifest>'),
                        base.replace('</manifest>','<uses-permission android:name="com.google.android.gms.permission.AD_ID"/></manifest>')):
            with self.assertRaises(ValueError): inspect_manifest(invalid)

    def test_provider_is_fail_closed_and_never_changes_mid_match(self):
        bridge = Bridge(); provider = PlayWorldAccess(bridge)
        provider.purchase()
        self.assertFalse(provider.has_world_access())
        provider.restore()
        self.assertTrue(provider.verified_now())
        self.assertFalse(provider.has_world_access())
        self.assertTrue(PlayWorldAccess(bridge).has_world_access())
        bridge.access = 'true'
        self.assertFalse(PlayWorldAccess(bridge).has_world_access())

    def test_world_uses_its_own_slot_and_never_copies_the_free_career(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, STRIKER_SAVE_DIR=temp):
            free = CareerMode(autoload=False, save_slot='free')
            free.accept_starting_offer(free.offers[0]);free.player_name='Free Player';free.goals=7;free.save()
            before=free.save_path.read_bytes()
            bridge=Bridge();bridge.access=True
            world=free.new_world_career(PlayWorldAccess(bridge), 'Brazil')
            self.assertNotEqual(world.save_path,free.save_path)
            self.assertEqual((world.club_name,world.goals,world.matches),('',0,0))
            self.assertFalse(world.save_path.exists())
            world.set_player_name('World Player');world.accept_starting_offer(world.offers[0]);world.goals=3;world.save()
            self.assertEqual(free.save_path.read_bytes(),before)
            loaded=CareerMode(PlayWorldAccess(bridge),save_slot='world')
            self.assertEqual((loaded.player_name,loaded.goals),('World Player',3))
            self.assertEqual(CareerMode(save_slot='free').goals,7)
            self.assertFalse(CareerMode(PlayWorldAccess(bridge), save_slot='free').world_unlocked)
            world_before=world.save_path.read_bytes()
            self.assertTrue(world.backup_before_new_game())
            self.assertTrue(world.save_path.with_suffix('.previous.json').exists())
            self.assertFalse(free.save_path.with_suffix('.previous.json').exists())
            denied=CareerMode(autoload=False,save_slot='world')
            self.assertFalse(denied.save())
            self.assertEqual(world.save_path.read_bytes(),world_before)

    def test_world_slot_rejects_a_copied_free_save(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, STRIKER_SAVE_DIR=temp):
            free=CareerMode(autoload=False,save_slot='free');free.accept_starting_offer(free.offers[0]);free.goals=99;free.save()
            bridge=Bridge();bridge.access=True
            world=CareerMode(PlayWorldAccess(bridge),autoload=False,save_slot='world')
            world.save_path.write_bytes(free.save_path.read_bytes())
            self.assertFalse(world.load())
            self.assertEqual((world.club_name,world.goals),('',0))

    def test_unverified_or_invalid_slot_cannot_open_or_migrate_world(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, STRIKER_SAVE_DIR=temp):
            free=CareerMode(autoload=False);free.accept_starting_offer(free.offers[0]);free.save()
            before=free.save_path.read_bytes()
            with self.assertRaises(ValueError): free.new_world_career(PlayWorldAccess(Bridge()))
            with self.assertRaises(ValueError): CareerMode(save_slot='../other')
            self.assertEqual(free.save_path.read_bytes(),before)



class LicensingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from cryptography.hazmat.primitives.asymmetric import rsa
        cls.key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    def request(self):
        return {'package': 'com.clemir.striker', 'product':'scorer_world_upgrade',
                'purchase_token':'a_valid_private_token_123456789', 'installation':str(uuid.uuid4()), 'nonce':str(uuid.uuid4())}

    def service(self, result=None, ack_fails=False):
        state = result if result is not None else {'purchaseState':0,'consumptionState':0,'acknowledgementState':0}
        class FakeGoogle:
            acknowledgements=0
            def get(self, token): return state
            def acknowledge(self, token):
                self.acknowledgements += 1
                if ack_fails: raise Unavailable()
        return LicenceService(FakeGoogle(), self.key, clock=lambda: 1000000)

    def test_verified_purchased_token_acknowledged_and_signed_for_installation_and_nonce(self):
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        service = self.service(); request = self.request(); receipt = service.issue(request)
        payload = base64.b64decode(receipt['payload']); signature = base64.b64decode(receipt['signature'])
        self.key.public_key().verify(signature, payload, padding.PKCS1v15(), hashes.SHA256())
        data=json.loads(payload)
        for key in ('package','product','installation','nonce'): self.assertEqual(data[key],request[key])
        self.assertEqual(data['expires_at']-data['issued_at'],7*24*3600)
        self.assertNotIn(request['purchase_token'],json.dumps(receipt))
        self.assertEqual(service.google.acknowledgements,1)
        with self.assertRaises(Exception): self.key.public_key().verify(signature,payload+b' ',padding.PKCS1v15(),hashes.SHA256())

    def test_pending_refunded_consumed_invalid_and_test_payments_never_grant(self):
        valid={'purchaseState':0,'consumptionState':0,'acknowledgementState':1}
        for delta in ({'purchaseState':1},{'purchaseState':2},{'purchaseState':False},
                      {'consumptionState':1},{'acknowledgementState':False},{'purchaseType':0},
                      {'purchaseType':2},{'quantity':2}):
            with self.subTest(delta=delta), self.assertRaises(Denied):
                self.service(valid|delta).issue(self.request())
        with self.assertRaises(Unavailable): self.service(ack_fails=True).issue(self.request())

    def test_invalid_request_never_calls_google(self):
        for key, value in [('package','other.app'),('product','coins'),('purchase_token','x'),('nonce','bad')]:
            data=self.request();data[key]=value
            service=self.service()
            with self.assertRaises(ValueError): service.issue(data)
            self.assertEqual(service.google.acknowledgements,0)

    def test_missing_service_identity_is_unavailable_not_a_client_error(self):
        body=json.dumps(self.request()).encode(); statuses=[]
        env={'REQUEST_METHOD':'POST','PATH_INFO':'/v1/world/verify','CONTENT_LENGTH':str(len(body)),
             'CONTENT_TYPE':'application/json','wsgi.input':io.BytesIO(body)}
        with patch('server.world_licensing._service',None), patch('server.world_licensing.load_service',side_effect=KeyError('missing secret selector')):
            payload=b''.join(application(env,lambda status,headers:statuses.append(status)))
        self.assertEqual(statuses,['503 Service Unavailable'])
        self.assertNotIn(b'secret',payload)

    def test_wsgi_limits_schema_and_does_not_expose_tokens_in_errors(self):
        request=self.request(); body=json.dumps(request).encode();statuses=[]
        env={'REQUEST_METHOD':'POST','PATH_INFO':'/v1/world/verify','CONTENT_LENGTH':str(len(body)),
             'CONTENT_TYPE':'application/json','wsgi.input':io.BytesIO(body)}
        with patch('server.world_licensing._service',self.service(ack_fails=True)):
            payload=b''.join(application(env,lambda status,headers:statuses.append(status)))
        self.assertEqual(statuses,['503 Service Unavailable'])
        self.assertNotIn(request['purchase_token'].encode(),payload)
        env['CONTENT_LENGTH']='9000';statuses.clear()
        application(env,lambda status,headers:statuses.append(status))
        self.assertEqual(statuses,['400 Bad Request'])


if __name__ == '__main__': unittest.main()
