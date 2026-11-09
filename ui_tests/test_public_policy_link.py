import unittest
from unittest.mock import patch
from test_menus import isolated_game,settle

class PublicPolicyLinkTests(unittest.TestCase):
 def test_settings_opens_the_independent_https_policy(self):
  with isolated_game(saved=True) as game:
   game.view='privacy';game.draw();settle();before=game.career.save_path.read_bytes()
   with patch('webbrowser.open') as browser:
    game._activate_ui('open_privacy_policy')
   browser.assert_called_once_with('https://pereiragoncalo.github.io/Scorer/privacy/')
   self.assertEqual(game.career.save_path.read_bytes(),before)
