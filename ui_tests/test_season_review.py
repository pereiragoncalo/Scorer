import unittest,copy
from kivy.core.window import Window
from test_menus import isolated_game,settle
from season_review import capture,finalize,dismiss
from season_review_ui import SeasonReviewScreen

class SeasonReviewUI(unittest.TestCase):
 def test_layout_uses_frozen_portrait_and_continue_does_not_reset_new_season(self):
  with isolated_game() as g:
   c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting()
   c.current_league.scorer_goals={c.player_name:6,**{f'Rival {i}':20-i for i in range(6)}}
   c._finish_season();g.view='hub';g._career_started=True;c.post_match_stage='';c.title_events['queue']=[]
   c.life['private_meeting']='';g.draw();settle()
   self.assertIsInstance(g._menu.body,SeasonReviewScreen)
   screen=g._menu.body;self.assertIn(f"coach_{c.season_review['portrait']+1:02d}",screen.photo.source)
   season=c.season;goals=c.goals
   for size in ((1280,720),(960,540),(640,360),(640,295)):
    g.size=size;g._menu.size=size;screen.size=size;screen.fit();settle()
    self.assertGreaterEqual(screen.continue_button.height,48)
    self.assertGreaterEqual(screen.continue_button.y,screen.y)
    self.assertLessEqual(screen.continue_button.right,screen.right)
    for label in screen.items:
     self.assertGreater(label.width,0);self.assertGreaterEqual(label.y,screen.y-1)
   g._menu.action('season_review_done');self.assertFalse(c.season_review['pending'])
   self.assertEqual((c.season,c.goals),(season,goals))
 def test_all_nine_languages_fit_the_review_panel(self):
  with isolated_game() as g:
   c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();c._finish_season()
   c.post_match_stage='';c.title_events['queue']=[];c.life['private_meeting']='';g.view='hub';g._career_started=True
   g.i18n.world=True
   for language in ('en','pt','es','de','it','ko','ja','zh','vi'):
    g.i18n.choice=language;g.i18n.revision+=1
    for size in ((1280,720),(640,360),(640,295)):
     g.size=size;g.draw();settle();screen=g._menu.body
     self.assertIsInstance(screen,SeasonReviewScreen)
     for label in screen.items:
      self.assertGreaterEqual(label.y,screen.y-1,(language,size,label.text))
      self.assertLessEqual(label.right,screen.right+1,(language,size,label.text))
     self.assertGreaterEqual(screen.continue_button.height,48)
