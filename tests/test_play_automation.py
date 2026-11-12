"""Local fixtures only. Never contacts Google or uses owner signing/API credentials."""
import base64,copy,hashlib,json,os,shutil,ssl,subprocess,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError
from tools.play import bastion_play_internal as p

class FakeClient:
 def __init__(self,track=None,bundles=None,fail=None):
  self.track=copy.deepcopy(track or {'track':'internal','releases':[{'status':'completed','versionCodes':['1030001']}]});self.bundles=bundles or [];self.calls=[];self.fail=fail
 def api(self,method,url,body=None):
  self.calls.append((method,url,copy.deepcopy(body)))
  if self.fail and self.fail in url:raise p.APIError(400,'Fixture failure')
  if method=='POST' and url==p.BASE:return {'id':'fixture-edit'}
  if method=='DELETE':return {}
  if url.endswith('/tracks/internal'):
   if method=='PUT':self.track=body
   return copy.deepcopy(self.track)
  if url.endswith('/bundles'):return {'bundles':self.bundles}
  return {'id':'fixture-edit'}

class PublisherTests(unittest.TestCase):
 def test_publish_only_internal_validates_then_commits_without_cancelling_review(self):
  client=FakeClient()
  with patch.object(p,'upload',return_value={'versionCode':p.VERSION,'sha256':'abc'}):self.assertEqual(p.publish(client,Path('fixture'),'abc'),'committed')
  methods=[(method,url) for method,url,_ in client.calls]
  put=next(body for method,url,body in client.calls if method=='PUT')
  self.assertEqual(put['track'],'internal');self.assertEqual(put['releases'][0]['versionCodes'],['1030008'])
  self.assertEqual(put['releases'][0]['status'],'completed')
  self.assertTrue(methods[-2][1].endswith(':validate'));self.assertIn(':commit?',methods[-1][1])
  self.assertNotIn('changesNotSentForReview',methods[-1][1]);self.assertIn('ERROR_IF_IN_REVIEW',methods[-1][1])
  self.assertFalse(any('/production' in url for _,url in methods))
 def test_check_only_does_not_upload_update_validate_or_commit(self):
  client=FakeClient()
  with patch.object(p,'upload') as upload:
   self.assertEqual(p.publish(client,None,'',True),'checked');upload.assert_not_called()
  self.assertEqual([m for m,_,_ in client.calls],['POST','GET','DELETE'])
 def test_validation_failure_cleans_edit_without_commit(self):
  client=FakeClient(fail=':validate')
  with patch.object(p,'upload',return_value={'versionCode':p.VERSION,'sha256':'abc'}),self.assertRaises(p.APIError):p.publish(client,Path('fixture'),'abc')
  self.assertEqual(client.calls[-1][0],'DELETE');self.assertFalse(any(':commit' in u for _,u,_ in client.calls))
 def test_already_committed_same_bundle_is_idempotent(self):
  client=FakeClient(track={'track':'internal','releases':[{'versionCodes':['1030008'],'status':'completed'}]},bundles=[{'versionCode':p.VERSION,'sha256':'abc'}])
  with patch.object(p,'upload') as upload:self.assertEqual(p.publish(client,Path('fixture'),'abc'),'unchanged');upload.assert_not_called()
  self.assertFalse(any(m=='PUT' or ':commit' in u for m,u,_ in client.calls))
 def test_existing_version_other_hash_cannot_be_reused(self):
  client=FakeClient(bundles=[{'versionCode':p.VERSION,'sha256':'other'}])
  with self.assertRaisesRegex(p.Stop,'another SHA256'):p.publish(client,Path('fixture'),'abc')
  self.assertEqual(client.calls[-1][0],'DELETE')
 def test_newer_internal_release_cannot_be_downgraded(self):
  client=FakeClient(track={'releases':[{'versionCodes':['1030009']}]})
  with self.assertRaisesRegex(p.Stop,'newer'):p.publish(client,Path('fixture'),'abc')
 def test_google_wrong_version_or_hash_never_reaches_track_update(self):
  for result in ({'versionCode':p.VERSION-1,'sha256':'abc'},{'versionCode':p.VERSION,'sha256':'wrong'}):
   client=FakeClient()
   with patch.object(p,'upload',return_value=result),self.assertRaisesRegex(p.Stop,'differs'):p.publish(client,Path('fixture'),'abc')
   self.assertFalse(any(m=='PUT' for m,_,_ in client.calls))
 def test_commit_timeout_is_not_retried_or_deleted_as_if_unpublished(self):
  client=FakeClient();original=client.api
  def lose(method,url,body=None):
   if ':commit?' in url:client.calls.append((method,url,body));raise URLError('fixture disconnect')
   return original(method,url,body)
  client.api=lose
  with patch.object(p,'upload',return_value={'versionCode':p.VERSION,'sha256':'abc'}),self.assertRaisesRegex(p.Stop,'outcome uncertain'):p.publish(client,Path('fixture'),'abc')
  self.assertEqual(sum(':commit?' in u for _,u,_ in client.calls),1);self.assertNotEqual(client.calls[-1][0],'DELETE')
 def test_review_rejection_is_not_retried_with_safety_flags_removed(self):
  client=FakeClient(fail=':commit?')
  with patch.object(p,'upload',return_value={'versionCode':p.VERSION,'sha256':'abc'}),self.assertRaises(p.APIError):p.publish(client,Path('fixture'),'abc')
  self.assertEqual(sum(':commit?' in u for _,u,_ in client.calls),1)

 def test_automatic_review_mode_accepts_commit_without_unsupported_parameter(self):
  client=FakeClient(bundles=[{'versionCode':p.VERSION,'sha256':'abc'}]);original=client.api
  def google_mode(method,url,body=None):
   if ':commit?' in url and 'changesNotSentForReview' in url:
    raise p.APIError(400,'Changes are sent for review automatically. The query parameter changesNotSentForReview must not be set.')
   return original(method,url,body)
  client.api=google_mode
  with patch.object(p,'upload') as upload:
   self.assertEqual(p.publish(client,Path('fixture'),'abc'),'committed');upload.assert_not_called()
  commit=next(u for _,u,_ in client.calls if ':commit?' in u)
  self.assertIn('ERROR_IF_IN_REVIEW',commit)

