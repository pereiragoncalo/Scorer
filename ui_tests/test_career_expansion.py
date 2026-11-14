import unittest,copy,math
from unittest.mock import patch
from kivy.uix.image import Image
from kivy.core.window import Window
from test_menus import isolated_game,settle
import test_retro_attendance_titles as scene_fixture
from career_life import purchase
from celebrations import start,active
import honours,title_events
class ExpansionTests(unittest.TestCase):
 def setUp(self):self.old_window=Window.size
 def tearDown(self):Window.size=self.old_window
 def prepare(self,g):return scene_fixture.RetroSceneTests().prepare(g)
 def test_primary_actions_equal_size_and_aligned(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=self.prepare(g);g.size=(1280,720);Window.size=g.size;g.view='hub';g.draw();settle();d=g._menu.body
   buttons=[d.player_button,d.club_button,d.training,d.play]
   for b in buttons:self.assertAlmostEqual(b.width,buttons[0].width,delta=1);self.assertAlmostEqual(b.height,buttons[0].height,delta=1)
   self.assertAlmostEqual(d.player_button.x,d.training.x,delta=1);self.assertAlmostEqual(d.club_button.x,d.play.x,delta=1);self.assertGreater(d.player_button.y,d.training.y)
 def test_title_carries_extended_arms_and_uses_menu_button(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=self.prepare(g);honours.award(c,dict(season=c.season,competition='cup:qa',title='QA cup',team_uid=c.club.uid,team=c.club.name,country=c.club.country));g.view='trophy';g.draw();g.elapsed+=2.;g.draw()
   from menu_ui import MenuTile
   self.assertIsInstance(g._title_button,MenuTile);self.assertEqual(g._retro_renderer().clocks['title_0'][0].state,'CARRY');self.assertGreaterEqual(g._title_button.height,48)
 def test_title_talk_merge_does_not_repeat_after_newspaper(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=self.prepare(g);c.week+=1;c.life['private_meeting']='offer';c.post_match_stage='newspaper';honours.award(c,dict(season=c.season,competition='cup:qa',title='QA cup',team_uid=c.club.uid,team=c.club.name,country=c.club.country))
   g.view='trophy';g.draw();g._activate_ui('title_continue');g.draw();settle();self.assertEqual(g.view,'title_coach');g._activate_ui('coach_focus',c.coach_focus_options()[0]);g._activate_ui('title_coach_complete');g.draw();settle();self.assertEqual(g.view,'newspaper');g._activate_ui('post_match_continue');g.draw();settle();self.assertEqual(g.view,'hub');self.assertTrue(c.coach_meeting_held);self.assertEqual(c.life['private_meeting'],'')
 def test_hat_trick_slide_and_losing_goal_retrieval_priority(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   self.prepare(g);g._match_shot_goal_counted=False;g.match_player_goals=2;home=g._player_match_is_home();g.match_home_score=g.match_away_score=2;g._record_player_match_goal();self.assertEqual(g.match_player_goals,3);self.assertTrue(g.goal_celebration.decisive);self.assertTrue(g.hattrick_feedback)
   g._match_shot_goal_counted=False;g.match_home_score=0 if home else 5;g.match_away_score=5 if home else 0;g._record_player_match_goal();self.assertTrue(g.goal_celebration.retrieving);self.assertFalse(g.goal_celebration.retrieval.secured);self.assertFalse(g.goal_celebration.decisive)
 def test_coach_has_only_dressing_room_photo(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=self.prepare(g);c.week+=1;g.view='coach';g.draw();settle();images=[w for w in g._menu.body.walk() if isinstance(w,Image)];self.assertEqual(len(images),1);self.assertEqual(images[0].source,'assets/coaches/team_talk.png')
 def test_shop_images_prices_and_local_money_save(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=self.prepare(g);c.life['balance']=100000;g.view='shopping';g.draw();settle();self.assertTrue(any(isinstance(w,Image) and w.source.endswith('/studio.png') for w in g._menu.body.walk()));self.assertTrue(purchase(c,'studio'));self.assertEqual(c.life['balance'],20000);self.assertTrue(c.load());self.assertIn('studio',c.life['owned'])
 def test_penalty_players_wait_legally_and_training_stays_isolated(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   self.prepare(g);g._start_opportunity('penalty',8);self.assertEqual(len(g.field_players),8);self.assertTrue(all(p.y>=16.5 and math.hypot(p.x,p.y-11)>=9.15 for p in g.field_players));g.shot_context='training';g._prepare_next_shot();self.assertEqual(g.field_players,[])

 def test_trophy_continue_accepts_real_touch_after_multiple_redraws(self):
  from kivy.tests.common import UnitTestTouch
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=self.prepare(g);honours.award(c,dict(season=c.season,competition='cup:qa',title='QA cup',team_uid=c.club.uid,team=c.club.name,country=c.club.country));g.view='trophy';g.draw();g.draw();g.draw();settle()
   self.assertIs(g.canvas.children[-1],g._title_button.canvas);t=UnitTestTouch(*g._title_button.center);t.touch_down();t.touch_up();settle();self.assertEqual(g.view,'title_coach')
 def test_competitive_goal_tap_uses_marker_instead_of_free_target(self):
  from kivy.tests.common import UnitTestTouch
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   self.prepare(g);g.state=g.STATE_AIMING;g._menu=None;g._match_notice=None;g.ui_buttons=[];x,y=g.project(3.4,0,2.)
   with patch.object(g,'shoot') as shoot:g.on_touch_down(UnitTestTouch(x,y));shoot.assert_called_once_with()

 def test_lifestyle_from_hub_has_shopping_and_owned_assets(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=self.prepare(g);g.view='hub';g._activate_ui('lifestyle');g.draw();settle();self.assertEqual(g.view,'lifestyle')
   texts=[w.text for w in g._menu.body.walk() if hasattr(w,'text')];self.assertIn('SHOPPING',texts);self.assertIn('MY ASSETS',texts);self.assertFalse(any('studio' in t.lower() for t in texts))
   g._activate_ui('possessions');g.draw();settle();self.assertFalse(any(isinstance(w,Image) for w in g._menu.body.walk()))
   c.life['balance']=100;c.life['owned']={'rose':2};g.view='collection';g._shop_category=2;g._menu._signature=None;g.draw();settle()
   images=[w.source for w in g._menu.body.walk() if isinstance(w,Image)];self.assertEqual(images,['assets/lifestyle/rose.png'])
   g._activate_ui('lifestyle');g._activate_ui('shopping');g.draw();settle();self.assertEqual(g.view,'shopping')
 def test_injury_simulates_fixture_without_training_or_personal_appearance(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=self.prepare(g);c.life.update(injury_name='Ankle sprain',injury_games=2);c.last_training_week=-1;g.view='hub';g.draw();settle()
   self.assertTrue(g._menu.body.training.disabled);self.assertFalse(g._menu.body.play.disabled)
   before=c.matches+c.international_caps;g.start_career_match();settle();self.assertEqual(g.view,'newspaper');self.assertEqual(c.life['injury_games'],1);self.assertEqual(c.matches+c.international_caps,before);self.assertFalse(c.fixture_history[-1]['player_played'])

 def test_season_labels_fit_short_phone_panel(self):
  from kivy.core.text import Label as CoreLabel
  from menu_ui import DashboardField
  from kivy.metrics import Metrics
  old_density=Metrics.density
  try:
   with patch('edition.WORLD_BUILD',True),isolated_game() as g:
    self.prepare(g);Metrics.density=3;Window.size=g.size=(1920,1080);g.view='hub';g.draw();settle()
    for w in g._menu.body.season.walk(restrict=True):
     if isinstance(w,DashboardField):
      m=CoreLabel(text=w.text,text_size=(w.width,None),font_name=w.font_name,font_size=w.font_size,bold=w.bold,line_height=w.line_height);m.refresh();self.assertLessEqual(m.texture.size[1],w.height+1,w.text)
  finally:Metrics.density=old_density
