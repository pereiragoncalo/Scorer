import unittest,copy
from unittest.mock import patch
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.label import Label
from menu_ui import MenuTile,FlowLabel
from player_development import FOCI
from test_menus import isolated_game,settle
class DevelopmentUI(unittest.TestCase):
 def sign(self,g):
  c=g.career;c.accept_starting_offer(c.offers[0]);g._career_started=True;g.view='hub';g.draw();settle();Clock.unschedule(g.update);return c
 def test_player_entry_tabs_and_name_draft_survive(self):
  with isolated_game() as g:
   self.sign(g);g._activate_ui('profile');g.draw();settle();g._menu.body.name.text='My Draft'
   button=next(w for w in g.walk() if isinstance(w,MenuTile) and w.text=='PLAYER DEVELOPMENT')
   button.dispatch('on_release');settle();self.assertEqual(g.view,'development')
   self.assertTrue(any(isinstance(w,Label) and 'Club goals:'in w.text for w in g.walk()))
   for tab in ('skills','trust','objectives'):
    g._activate_ui('development_tab',tab);g.draw();settle();self.assertEqual(g._menu.body.tab,tab)
   g._activate_ui('development_back');g.draw();settle();self.assertEqual(g.view,'profile');self.assertEqual(g._menu.body.name.text,'My Draft')
   g._menu.body.name.text='';g._activate_ui('development');g.draw();settle()
   g._activate_ui('development_back');g.draw();settle();self.assertEqual(g._menu.body.name.text,'')
 def test_training_focus_is_selectable_and_locked_until_match(self):
  with isolated_game() as g:
   c=self.sign(g);g.view='training';g.draw();settle()
   g._activate_ui('development','skills');g.draw();settle();g._activate_ui('training_focus','heading')
   self.assertEqual(c.training_focus,'heading');g._activate_ui('development_back');g.start_training()
   self.assertEqual(g.shot_type,'header');self.assertEqual(g.field_players,[])
   self.assertFalse(c.choose_training_focus('penalties'))
   for _ in range(3):g.result_text='GOAL!';g._advance_after_shot()
   self.assertTrue(c.trained_this_week);self.assertEqual(c.development['skills']['heading']['xp'],24)
   self.assertEqual(c.skill_level('placed'),0)
 def test_all_four_training_focuses_have_the_promised_shots(self):
  with isolated_game() as g:
   c=self.sign(g)
   for focus in FOCI:
    c._consume_match_training();self.assertTrue(c.choose_training_focus(focus));g.view='training';g.start_training()
    self.assertEqual(g.field_players,[]);self.assertIsNone(g.current_opportunity)
    self.assertEqual(g.shot_type,'header' if focus=='heading' else 'penalty' if focus=='penalties' else 'kick')
    if focus=='penalties':self.assertEqual((g.shot_origin_x,g.shot_origin_y),(0,11))
    if focus=='heading':self.assertAlmostEqual(g.ball.z,1.31)
 def test_focus_bonus_uses_visible_low_and_outer_third_criteria(self):
  for focus,targets in (('low',((0.,.4),(0.,1.2),(0.,.9))),('placed',((1.5,1.),(0.,1.),(-2.5,1.)))):
   with self.subTest(focus=focus),isolated_game() as g:
    c=self.sign(g);c.choose_training_focus(focus);g.start_training()
    for x,z in targets:
     g.aim_x=x;g.aim_z=z;g.result_text='GOAL!';g._advance_after_shot()
    self.assertEqual(c.training_session_goals,3)
    self.assertEqual(c.development['skills'][focus]['xp'],20)
 def test_role_restricts_real_chance_minutes_and_preserves_high_morale_floor(self):
  with isolated_game() as g:
   c=self.sign(g);c.morale=16;c.development.update(trust=30,peak_trust=50);c.last_training_week=c.week
   g.start_career_match()
   self.assertEqual(len(g.match_chance_minutes),3)
   self.assertEqual((g.match_entry_minute,g.match_exit_minute),(60,90))
   self.assertTrue(all(m>=60+g.match_first_stoppage for m in g.match_chance_minutes))
   c.development.update(trust=50,peak_trust=50);c.last_training_week=c.week
   with patch('main.match_stakes',return_value={'kind':'','prior':(0,0),'late_allowed':True}):g.start_career_match()
   self.assertEqual((g.match_entry_minute,g.match_exit_minute),(0,75))
   self.assertTrue(all(m<75+g.match_first_stoppage for m in g.match_chance_minutes))
 def test_match_skills_change_control_parameters_without_touching_chance_count(self):
  with isolated_game() as g:
   c=self.sign(g);g.shot_context='match';g.view='shot';g.current_chance_difficulty='hard'
   for kind,focus in (('cross','heading'),('first_time','placed'),('penalty','penalties')):
    c.development['skills'][focus]=dict(level=0,xp=0);g._prepare_next_shot();g.shot_time_limit=4.;g.current_aim_speed=3.
    g._start_opportunity(kind,7);base=(g.shot_time_limit,g.current_aim_speed)
    c.development['skills'][focus]=dict(level=10,xp=0);g._prepare_next_shot();g.shot_time_limit=4.;g.current_aim_speed=3.
    g._start_opportunity(kind,7)
    self.assertGreaterEqual(g.shot_time_limit,base[0]);self.assertLess(g.current_aim_speed,base[1])
 def test_new_tabs_keep_navigation_reachable_at_phone_sizes(self):
  old=Window.size;self.addCleanup(setattr,Window,'size',old)
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   self.sign(g);g._activate_ui('profile');g.draw();settle();g._activate_ui('development')
   for size in ((320,240),(640,360),(1280,591)):
    Window.size=size;g.size=size
    for lang in ('en','pt','de','ja'):
     g.i18n.choose(lang)
     for tab in ('objectives','skills','trust'):
      g._activate_ui('development_tab',tab);g.draw();settle()
      self.assertEqual(g.view,'development')
      for button in g._menu.body.tabs.children:
       self.assertGreaterEqual(button.height,dp(48))
       self.assertGreaterEqual(button.y,g._menu.y-1)
       self.assertLessEqual(button.top,g._menu.top+1)
      self.assertGreaterEqual(g._menu.body.scroll.height,1)
      for w in g._menu.body.children:
       self.assertGreaterEqual(w.y,g._menu.y-1);self.assertLessEqual(w.top,g._menu.top+1)