class ResumableTests(unittest.TestCase):
 def test_chunking_and_acknowledged_offsets(self):
  with tempfile.TemporaryDirectory() as directory:
   path=Path(directory)/'fixture';path.write_bytes(b'1234567890');calls=[]
   class Client:
    def request(self,method,url,body,headers,accepted):
     calls.append((method,url,body,headers))
     if method=='POST':return 200,{'Location':'https://androidpublisher.googleapis.com/session/fixture'},{}
     start=int(headers['Content-Range'].split()[1].split('-')[0]);end=start+len(body)
     return (200,{},dict(versionCode=p.VERSION,sha256='abc')) if end==10 else (308,{'Range':'bytes=0-'+str(end-1)},{})
   with patch.object(p,'CHUNK',4):self.assertEqual(p.upload(Client(),'e',path)['versionCode'],p.VERSION)
   self.assertEqual([len(body) for method,_,body,_ in calls if method=='PUT'],[4,4,2])
   self.assertIn('/resumable/upload/',calls[0][1]);self.assertEqual(calls[-1][3]['Content-Range'],'bytes 8-9/10')
 def test_lost_ack_queries_offset_before_continuing(self):
  with tempfile.TemporaryDirectory() as directory:
   path=Path(directory)/'fixture';path.write_bytes(b'abcdefgh');requests=[]
   class Client:
    def request(self,method,url,body,headers,accepted):
     if method=='POST':return 200,{'Location':'https://androidpublisher.googleapis.com/session/fixture'},{}
     requests.append(headers['Content-Range'])
     if len(requests)==1:raise URLError('lost ACK')
     if headers['Content-Range']=='bytes */8':return 308,{'Range':'bytes=0-3'},{}
     return 200,{},dict(versionCode=p.VERSION,sha256='abc')
   with patch.object(p,'CHUNK',4):p.upload(Client(),'e',path)
   self.assertEqual(requests,['bytes 0-3/8','bytes */8','bytes 4-7/8'])
 def test_untrusted_upload_location_cannot_receive_google_token(self):
  client=p.Client({'private_key':'fixture'});client.token='fixture-bearer';client.expires=10**12
  with patch.object(client.opener,'open') as opened:
   with self.assertRaisesRegex(p.Stop,'untrusted'):client.request('PUT','https://evil.example/session',b'file')
   opened.assert_not_called()

