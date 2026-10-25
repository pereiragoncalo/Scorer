import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.metrics import Metrics,dp
from kivy.uix.scrollview import ScrollView
from menu_ui import PlayerScreen,MenuTile
from test_menus import isolated_game,settle

class PlayerCreationUITests(unittest.TestCase):
    def start(self,g):
        g._activate_ui('splash_continue');g._activate_ui('new_game');g.draw();settle()
        return g._menu.body
    def test_world_search_select_and_commit_use_canonical_independent_countries(self):
        with patch('edition.WORLD_BUILD',True),patch('main.phone_country',return_value='Portugal'),patch('main.phone_locale_tag',return_value='pt-PT'),isolated_game() as g:
            form=self.start(g);form.name.text='marco costa';before=(g.career.nationality,g.career.league_key,list(g.career.offers),g.career.rng.getstate())
            for field,query,key in [('nationality','Brasil','Brazil'),('country','México','Mexico')]:
                form.choose_country(field);p=g._country_popup;p.search.text=query;settle()
                self.assertFalse(any(isinstance(w,ScrollView) for w in p.walk()))
                next(w for w in p.grid.children if isinstance(w,MenuTile)).dispatch('on_release');settle()
                self.assertEqual(form.draft[field],key)
            self.assertEqual((g.career.nationality,g.career.league_key,g.career.offers,g.career.rng.getstate()),before)
            form.submit();self.assertEqual(g.view,'offers');self.assertEqual((g.career.player_name,g.career.nationality,g.career.current_league.country),('Marco Costa','Brazil','Mexico'))
            self.assertFalse(g.career.save_path.exists())
            g._activate_ui('accept_offer',g.career.offers[0]);self.assertTrue(g.career.save_path.exists())
            g.view='start';g._load_career();self.assertEqual(g.view,'hub');self.assertTrue(g._career_started)
            self.assertEqual((g.career.nationality,g.career.current_league.country),('Brazil','Mexico'))
    def test_draft_survives_validation_and_rebuild_and_picker_cancel_does_not_apply(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            f=self.start(g);f.draft['nationality']='Japan';f.draft['country']='England';f.submit();g.draw();settle()
            self.assertEqual(g.view,'profile');f=g._menu.body;self.assertEqual(f.draft['nationality'],'Japan')
            f.name.text='Nguyễn Minh';g._menu._build();settle();f=g._menu.body
            self.assertEqual(f.name.text,'Nguyễn Minh');f.choose_country('country');g._country_popup.dismiss();settle();self.assertEqual(f.draft['country'],'England')
            f.submit();self.assertEqual(g.career.league_key,'England|4');self.assertEqual(g.career.nationality,'Japan')
    def test_world_profile_and_country_controls_fit_phone_sizes(self):
        old=Window.size;density=Metrics.density
        try:
            Metrics.density=1.6
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                self.start(g)
                for size in [(1280,640),(640,360),(360,640)]:
                    Window.size=size;g.size=size;g.draw();settle();f=g._menu.body
                    self.assertIsInstance(f,PlayerScreen);self.assertIsNone(g._menu.scroll)
                    for w in [f.name,f.choices,f.actions]:
                        self.assertGreaterEqual(w.y,f.panel.y-1);self.assertLessEqual(w.top,f.panel.top+1);self.assertGreaterEqual(w.height,dp(48)-1)
                    f.choose_country('country');p=g._country_popup;settle()
                    for w in [p.search,*p.grid.children,p.previous,p.next]:
                        self.assertGreaterEqual(w.height,dp(48)-1);self.assertGreaterEqual(w.y,p.y-1);self.assertLessEqual(w.top,p.top+1)
                    p.dismiss();settle()
        finally:Window.size=old;Metrics.density=density
    def test_free_and_existing_world_profile_have_name_only(self):
        with isolated_game() as g:
            f=self.start(g);self.assertFalse(f.world_creation);self.assertFalse(hasattr(f,'country_buttons'))
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            g.career.accept_starting_offer(g.career.offers[0]);g.view='hub';g._activate_ui('profile');g.draw();settle()
            f=g._menu.body;self.assertFalse(f.world_creation);self.assertFalse(hasattr(f,'country_buttons'))
