import copy,unittest
from test_menus import isolated_game,settle
from ui_tests.test_player_portrait import PortraitLayoutTests
class PlayerCollectiveTitles(unittest.TestCase):
 def test_collective_count_and_full_history_exclude_individual_awards(self):
  with isolated_game()as g:
   c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True
   def row(season,key,title):return dict(season=season,competition=key,title=title,team_uid=c.club.uid,team=c.club.name,country=c.club.country)
   c.honours['trophies']=[row(2026,'league:test','League'),row(2027,'league:test','League'),row(2027,'cup:test','Cup'),row(2027,'scorer:test','Golden Boot')]
   before=copy.deepcopy(c.honours);g._profile_return='hub';g.view='profile';g.draw();settle();stats=g._menu.body.objectives
   self.assertEqual(len(stats.collective_titles),3);self.assertIn('3',stats.titles_button.text)
   stats.titles_button.dispatch('on_release');settle();popup=stats.titles_popup
   try:
    texts=[getattr(w,'text','')for w in popup.walk()];joined=' '.join(texts)
    self.assertIn('2026/27',joined);self.assertIn('2027/28',joined);self.assertIn('Cup',joined);self.assertNotIn('Golden Boot',joined)
   finally:popup.dismiss()
   self.assertEqual(c.honours,before)