class CredentialTests(unittest.TestCase):
 def fixture(self):return {'type':'service_account','client_email':'fixture@scorer-test.iam.gserviceaccount.com','private_key':'-----BEGIN PRIVATE KEY-----\nfixture\n-----END PRIVATE KEY-----\n','token_uri':p.TOKEN_URL}
 def test_private_credential_install_is_idempotent_and_never_removes_existing_key(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);private=root/'private';private.mkdir(mode=0o700);incoming=root/'incoming';incoming.mkdir(mode=0o700);source=incoming/'key.json';source.write_text(json.dumps(self.fixture()));dest=private/'google.json'
   with patch.object(p,'PRIVATE',private),patch.object(p,'CREDENTIALS',dest):
    p.install_credentials(source);before=dest.read_bytes();self.assertEqual(dest.stat().st_mode&0o777,0o600)
    p.install_credentials(source);self.assertEqual(dest.read_bytes(),before)
    changed=self.fixture();changed['client_email']='different@scorer-test.iam.gserviceaccount.com';source.write_text(json.dumps(changed))
    with self.assertRaisesRegex(p.Stop,'refusing replacement'):p.install_credentials(source)
    self.assertEqual(dest.read_bytes(),before)
 def test_bad_new_credentials_are_removed_but_source_preserved(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);source=root/'bad.json';source.write_text('{}');dest=root/'google.json'
   with patch.object(p,'PRIVATE',root),patch.object(p,'CREDENTIALS',dest),self.assertRaises(p.Stop):p.install_credentials(source)
   self.assertFalse(dest.exists());self.assertTrue(source.exists())
 def test_readable_by_other_users_and_symlink_credentials_are_rejected(self):
  with tempfile.TemporaryDirectory() as directory:
   path=Path(directory)/'key.json';path.write_text(json.dumps(self.fixture()));path.chmod(0o644)
   with self.assertRaises(p.Stop):p.load_account(path)
   path.chmod(0o600);link=Path(directory)/'link';link.symlink_to(path)
   with self.assertRaises(p.Stop):p.load_account(link)
 def test_non_google_token_endpoint_is_rejected_before_auth(self):
  with tempfile.TemporaryDirectory() as directory:
   path=Path(directory)/'key.json';data=self.fixture();data['token_uri']='https://evil.example/token';path.write_text(json.dumps(data));path.chmod(0o600)
   with self.assertRaises(p.Stop):p.load_account(path)

