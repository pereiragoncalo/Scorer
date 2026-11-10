"""Isolated real v3->v4 installer rehearsal; never connects to the public service."""
import argparse,hashlib,http.client,json,os,runpy,selectors,sqlite3,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
OLD_FILES=('anonymous_stats.py','online_safety.py','privacy_requests.py','season_records.py',
 'server/usage_collector.py','server/moderation.py','server/leaderboard.py',
 'server/season_records.py','server/privacy_cases.py','server/public_pages.py',
 'server/configure_public.py','server/dashboard.html')
ADMIN='isolated-test-only'

def verify(report_path,baseline='qa-0.9.33',installer_path=None,missing_dependencies=False):
 installer_file=Path(installer_path) if installer_path else ROOT/'docs/data/server/Scorer-Backend-Repair-1.py'
 installer=runpy.run_path(str(installer_file),run_name='installer_for_test')
 checks=[];process=None;port=None
 def passed(name,condition=True):
  checks.append(dict(check=name,passed=bool(condition)))
  if not condition:raise AssertionError(name)
 with tempfile.TemporaryDirectory(prefix='scorer-service-rehearsal-') as directory:
  target=Path(directory);(target/'server').mkdir();db=target/'data.sqlite';config=target/'public.json'
  for name in OLD_FILES:
   raw=subprocess.check_output(['git','show',baseline+':'+name],cwd=ROOT)
   (target/name).write_bytes(raw)
  config.write_bytes(subprocess.check_output(['git','show',baseline+':server/public.world.policy.json'],cwd=ROOT))
  def stop():
   nonlocal process
   if process is not None:
    process.terminate()
    try:process.wait(timeout=5)
    except subprocess.TimeoutExpired:process.kill();process.wait()
    process=None
  def start():
   nonlocal process,port
   code="from server.usage_collector import Collector; s=Collector(('127.0.0.1',0),%r,%r,%r); print(s.server_port,flush=True); s.serve_forever()"%(str(db),ADMIN,str(config))
   env=dict(os.environ,PYTHONPATH=str(target))
   process=subprocess.Popen([sys.executable,'-B','-u','-c',code],cwd=target,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
   with selectors.DefaultSelector() as selector:
    selector.register(process.stdout,selectors.EVENT_READ)
    if not selector.select(8):raise RuntimeError('Isolated server startup timed out')
   line=process.stdout.readline().strip()
   if not line.isdigit():raise RuntimeError('Isolated server did not start: '+process.stderr.read())
   port=int(line)
  def call(path,payload=None,admin=False,expect=204):
   time.sleep(.06)  # Exercise protocol correctness below the service rate limit.
   client=http.client.HTTPConnection('127.0.0.1',port,timeout=8)
   headers={'Content-Type':'application/json'}
   if admin:headers['Authorization']='Bearer '+ADMIN
   try:
    client.request('GET' if payload is None else 'POST',path,None if payload is None else json.dumps(payload),headers)
    response=client.getresponse();raw=response.read();status=response.status
   finally:client.close()
   if status!=expect:raise AssertionError(path+' returned '+str(status)+' expected '+str(expect))
   return json.loads(raw) if raw else {}
  query=lambda version:'/v%d/records?edition=world&country=Portugal&division=1'%version
  baseline_row=dict(edition='world',country='Portugal',division=1,season=2026,player='Baseline fixture',team='Old club',matches=30,goals=10)
  baseline_token='1'*64;owner='2'*64;reporter='3'*64
  publisher=hashlib.sha256(('scorer-public:'+hashlib.sha256(owner.encode()).hexdigest()).encode()).hexdigest()[:32]
  try:
   start();passed('old_v3_responds',call(query(3),expect=200)['schema']==3)
   call(query(4),expect=404)
   call('/v3/records',dict(token=baseline_token,record=baseline_row,terms_version=1))
   old_publisher=call('/v1/moderation',admin=True,expect=200)['entries'][0]['publisher']
   call('/v1/moderation',dict(publisher=old_publisher,action='approve'),admin=True)
   with sqlite3.connect(db) as connection:
    connection.execute("INSERT INTO totals VALUES(date('now'),'sessions',42)")
    passed('baseline_has_no_career_table',not connection.execute("SELECT 1 FROM sqlite_master WHERE name='career_records'").fetchone())
   if missing_dependencies:
    stop()
    for name in ('server/privacy_cases.py','privacy_requests.py'):(target/name).unlink()
    env=dict(os.environ,PYTHONPATH=str(target))
    failed=subprocess.run([sys.executable,'-B','-c','from server.usage_collector import Collector'],cwd=target,env=env,capture_output=True,text=True)
    passed('reproduces_missing_privacy_cases_import_failure',failed.returncode!=0 and 'privacy_cases' in failed.stderr)
   installer['apply'](target,installer['sources'](),stop,start,lambda:installer['verify'](port))
   if missing_dependencies:passed('missing_dependencies_repaired',(target/'server/privacy_cases.py').is_file() and (target/'privacy_requests.py').is_file())
   passed('real_bundled_installer_verifies_public_pages_and_v3_v4')
   passed('existing_season_record_preserved',call(query(3),expect=200)['entries']==[dict(baseline_row,publisher=old_publisher,record_id=call(query(3),expect=200)['entries'][0]['record_id'])])
   passed('new_career_board_empty',call(query(4),expect=200)['entries']==[])
   row=dict(baseline_row,player='New fixture',team='New club',matches=20,goals=6)
   career=dict(row,matches=300,goals=120)
   for version,record in ((3,row),(4,career)):
    call('/v%d/records'%version,dict(token=owner,record=record,terms_version=True),expect=400)
    call('/v%d/records'%version,dict(token=owner,record=record,terms_version=1))
    passed('v%d_pending_record_not_public'%version,not any(e['publisher']==publisher for e in call(query(version),expect=200)['entries']))
   call('/v1/moderation',dict(publisher=publisher,action='approve'),expect=404)
   queue=call('/v1/moderation',admin=True,expect=200)
   passed('both_pending_categories_in_private_queue',len([e for e in queue['entries'] if e['publisher']==publisher])==2)
   passed('queue_does_not_expose_write_credentials',all(t not in json.dumps(queue) for t in (owner,baseline_token,reporter)))
   call('/v1/moderation',dict(publisher=publisher,action='approve'),admin=True)
   for version in (3,4):passed('v%d_approval_publishes'%version,any(e['publisher']==publisher for e in call(query(version),expect=200)['entries']))
   from online_leaderboard import Leaderboard
   client=Leaderboard(target/'test-client');client.entries=call(query(3),expect=200)['entries'];client.block(publisher)
   passed('client_block_preserves_other_publisher',len(client.entries)==1 and client.entries[0]['publisher']==old_publisher)
   passed('client_block_survives_reload',publisher in Leaderboard(target/'test-client').blocked)
   call('/v3/reports',dict(token=reporter,publisher=publisher,reason='other'))
   passed('report_visible_to_moderator',len(call('/v1/moderation',admin=True,expect=200)['reports'])==1)
   call('/v1/moderation',dict(publisher=publisher,action='ban'),admin=True)
   for version,record in ((3,row),(4,career)):
    passed('v%d_ban_hides'%version,not any(e['publisher']==publisher for e in call(query(version),expect=200)['entries']))
    call('/v%d/records'%version,dict(token=owner,record=record,terms_version=1),expect=403)
   call('/v3/records/withdraw',dict(token=owner));call('/v3/records/withdraw',dict(token=owner))
   queue=call('/v1/moderation',admin=True,expect=200)
   passed('withdraw_removes_both_categories_and_reports',not any(e['publisher']==publisher for e in queue['entries']) and not queue['reports'])
   passed('withdraw_preserves_unrelated_record',call(query(3),expect=200)['entries'][0]['publisher']==old_publisher)
   with sqlite3.connect(db) as connection:
    passed('aggregate_totals_preserved',connection.execute("SELECT count FROM totals WHERE event='sessions'").fetchone()[0]==42)
    passed('no_career_rows_after_withdrawal',connection.execute('SELECT COUNT(*) FROM career_records').fetchone()[0]==0)
   result=dict(scope='Isolated fixture only; no public requests',baseline=baseline,installer_sha256=hashlib.sha256(installer_file.read_bytes()).hexdigest(),checks=checks)
  finally:stop()
 Path(report_path).parent.mkdir(parents=True,exist_ok=True)
 Path(report_path).write_text(json.dumps(result,indent=2)+'\n')
 print('PASS:',len(checks),'isolated migration/moderation/deletion checks')
 return result
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',type=Path,required=True);parser.add_argument('--installer',type=Path);parser.add_argument('--missing-dependencies',action='store_true');args=parser.parse_args();verify(args.report,installer_path=args.installer,missing_dependencies=args.missing_dependencies)
