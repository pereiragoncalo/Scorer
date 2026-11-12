import unittest
from kivy.core.window import Window
from kivy.metrics import Metrics,dp
from kivy.uix.scrollview import ScrollView
from test_menus import isolated_game,settle

class PortraitLayoutTests(unittest.TestCase):
 def test_caption_moves_with_photo_and_keeps_editable_name_and_stats_on_screen(self):
  old_size=Window.size;old_density=Metrics.density
  try:
   for size,density in (((1280,591),1.6),((960,540),1.6),((640,360),1.0)):
    Metrics.density=density;Window.size=size
    with isolated_game() as g:
     c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True;g._profile_return='hub';g.view='profile';g.size=size;g.draw();settle()
     screen=g._menu.body;stats=screen.objectives;photo=stats.portrait
     self.assertEqual(stats.cols,3);self.assertIs(screen.name.parent,photo.parent)
     self.assertIs(screen.contract_info.parent,photo.parent);self.assertGreater(photo.texture.width,0)
     self.assertGreater(photo.height,dp(40));self.assertGreaterEqual(photo.x,stats.center_x)
     self.assertLessEqual(screen.name.top,photo.y+1);self.assertLessEqual(stats.age_info.top,screen.name.y+1)
     self.assertLessEqual(stats.contract_info.top,stats.age_info.y+1)
     for w in (photo,screen.name,stats.age_info,stats.contract_info,screen.actions):
      self.assertGreaterEqual(w.y,-1);self.assertLessEqual(w.top,g.height+1)
     self.assertFalse(any(isinstance(w,ScrollView) for w in screen.walk()))
     before=c.goals,c.life['salary'],dict(c.life['owned']);screen.name.text='Portrait Name';screen.submit()
     self.assertEqual(c.player_name,'Portrait Name');self.assertEqual((c.goals,c.life['salary'],c.life['owned']),before)
  finally:Metrics.density=old_density;Window.size=old_size