class CryptoTests(unittest.TestCase):
 def test_real_rs256_jwt_signature_and_claims_with_disposable_fixture_key(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);key=root/'fixture.pem';public=root/'fixture.pub'
   subprocess.run(['openssl','genpkey','-algorithm','RSA','-pkeyopt','rsa_keygen_bits:2048','-out',str(key)],check=True,capture_output=True)
   subprocess.run(['openssl','pkey','-in',str(key),'-pubout','-out',str(public)],check=True,capture_output=True)
   account={'client_email':'fixture@test.iam.gserviceaccount.com','private_key':key.read_text(),'private_key_id':'fixture-id'}
   token=p.jwt(account,now=1000);header,claims,signature=token.split('.');decode=lambda s:base64.urlsafe_b64decode(s+'='*(-len(s)%4))
   body=json.loads(decode(claims));self.assertEqual(body['aud'],p.TOKEN_URL);self.assertEqual(body['scope'],p.SCOPE);self.assertEqual(body['exp'],4500)
   signature_file=root/'signature';signature_file.write_bytes(decode(signature))
   result=subprocess.run(['openssl','dgst','-sha256','-verify',str(public),'-signature',str(signature_file)],input=(header+'.'+claims).encode(),capture_output=True)
   self.assertEqual(result.returncode,0)
 def test_actual_approved_unsigned_payload_matches_pinned_payload(self):
  path=Path('/workspace/Scorer-World-1.0-1030008-unsigned.aab')
  if not path.exists():self.skipTest('Approved build is not part of portable source fixtures')
  self.assertEqual(p.payload_digest(path),p.PAYLOAD)
 @unittest.skipUnless(shutil.which('jarsigner') and shutil.which('keytool'),'Full JDK required for fixture signing')
 def test_owner_certificate_and_payload_validation_with_real_jdk_fixture_signature(self):
  from tools.play.sign_local_bundle import sign_bundle,fingerprint
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);key=root/'fixture.p12';source=root/'unsigned.aab';output=root/'signed.aab'
   subprocess.run(['keytool','-genkeypair','-alias','fixture','-keyalg','RSA','-keysize','2048','-validity','30','-storetype','PKCS12','-keystore',str(key),'-storepass','fixture-only-1234','-dname','CN=Disposable Fixture'],check=True,capture_output=True)
   result=subprocess.run(['keytool','-exportcert','-rfc','-alias','fixture','-keystore',str(key),'-storepass','fixture-only-1234'],check=True,capture_output=True,text=True);cert=fingerprint(result.stdout)
   with zipfile.ZipFile(source,'w') as z:z.writestr('BundleConfig.pb',b'fixture');z.writestr('base/manifest/AndroidManifest.xml',b'fixture');z.writestr('base/assets/original',b'approved fixture')
   content=p.payload_digest(source);sign_bundle(source,output,key,'fixture-only-1234',p.sha(source),cert,'fixture')
   with patch.object(p,'PAYLOAD',content),patch.object(p,'CERT',cert):self.assertEqual(p.verify_signed(output),p.sha(output))
   with patch.object(p,'PAYLOAD',content),patch.object(p,'CERT','0'*64),self.assertRaisesRegex(p.Stop,'certificate'):p.verify_signed(output)
   with zipfile.ZipFile(output,'a') as z:z.writestr('base/assets/injected',b'not approved')
   with patch.object(p,'PAYLOAD',content),self.assertRaisesRegex(p.Stop,'payload'):p.verify_signed(output)

class TransportTests(unittest.TestCase):
 class Response:
  def __init__(self,code,data,headers=None):self.code=code;self.headers=headers or {};self.data=json.dumps(data).encode()
  def read(self,limit):return self.data[:limit]
  def __enter__(self):return self
  def __exit__(self,*_):pass
 def test_oauth_token_exchange_then_bearer_request_without_private_key_in_payload(self):
  client=p.Client({'private_key':'fixture-private-key'});requests=[]
  def open_request(request,timeout):
   requests.append(request)
   return self.Response(200,{'access_token':'fixture-token','expires_in':3600}) if len(requests)==1 else self.Response(200,{'id':'fixture'})
  with patch.object(p,'jwt',return_value='fixture-jwt-assertion'),patch.object(client.opener,'open',side_effect=open_request):self.assertEqual(client.api('POST',p.BASE,{}),{'id':'fixture'})
  self.assertEqual(requests[0].full_url,p.TOKEN_URL);self.assertIsNone(requests[0].get_header('Authorization'))
  self.assertIn(b'fixture-jwt-assertion',requests[0].data);self.assertNotIn(b'fixture-private-key',requests[0].data)
  self.assertEqual(requests[1].get_header('Authorization'),'Bearer fixture-token')
 def test_error_output_redacts_secrets(self):
  client=p.Client({'private_key':'fixture-private-key'});client.token='fixture-token';client.expires=10**12
  with patch.object(client.opener,'open',return_value=self.Response(403,{'error':{'message':'fixture-token fixture-private-key'}})):
   with self.assertRaises(p.APIError) as result:client.api('GET',p.BASE)
  self.assertNotIn('fixture-token',str(result.exception));self.assertNotIn('fixture-private-key',str(result.exception))
 def test_redirect_does_not_forward_bearer(self):
  self.assertIsNone(p.NoRedirect().redirect_request(None,None,302,'Moved',{},'https://evil.example'))

class SnapshotTests(unittest.TestCase):
 def test_private_snapshot_remains_stable_when_sftp_path_is_replaced(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);source=root/'incoming.aab';source.write_bytes(b'approved snapshot');private=root/'private';private.mkdir(mode=0o700)
   target=p.snapshot_signed(source,private);source.write_bytes(b'replaced source')
   self.assertEqual(target.read_bytes(),b'approved snapshot');self.assertEqual(target.stat().st_mode&0o777,0o600)
   link=root/'link';link.symlink_to(source)
   with self.assertRaises(OSError):p.snapshot_signed(link,private)
