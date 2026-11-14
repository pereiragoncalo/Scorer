import copy,unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.metrics import Metrics
from kivy.uix.button import Button
from test_menus import isolated_game,settle
from contract_negotiation import expired,remaining

class ContractMeetings(unittest.TestCase):
 def test_hearing_club_does_not_sign_and_explicit_signature_opens_coach(self):
  with isolated_game()as g:
   g.view='offers';name=g.career.offers[0];g._activate_ui('accept_offer',name);g.draw();settle()
   self.assertEqual(g.view,'contract_meeting');self.assertFalse(g.career.club_name)
   g._activate_ui('contract_change','premium');g._activate_ui('contract_sign');self.assertFalse(g.career.club_name)
   g._activate_ui('contract_propose');g._activate_ui('contract_sign');g.draw();settle()
   self.assertEqual(g.career.club_name,name);self.assertTrue(g._career_started);self.assertEqual(g.view,'coach');self.assertGreater(remaining(g.career),0)
 def test_back_button_and_escape_return_to_offers_without_signing(self):
  with isolated_game()as g:
   g.view='offers';g._activate_ui('accept_offer',g.career.offers[0]);g.draw();settle()
   back=next(w for w in g._menu.walk()if isinstance(w,Button)and w.text=='BACK');back.dispatch('on_release')
   self.assertEqual(g.view,'offers');self.assertFalse(g.career.club_name)
   g._activate_ui('accept_offer',g.career.offers[0]);g._activate_ui('help');g._activate_ui('help_back');self.assertEqual(g.view,'contract_meeting')
   g._on_key_down(None,27,0,'',[])
   self.assertEqual(g.view,'offers');self.assertFalse(g.career.club_name)
 def test_hearing_other_club_retains_first_clubs_actual_response(self):
  with isolated_game()as g:
   g.view='offers';g.career.offers=[t.name for t in g.career.current_league.clubs[:2]];a,b=g.career.offers[:2];g._activate_ui('accept_offer',a);uid=g._contract_uid
   g._activate_ui('contract_change','home');g._activate_ui('contract_propose');row=copy.deepcopy(g.career.life['negotiations'][uid])
   g._activate_ui('contract_back');g._activate_ui('accept_offer',b);self.assertNotEqual(g._contract_uid,uid)
   g._activate_ui('contract_back');g._activate_ui('accept_offer',a);self.assertEqual(g.career.life['negotiations'][uid],row);self.assertFalse(g.career.club_name)
 def test_expired_contract_blocks_play_and_training_until_renewed(self):
  with isolated_game()as g:
   c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();c.season=c.life['contract']['end_season'];g.view='hub';g._career_started=True
   self.assertTrue(expired(c));g.start_career_match();self.assertEqual(g.view,'agent');self.assertEqual(c.matches,0)
   g.start_training();self.assertEqual(g.view,'agent');self.assertEqual(c.training_shots_taken,0)
   g._activate_ui('contract_renew');self.assertEqual(g.view,'contract_meeting');g._activate_ui('contract_sign');self.assertFalse(expired(c))
 def test_failed_sign_does_not_show_success_or_leave_the_meeting(self):
  with isolated_game()as g:
   g.view='offers';g._activate_ui('accept_offer',g.career.offers[0])
   with patch.object(g.career,'save',return_value=False):g._activate_ui('contract_sign')
   self.assertEqual(g.view,'contract_meeting');self.assertFalse(g.career.club_name);self.assertIn('Unable',g.career.message)
 def test_meeting_is_readable_and_sign_button_reachable_in_nine_languages(self):
  old=Window.size;density=Metrics.density
  try:
   Metrics.density=1.;Window.size=(640,295)
   with isolated_game()as g:
    g.size=Window.size;g.i18n.world=True;g.view='offers';g._activate_ui('accept_offer',g.career.offers[0])
    from localization import LANGUAGES
    for language in LANGUAGES:
     g.i18n.choose(language);g.draw();settle()
     label=g.i18n.tr('Sign club offer');button=next(w for w in g._menu.walk()if isinstance(w,Button)and w.text==label)
     self.assertGreaterEqual(button.height,48)
     g._menu.scroll.scroll_to(button,padding=10,animate=False);settle()
     self.assertGreaterEqual(button.to_window(*button.pos)[1],-1);self.assertLessEqual(button.to_window(button.x,button.top)[1],g.top+1)
  finally:Window.size=old;Metrics.density=density
