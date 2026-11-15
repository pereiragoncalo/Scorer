import unittest
from unittest.mock import patch
from kivy.uix.label import Label
from test_menus import isolated_game,settle
from international_calendar import match_date
from club_calendar import upcoming_date
class RealFixtureDates(unittest.TestCase):
 def test_competition_and_hub_show_dated_fixtures(self):
  with patch('edition.WORLD_BUILD',True),isolated_game()as g:
   c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True
   g._activate_ui('competitions');g._activate_ui('competition_open','nations_a');settle()
   cup=c.world_competitions.tournaments['nations_a'];text=g.i18n.date(match_date(c.season,cup,cup.fixtures[0]))
   self.assertTrue(any(text in w.text for w in g.walk()if isinstance(w,Label)))
   g.view='hub';g.draw();settle();fixture=c.next_match();text=g.i18n.date(upcoming_date(c,fixture))
   self.assertTrue(any('NEXT MATCH'in w.text and text in w.text for w in g.walk()if isinstance(w,Label)))
