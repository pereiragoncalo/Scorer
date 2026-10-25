import unittest
from kivy.core.window import Window
from kivy.uix.label import Label
from test_menus import isolated_game,settle

class CleanMenuTests(unittest.TestCase):
    def texts(self,g):return {w.text for w in g.walk() if isinstance(w,Label)}
    def test_normal_menus_show_controls_and_data_without_boilerplate(self):
        with isolated_game(saved=True) as g:
            g.view='start';g.draw();settle()
            self.assertIn('NEW GAME',self.texts(g))
            self.assertFalse(any('Google test ads' in t or 'One division.' in t for t in self.texts(g)))
            g._load_career();g.draw();settle()
            self.assertIn('TRAINING',self.texts(g));self.assertIn('PLAY',self.texts(g))
            self.assertNotIn('Complete weekly training to unlock Play.',self.texts(g))
            self.assertNotIn(g.career.message,self.texts(g))
            g._activate_ui('profile');g.draw();settle()
            self.assertNotIn('Choose your name. Your progress is kept.',self.texts(g))
            g.view='training';g.draw();settle()
            self.assertIn('WATCH AD: +1 MORALE',self.texts(g))
            self.assertNotIn('Optional ad: +1 morale after completion. Once per week, max 20.',self.texts(g))
    def test_load_name_and_save_errors_remain_visible(self):
        with isolated_game(corrupt=True) as g:
            g.view='start';g._load_career();g.draw();settle()
            self.assertIn('Unable to load this career. Your previous save has been preserved.',self.texts(g))
        old=Window.size
        try:
            Window.size=(1280,640)
            with isolated_game(saved=True) as g:
                g.view='start';g._load_career();g._activate_ui('profile');g._activate_ui('save_profile','');g.draw();settle()
                self.assertIn('Enter a name with at least 2 characters.',self.texts(g))
                g.view='hub';g.career.message='Unable to save your career. Please try again.';g.draw();settle()
                self.assertIn(g.career.message,self.texts(g))
        finally:Window.size=old
