import sqlite3,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from server.session_notices import run

class SessionNoticesTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.db=Path(self.tmp.name)/'usage.sqlite'
        with sqlite3.connect(self.db) as db:
            db.execute('CREATE TABLE totals(day TEXT,event TEXT,count INTEGER,PRIMARY KEY(day,event))')
            db.execute("INSERT INTO totals VALUES('2026-10-26','sessions',1)")
    def test_preview_no_mail_or_ack_and_send_only_new_totals(self):
        with patch('server.session_notices.send_message') as send:
            self.assertIn('Sessões iniciadas: 1',run(self.db));send.assert_not_called()
            self.assertIn('Sessões iniciadas: 1',run(self.db,send=True));self.assertEqual(send.call_count,1)
            self.assertEqual(run(self.db,send=True),'');self.assertEqual(send.call_count,1)
            with sqlite3.connect(self.db) as db:db.execute("INSERT INTO totals VALUES('2026-10-26','sessions_ended',1)")
            self.assertIn('Sessões terminadas normalmente: 1',run(self.db,send=True));self.assertEqual(send.call_count,2)
    def test_mail_failure_keeps_pending_and_baseline_does_not_send(self):
        with patch('server.session_notices.send_message',side_effect=OSError('offline')):
            with self.assertRaises(OSError):run(self.db,send=True)
        self.assertIn('Sessões iniciadas: 1',run(self.db))
        with patch('server.session_notices.send_message') as send:
            self.assertEqual(run(self.db,baseline=True),'');self.assertEqual(run(self.db,send=True),'');send.assert_not_called()
    def test_smtp_uses_server_configuration_and_verified_starttls(self):
        from server.usage_digest import send_message
        settings={'SCORER_STATS_MAIL_TO':'owner@example.com','SCORER_STATS_MAIL_FROM':'stats@example.com','SCORER_STATS_SMTP_HOST':'smtp.example.com','SCORER_STATS_SMTP_USER':'server-user','SCORER_STATS_SMTP_PASSWORD':'fake-test-secret'}
        with patch.dict('os.environ',settings),patch('server.usage_digest.smtplib.SMTP') as smtp:
            send_message('SCORER Free — sessões','Sessões iniciadas: 1')
            client=smtp.return_value.__enter__.return_value
            context=client.starttls.call_args.kwargs['context']
            self.assertTrue(context.check_hostname);self.assertEqual(context.verify_mode,2)
            client.login.assert_called_once_with('server-user','fake-test-secret')
            message=client.send_message.call_args.args[0]
            self.assertEqual(message['To'],'owner@example.com');self.assertNotIn('fake-test-secret',message.as_string())
