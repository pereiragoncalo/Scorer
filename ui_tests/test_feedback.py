import sys,types,unittest
from unittest.mock import patch,Mock
from urllib.parse import urlsplit,parse_qs,unquote
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.tests.common import UnitTestTouch
from kivy.uix.textinput import TextInput
from kivy.metrics import Metrics,dp
from menu_ui import TouchButton,DashboardField
from kivy.core.text import Label as CoreLabel
from test_menus import isolated_game,settle
import test_retro_attendance_titles as retro
import feedback,release_settings
class FeedbackTests(unittest.TestCase):
 def test_hub_button_opens_draft_without_changing_career(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=retro.RetroSceneTests().prepare(g);Window.size=g.size=(1280,591);g.view='hub';g.draw();settle();before=c.matches,c.goals,c.week
   button=next(w for w in g._menu.walk() if isinstance(w,TouchButton) and w.text=='FEEDBACK')
   with patch('feedback.compose') as compose:
    t=UnitTestTouch(*button.center);t.touch_down();t.touch_up();settle();compose.assert_called_once()
   self.assertEqual((c.matches,c.goals,c.week),before);self.assertEqual(g.view,'hub')
 def test_android_uses_sendto_on_ui_thread_with_public_address_only(self):
  launched=[];decorated=[]
  class Intent:
   ACTION_SENDTO='SENDTO'
   def __init__(self,action,url):self.action=action;self.url=url
  activity=types.SimpleNamespace(startActivity=launched.append)
  mapping={'android.content.Intent':Intent,'android.net.Uri':types.SimpleNamespace(parse=lambda url:url),'org.kivy.android.PythonActivity':types.SimpleNamespace(mActivity=activity)}
  def ui_thread(fn):decorated.append(fn);return fn
  modules={'android':types.ModuleType('android'),'android.runnable':types.SimpleNamespace(run_on_ui_thread=ui_thread),'jnius':types.SimpleNamespace(autoclass=mapping.__getitem__)}
  failed=Mock()
  with patch('kivy.utils.platform','android'),patch.dict(sys.modules,modules):feedback.compose(failed)
  self.assertEqual(len(decorated),1);self.assertEqual(len(launched),1);self.assertEqual(launched[0].action,'SENDTO')
  url=urlsplit(launched[0].url);self.assertEqual(url.scheme,'mailto');self.assertEqual(unquote(url.path),release_settings.SUPPORT_EMAIL);self.assertEqual(parse_qs(url.query),{'subject':['Scorer World - Feedback']});failed.assert_not_called()
 def test_missing_email_client_provides_copyable_contact(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   retro.RetroSceneTests().prepare(g);g.view='hub';g.draw();settle()
   try:
    with patch('kivy.utils.platform','linux'),patch('webbrowser.open',return_value=False):feedback.compose(lambda:feedback.unavailable(g));settle()
    popup=g._feedback_popup;self.assertIsNotNone(popup)
    field=next(w for w in popup.content.walk(restrict=True) if isinstance(w,TextInput));self.assertTrue(field.readonly);self.assertEqual(field.text,release_settings.SUPPORT_EMAIL)
    with patch('kivy.core.clipboard.Clipboard.copy') as copy:
     button=next(w for w in popup.content.walk(restrict=True) if isinstance(w,TouchButton) and w.text=='COPY EMAIL');button.dispatch('on_release');copy.assert_called_once_with(release_settings.SUPPORT_EMAIL)
   finally:
    if getattr(g,'_feedback_popup',None):g._feedback_popup.dismiss();settle()
 def test_android_no_handler_uses_main_clock_failure_callback(self):
  modules={'android':types.ModuleType('android'),'android.runnable':types.SimpleNamespace(run_on_ui_thread=lambda fn:fn),'jnius':types.SimpleNamespace(autoclass=Mock(side_effect=RuntimeError('No handler')))}
  failed=Mock()
  with patch('kivy.utils.platform','android'),patch.dict(sys.modules,modules):feedback.compose(failed)
  settle();failed.assert_called_once()
 def test_fallback_fits_compact_and_phone_sizes(self):
  old=Window.size;density=Metrics.density
  try:
   with patch('edition.WORLD_BUILD',True),isolated_game() as g:
    for width,height,ratio in ((320,240,1),(1280,591,1.4),(1920,1080,3)):
     Window.size=g.size=(width,height);Metrics.density=ratio
     for lang in ('en','pt','de','ja'):
      g.i18n.choose(lang);feedback.unavailable(g);settle();popup=g._feedback_popup
      try:
       self.assertGreaterEqual(popup.x,0);self.assertGreaterEqual(popup.y,0);self.assertLessEqual(popup.right,width+1);self.assertLessEqual(popup.top,height+1)
       for w in popup.content.walk(restrict=True):
        if isinstance(w,DashboardField):
         m=CoreLabel(text=w.text,text_size=(w.width,None),font_name=w.font_name,font_size=w.font_size,line_height=w.line_height);m.refresh();self.assertLessEqual(m.texture.size[1],w.height+2)
        if isinstance(w,TouchButton):self.assertGreaterEqual(w.height,dp(48));self.assertGreaterEqual(w.y,popup.y);self.assertLessEqual(w.top,popup.top)
      finally:popup.dismiss();settle()
  finally:Window.size=old;Metrics.density=density

 def test_feedback_is_available_before_creating_a_career(self):
  with isolated_game() as g:
   g.view='start';g.draw();settle();button=next(w for w in g._menu.walk() if isinstance(w,TouchButton) and w.text=='FEEDBACK')
   with patch('feedback.compose') as compose:button.dispatch('on_release');compose.assert_called_once()
   self.assertEqual(g.view,'start')
