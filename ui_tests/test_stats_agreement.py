"""Exercise startup choice through the real game and HTTP aggregate receiver."""
import json,tempfile,threading,unittest
from pathlib import Path
from unittest.mock import patch
from ui_tests.test_menus import isolated_game
from main import StrikerApp
from anonymous_stats import create_statistics,UsageStatistics
from server.usage_collector import Collector

class AgreementTests(unittest.TestCase):
 def setup_usage(self,g):
  with patch('anonymous_stats.APP_NOTICE_REQUIRED',True):g.usage=create_statistics(True,g.career.save_path.parent,endpoint='https://stats.example/v1/usage')
  g.view='data_notice'
 def wait(self,g):
  for _ in range(100):
   if not g.usage._sending:return
   threading.Event().wait(.01)
  self.fail('Upload did not finish')
 def test_agree_persists_enables_and_delivers_one_opening_to_real_collector(self):
  from urllib.request import Request,urlopen
  with tempfile.TemporaryDirectory() as d:
   collector=Collector(('127.0.0.1',0),Path(d)/'usage.sqlite','fixture-token')
   worker=threading.Thread(target=collector.serve_forever,daemon=True);worker.start()
   try:
    with isolated_game() as g:
     self.setup_usage(g);sent=[]
     def sender(_,payload):
      sent.append(payload)
      with urlopen(Request('http://127.0.0.1:'+str(collector.server_port)+'/v1/usage',json.dumps(payload).encode(),{'Content-Type':'application/json'},method='POST')) as response:return 200<=response.status<300
     g.usage._sender=sender;g.usage.begin_session()
     self.assertFalse(g.usage.flush_async());self.assertEqual(sent,[])
     g._activate_ui('notice_continue');self.wait(g)
     self.assertEqual(g.view,'start');self.assertTrue(g.usage.enabled);self.assertFalse(g.leaderboard.enabled)
     self.assertEqual(len(sent),1);self.assertEqual(sent[0]['counts'],{'sessions':1});self.assertEqual(g.usage.counts,{})
     self.assertTrue(UsageStatistics(g.career.save_path.parent,g.usage.endpoint,consent_version=1).enabled)
   finally:collector.shutdown();collector.server_close();worker.join()
 def test_decline_closes_and_never_transmits_even_with_previous_enabled_state(self):
  with isolated_game() as g:
   self.setup_usage(g);g.usage.set_enabled(True);g.usage.begin_session()
   app=type('App',(),{'stop':lambda _:None})()
   with patch.object(app,'stop') as stop,patch('main.App.get_running_app',return_value=app),patch.object(g.usage,'_sender') as sender:
    g._activate_ui('notice_exit');stop.assert_called_once();self.assertFalse(g.usage.flush_async());sender.assert_not_called()
    self.assertEqual(g.usage.counts,{})
 def test_agree_does_not_enter_game_or_send_if_choice_cannot_be_saved(self):
  with isolated_game() as g:
   self.setup_usage(g)
   with patch.object(g.usage,'_save',return_value=False),patch.object(g.usage,'_sender') as sender:
    g._activate_ui('notice_continue');self.assertEqual(g.view,'data_notice');self.assertFalse(g.usage.enabled);self.assertFalse(g.usage.delivery_ready);sender.assert_not_called()
 def test_real_agree_button_touch_activates_counters_on_phone_layouts(self):
  from kivy.core.window import Window
  from kivy.tests.common import UnitTestTouch
  from kivy.metrics import dp
  from menu_ui import MenuTile
  from ui_tests.test_menus import settle
  old=Window.size
  try:
   for size in ((1280,591),(640,360)):
    Window.size=size
    with isolated_game() as g:
     self.setup_usage(g);g.size=size;g.draw();settle()
     button=next(w for w in g.walk() if isinstance(w,MenuTile) and w.text=='I AGREE')
     self.assertGreaterEqual(button.height,dp(48));self.assertGreaterEqual(button.y,0);self.assertLessEqual(button.top,g.top+1)
     with patch.object(g.usage,'_sender',return_value=True):
      touch=UnitTestTouch(*button.center);touch.touch_down();touch.touch_up();settle();self.wait(g)
     self.assertTrue(g.usage.enabled);self.assertEqual(g.view,'start')
  finally:Window.size=old
