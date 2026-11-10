import unittest
from unittest.mock import patch
from kivy.core.window import Window
from menu_ui import ClubButton
from test_menus import isolated_game,settle
from tools.play.fictional_clubs import shipping_data
from pathlib import Path

class CityColourUITests(unittest.TestCase):
 def test_current_club_label_and_real_home_palette_stay_together(self):
  data=shipping_data(Path(__file__).resolve().parents[1]/'assets/data')
  with patch('world_clubs.catalogue',return_value=data['world_clubs']['clubs']),patch('club_profiles.catalogue',return_value=data['club_profiles']['clubs']),patch('edition.WORLD_BUILD',True),isolated_game() as g:
   g._select_career_mode('world');c=g.career
   cases=[('c8d6431e000ec7467295','Lisboa Vermelho'),('00d46be2fe2f866aca10','Lisboa Verde'),('d3811223093359dac065','Porto Azul'),('f9554f2ce1ab5ff99892','Salvador Vermelho-Preto')]
   for uid,label in cases:
    league,club=next((l,t) for l in c.leagues.values() for t in l.clubs if t.uid==uid)
    c.league_key=league.key;c.club_name=club.name;c.attend_coach_meeting();before=c.kit_for_club(club);g.view='hub';g.draw();settle()
    button=g._menu.body.club_button;self.assertIsInstance(button,ClubButton)
    self.assertEqual(button.text,label);self.assertEqual(button.club_kit,before)
    self.assertEqual((club.uid,club.name),(uid,data['world_clubs']['clubs'][uid]['canonical']))
