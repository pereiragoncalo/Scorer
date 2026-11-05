import unittest
from unittest.mock import patch
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.tests.common import UnitTestTouch
from menu_ui import MenuTile,EdgePanel
from player_development import FOCI,HINTS,NAMES
from test_menus import isolated_game,settle
class DevelopmentUI(unittest.TestCase):
 def sign(self,g):
  c=g.career;c.accept_starting_offer(c.offers[0]);g._career_started=True;g.view='hub';g.draw();settle();Clock.unschedule(g.update);return c
 def test_player_has_only_objectives_in_one_panel_and_preserves_name_controls(self):
  with isolated_game() as g:
   c=self.sign(g);g._activate_ui('profile');g.draw();settle()
   p=g._menu.body;text=' '.join(w.text for w in p.walk() if isinstance(w,Label))
   self.assertIn('Club goals:',text);self.assertIn('CAREER MILESTONES',text)
   for forbidden in ('TRAINING FOCUS','PLAYER DEVELOPMENT','Tracking began','Earlier seasons','HOW TRUST CHANGES','TROPHIES'):
    self.assertNotIn(forbidden,text)
   self.assertEqual(sum(isinstance(w,EdgePanel) for w in p.walk()),1)
   p.name.text='Updated Name';p.submit();self.assertEqual(c.player_name,'Updated Name')
 def test_confidence_link_shows_only_stats_and_returns_to_hub(self):
  with isolated_game() as g:
   c=self.sign(g);p=g._menu.body
   if hasattr(p,'trust_link'):
    touch=UnitTestTouch(*p.trust_link.center);touch.touch_down();touch.touch_up()
   else:next(w for w in p.walk() if isinstance(w,MenuTile) and w.text=='COACH TRUST').dispatch('on_release')
   g.draw();settle();self.assertEqual(g.view,'development')
   text=' '.join(w.text for w in g._menu.body.walk() if isinstance(w,Label))
   self.assertIn('Trust 50/100',text);self.assertIn('75 minutes',text)
   for forbidden in ('below 45','Training +2','Training and goals','TRAINING FOCUS','Role changes','Substitutes enter'):
    self.assertNotIn(forbidden,text)
   g._activate_ui('development_back');self.assertEqual(g.view,'hub')
 def test_focus_selector_is_training_only_and_keeps_session_locked(self):
  with isolated_game() as g:
   c=self.sign(g);g._activate_ui('training_focus_open');self.assertIsNone(getattr(g,'_training_focus_popup',None))
   g._activate_ui('training_focus','heading');self.assertEqual(c.training_focus,'placed')
   g.view='training';g.draw();settle();g._activate_ui('training_focus_open');settle()
   popup=g._training_focus_popup
   try:
    self.assertEqual(g.view,'training');popup.choose(g._menu,'heading');settle()
   finally:popup.dismiss()
   self.assertEqual(c.training_focus,'heading');g.start_training()
   self.assertEqual(g.shot_type,'header');self.assertEqual(g.field_players,[])
   self.assertFalse(c.choose_training_focus('penalties'))
   for _ in range(3):g.result_text='GOAL!';g._advance_after_shot()
   self.assertEqual(c.development['skills']['heading']['xp'],24)
   g.draw();settle();g._activate_ui('training_focus_open');settle();popup=g._training_focus_popup
   try:
    choices=[w for w in popup.walk() if isinstance(w,MenuTile) and '\n'in w.text]
    self.assertEqual(len(choices),4);self.assertTrue(all(w.disabled for w in choices))
   finally:popup.dismiss()
 def test_training_has_values_and_controls_without_explanations(self):
  with isolated_game() as g:
   c=self.sign(g);g.view='training';g.draw();settle()
   text=' '.join(w.text for w in g._menu.body.walk() if isinstance(w,Label))
   for value in ('Completed shots: 0/3','Goals: 0/3','XP 0/60','Energy: 10.0/20','Morale: 10.0/20'):
    self.assertIn(value,text)
   for forbidden in ('Complete three shots','One striker','Each level','earn 12 XP','SESSION PLAN','Alternate low'):
    self.assertNotIn(forbidden,text)
 def test_help_reaches_every_moved_explanation_and_justifies_all_paragraphs(self):
  from world_ui import WORLD_HELP_PAGES
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   self.sign(g);g._activate_ui('help')
   collected=[]
   for index in range(len(WORLD_HELP_PAGES)):
    g.help_page=index;g.draw();settle()
    collected.extend(w.text for w in g._menu.body.walk() if isinstance(w,Label))
    for label in g._menu.body.walk():
     if isinstance(label,Label) and len(label.text)>90:self.assertEqual(label.halign,'justify')
   text=' '.join(collected)
   for explanation in ('earn 12 XP','below 45','Training +2','Training and goals',*HINTS.values()):self.assertIn(explanation,text)
   g._activate_ui('help_page',1);self.assertEqual(g.help_page,len(WORLD_HELP_PAGES)-1)
   g._activate_ui('help_page',-100);self.assertEqual(g.help_page,0)
 def test_actual_focus_drills_and_visible_bonus_criteria_are_preserved(self):
  with isolated_game() as g:
   c=self.sign(g)
   for focus in FOCI:
    c._consume_match_training();c.choose_training_focus(focus);g.view='training';g.start_training()
    self.assertEqual(g.field_players,[]);self.assertIsNone(g.current_opportunity)
    self.assertEqual(g.shot_type,'header' if focus=='heading' else 'penalty' if focus=='penalties' else 'kick')
   for focus,targets in (('low',((0.,.4),(0.,1.2),(0.,.9))),('placed',((1.5,1.),(0.,1.),(-2.5,1.)))):
    c._consume_match_training();c.choose_training_focus(focus);g.view='training';g.start_training()
    for x,z in targets:g.aim_x=x;g.aim_z=z;g.result_text='GOAL!';g._advance_after_shot()
    self.assertEqual(c.development['skills'][focus]['xp'],20)
 def test_role_window_and_skill_controls_are_preserved(self):
  with isolated_game() as g:
   c=self.sign(g);c.morale=16;c.development.update(trust=30,peak_trust=50);c.last_training_week=c.week;g.start_career_match()
   self.assertEqual(len(g.match_chance_minutes),3);self.assertEqual((g.match_entry_minute,g.match_exit_minute),(60,90))
   self.assertTrue(all(m>=60+g.match_first_stoppage for m in g.match_chance_minutes))
   g.shot_context='match';g.view='shot';c.development['skills']['heading']=dict(level=10,xp=0)
   g._prepare_next_shot();g.shot_time_limit=4.;g.current_aim_speed=3.;g._start_opportunity('cross',7)
   self.assertAlmostEqual(g.shot_time_limit,4.8);self.assertLess(g.current_aim_speed,3.)
