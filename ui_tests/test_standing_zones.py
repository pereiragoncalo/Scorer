import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.metrics import Metrics,dp
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from menu_ui import CompactTable,MenuTile,ZONE_COLOURS,GREEN
from test_menus import isolated_game,settle

class StandingZoneUITests(unittest.TestCase):
    def world(self,g):
        g.career.choose_start_country('Portugal');g.career.accept_starting_offer(g.career.offers[0]);g._career_started=True
    def table(self,g,key=None):
        if key:g.world_league_key=key;g.view='world_league'
        else:g.view='standings'
        g.draw();settle();return next(w for w in g.walk() if isinstance(w,CompactTable))
    def test_portugal_zones_colours_rules_and_readonly_browsing(self):
        old=Window.size
        try:
            Window.size=(1280,640)
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                self.world(g);g.career.club_name=g.career.current_league.table()[8].name;g.career.save();rng=g.career.rng.getstate();save=g.career.save_path.read_bytes();identity=g.career.league_key
                t=self.table(g);self.assertEqual([r[0] for r in t.rows[:8]],['1 P','2 P','3 P','4 PO','5 PO','6 PO','7 PO',8])
                self.assertFalse(t.zones.relegation)
                hero=next(w for row in t.lines.children for w in row.children if isinstance(w,Label) and w.text==g.career.display_text(g.career.club_name))
                self.assertNotEqual(tuple(hero.color),GREEN)
                for row in t.lines.children:
                    if row.standing_zone:
                        label=next(w for w in row.children if isinstance(w,Label) and w.text.endswith((' P',' PO')))
                        self.assertEqual(tuple(label.color),ZONE_COLOURS[row.standing_zone])
                t.show_rules();settle();p=t.rules_popup;texts={w.text for w in p.walk() if isinstance(w,Label)}
                self.assertIn(g.i18n.tr('PO: Playoff (simulated) {places}',places='4-7'),texts)
                self.assertIn(g.i18n.tr('R: No relegation'),texts);p.dismiss();settle()
                t=self.table(g,'Portugal|2');self.assertEqual([r[0] for r in t.rows[-2:]],['17 R','18 R']);t.move(t.pages-1);settle()
                self.assertIn('relegation',{r.standing_zone for r in t.lines.children})
                t.toggle_detail();settle();self.assertIn('relegation',{r.standing_zone for r in t.lines.children})
                t=self.table(g,'Portugal|1');self.assertFalse(t.zones.promotion);self.assertFalse(t.zones.playoff)
                self.assertEqual(g.career.rng.getstate(),rng);self.assertEqual(g.career.save_path.read_bytes(),save);self.assertEqual(g.career.league_key,identity)
        finally:Window.size=old
    def test_simplified_model_marks_both_divisions_and_explicit_no_playoffs(self):
        with patch('edition.WORLD_BUILD',True),patch('main.phone_locale_tag',return_value='pt-PT'),isolated_game() as g:
            self.world(g)
            for key,up,down in [('Yemen|1',(),(10,11,12)),('Yemen|2',(1,2,3),())]:
                t=self.table(g,key);self.assertEqual(t.zones.promotion,up);self.assertEqual(t.zones.relegation,down);self.assertFalse(t.zones.playoff)
                t.show_rules();settle();p=t.rules_popup
                self.assertIn(g.i18n.tr('PO: No playoffs'),{w.text for w in p.walk() if isinstance(w,Label)})
                p.dismiss();settle()
    def test_zone_tables_fit_without_scroll_and_keep_controls_accessible(self):
        old=Window.size;density=Metrics.density
        try:
            Metrics.density=1.6
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                self.world(g)
                for size in [(1280,640),(640,360),(360,640)]:
                    Window.size=size;g.size=size;g._menu._signature=None;t=self.table(g)
                    self.assertFalse(any(isinstance(w,ScrollView) for w in t.walk()))
                    for w in [t.zone_legend,*[c for c in t.controls.children if isinstance(c,MenuTile)]]:
                        self.assertGreaterEqual(w.height,dp(48)-1);self.assertGreaterEqual(w.width,dp(48)-1,(size,getattr(w,'text',''),w.size))
                        self.assertGreaterEqual(w.y,t.y-1);self.assertLessEqual(w.top,t.top+1)
                    for row in t.lines.children:
                        self.assertGreaterEqual(row.y,t.controls.top-1);self.assertLessEqual(row.top,t.head.y+1)
                    t.show_rules();settle();p=t.rules_popup
                    self.assertGreaterEqual(p.back.y,p.y-1);self.assertLessEqual(p.back.top,p.top+1)
                    p.dismiss();settle()
        finally:Window.size=old;Metrics.density=density
    def test_free_standings_keep_one_division_without_movement_markers(self):
        with isolated_game(saved=True) as g:
            g.view='start';g._load_career();t=self.table(g)
            self.assertIsNone(t.zones);self.assertFalse(hasattr(t,'zone_legend'))
            self.assertTrue(all(type(r[0]) is int for r in t.rows))
