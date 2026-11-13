import json,sqlite3,tempfile,threading,unittest
from datetime import date,datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from server.usage_collector import activity,Collector

class ActivityTests(unittest.TestCase):
 def test_window_includes_today_and_29_prior_dates_with_zero_days(self):
  with sqlite3.connect(':memory:') as db:
   db.execute('CREATE TABLE totals(day TEXT,event TEXT,count INTEGER)')
   db.executemany('INSERT INTO totals VALUES(?,?,?)', [('2026-10-14','sessions',99),('2026-10-15','sessions',2),('2026-10-15','sessions_ended',1),('2026-11-13','sessions',5),('2026-11-13','sessions_ended',4),('2026-11-14','sessions',99),('2026-11-13','goals_scored',800)])
   before=db.execute('SELECT * FROM totals').fetchall();data=activity(db,date(2026,11,13))
   self.assertEqual((data['start'],data['end'],data['opens'],data['closes']),('2026-10-15','2026-11-13',7,5))
   self.assertEqual(len(data['days']),30);self.assertEqual(data['days'][1],{'day':'2026-11-12','opens':0,'closes':0})
   self.assertEqual(db.execute('SELECT * FROM totals').fetchall(),before)
 def test_leap_day_empty_window(self):
  with sqlite3.connect(':memory:') as db:
   db.execute('CREATE TABLE totals(day TEXT,event TEXT,count INTEGER)');data=activity(db,date(2024,3,1))
   self.assertEqual(data['start'],'2024-02-01');self.assertEqual(data['days'][1]['day'],'2024-02-29');self.assertEqual((data['opens'],data['closes']),(0,0))
 def test_http_auth_and_panel_only_activity_management_retained(self):
  with tempfile.TemporaryDirectory() as directory:
   server=Collector(('127.0.0.1',0),Path(directory)/'counts.sqlite','fixture-token');thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
   try:
    base='http://127.0.0.1:'+str(server.server_port)
    for headers in ({},{'Authorization':'Bearer wrong'}):
     with self.assertRaises(HTTPError) as error:urlopen(Request(base+'/v1/activity',headers=headers))
     self.assertEqual(error.exception.code,404)
    with server.db() as db:db.execute('INSERT INTO totals VALUES(?,?,?)',(datetime.now(timezone.utc).date().isoformat(),'sessions',3))
    with urlopen(Request(base+'/v1/activity',headers={'Authorization':'Bearer fixture-token'})) as response:
     self.assertEqual(response.headers['Cache-Control'],'no-store');self.assertEqual(json.load(response)['opens'],3)
    with urlopen(base+'/admin') as response:
     html=response.read().decode();self.assertIn('Últimos 30 dias',html);self.assertNotIn('Load moderation',html);self.assertNotIn('goals_scored',html)
    with urlopen(base+'/admin/manage') as response:self.assertIn(b'Load moderation',response.read())
   finally:server.shutdown();server.server_close()

class ActivityInstallTests(unittest.TestCase):
 def test_installer_rolls_back_every_file_and_preserves_database(self):
  from server.install_activity_dashboard import apply,sources
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory)/'app';(root/'server').mkdir(parents=True)
   for name in ('usage_collector.py','dashboard.html'):(root/'server'/name).write_bytes(b'old-'+name.encode())
   (root/'counts.sqlite').write_bytes(b'private database fixture');calls=[]
   with self.assertRaisesRegex(RuntimeError,'probe'):
    apply(root,sources(),lambda:calls.append('stop'),lambda:calls.append('start'),lambda:(_ for _ in ()).throw(RuntimeError('probe')))
   self.assertEqual((root/'server/dashboard.html').read_bytes(),b'old-dashboard.html')
   self.assertFalse((root/'server/management.html').exists());self.assertEqual((root/'counts.sqlite').read_bytes(),b'private database fixture')
   self.assertEqual(calls,['stop','start','stop','start'])
 def test_unknown_installed_version_stops_before_service_changes(self):
  from server.install_activity_dashboard import apply,sources
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory)/'app';(root/'server').mkdir(parents=True)
   for name in ('usage_collector.py','dashboard.html'):(root/'server'/name).write_text('unexpected')
   calls=[]
   with self.assertRaisesRegex(ValueError,'differs'):apply(root,sources(),lambda:calls.append('stop'),lambda:calls.append('start'),lambda:None,{})
   self.assertEqual(calls,[])
