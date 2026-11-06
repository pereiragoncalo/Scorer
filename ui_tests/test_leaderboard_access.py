import unittest,time
from unittest.mock import patch
from kivy.uix.button import Button
from kivy.uix.label import Label
from test_menus import isolated_game,settle
from season_records import scope
from menu_ui import SeasonRecordsScreen

class LeaderboardAccessTests(unittest.TestCase):
    def test_locked_sharing_still_fetches_and_displays_public_rows_without_a_post(self):
        with isolated_game(saved=True) as g:
            kind,country,division=scope(g.career,False)
            entry=dict(edition=kind,country=country,division=division,season=2026,player='Published Player',team='Published Club',matches=46,goals=30,publisher='a'*32,record_id='b'*32)
            g.leaderboard.origin='https://stats.example.com';self.assertFalse(g.family.social)
            with patch.object(g.leaderboard,'request',return_value={'schema':3,'entries':[entry]}) as request:
                g.view='hub';g._activate_ui('leaderboard')
                until=time.monotonic()+3
                while g.leaderboard.busy and time.monotonic()<until:time.sleep(.01)
                settle();g.draw();settle()
                self.assertEqual(g.view,'leaderboard');self.assertIsInstance(g._menu.body,SeasonRecordsScreen)
                request.assert_called_once();self.assertTrue(request.call_args.args[0].startswith('/v3/records?'))
                self.assertEqual(len(request.call_args.args),1);self.assertFalse(g.leaderboard.enabled)
                text=' '.join(w.text for w in g._menu.walk() if isinstance(w,Label))
                self.assertIn('Published Player',text);self.assertNotIn('Adult PIN',text);self.assertNotIn('automatic usage',text)
                g._activate_ui('record_safety');self.assertEqual(g.view,'record_safety')
    def test_main_menus_have_no_privacy_and_help_keeps_transfer_settings_accessible(self):
        with patch('edition.WORLD_BUILD',True),isolated_game(saved=True) as g:
            for size in ((960,540),(320,240),(360,640)):
                g.size=size
                for view in ('start','hub','scorers'):
                    g.view=view;g.draw();settle()
                    texts={w.text for w in g._menu.walk() if isinstance(w,Button)}
                    self.assertNotIn('PRIVACY',texts);self.assertNotIn('GLOBAL',texts)
                    if view=='hub':self.assertIn('LEADERBOARD',texts)
            g.view='hub';g._activate_ui('help');settle()
            settings=next(w for w in g._context_help.walk() if isinstance(w,Button) and w.text=='SETTINGS')
            settings.trigger_action(duration=0);settle();self.assertEqual(g.view,'privacy')
            self.assertTrue(any(isinstance(w,Button) and w.text=='EXPORT CAREER' for w in g._menu.walk()))
            g._activate_ui('privacy_back');self.assertEqual(g.view,'hub')
