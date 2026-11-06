import unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from test_menus import isolated_game,settle
class WorldCompetitionUI(unittest.TestCase):
    def test_competitions_page_fixture_pagination_table_groups_and_back(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            g.career.accept_starting_offer(g.career.offers[0]);g._activate_ui('competitions');settle();self.assertEqual(g.view,'competitions')
            g._activate_ui('competition_open','ucl');settle();self.assertEqual(g.view,'competition');self.assertIsNotNone(g._menu.scroll)
            before={w.text for w in g.walk() if isinstance(w,Label)}
            g._activate_ui('competition_page',1);settle();self.assertEqual(g.competition_page,1);self.assertNotEqual(before,{w.text for w in g.walk() if isinstance(w,Label)})
            g._activate_ui('competition_tab','table');settle();self.assertTrue(any('Group 1' in w.text for w in g.walk() if isinstance(w,Label)))
            g._activate_ui('competitions_back');self.assertEqual(g.view,'competitions');g._activate_ui('competitions_back');self.assertEqual(g.view,'world')
    def test_national_calendar_and_secondary_cups_are_browsable(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            g.career.accept_starting_offer(g.career.offers[0]);g._activate_ui('competitions');settle()
            texts={w.text for w in g.walk() if isinstance(w,Label)}
            self.assertTrue({'FIFA World Cup','Copa America','OFC Nations Cup','2030'}<=texts)
            for key in ('sudamericana','caf_confederation','afc_two','afc_challenge'):
                g._activate_ui('competition_open',key);settle()
                self.assertEqual(g.view,'competition');self.assertIsNotNone(g._menu.scroll)
                g._activate_ui('competition_tab','table');settle()
                self.assertTrue(any('Group 1' in w.text for w in g.walk() if isinstance(w,Label)))
                g._activate_ui('competitions_back');settle()

    def test_away_national_goal_updates_correct_scoreboard_side(self):
        from career import CareerClub
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            g.career.accept_starting_offer(g.career.offers[0]);g.career.nationality='Argentina';g.match_competition='world|friendly|x';g.match_is_international=True
            g.match_home=CareerClub('Brazil','Brazil','National Team',1,90,uid='nation:Brazil');g.match_away=CareerClub('Argentina','Argentina','National Team',1,90,uid='nation:Argentina')
            g._match_shot_goal_counted=False;g.match_home_score=g.match_away_score=0;g._record_player_match_goal()
            self.assertEqual((g.match_home_score,g.match_away_score),(0,1));g._record_player_match_goal();self.assertEqual(g.match_away_score,1)
    def test_imported_aliases_are_used_for_cross_country_cup_and_calendar(self):
        from menu_ui import CompactTable
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            g.career.accept_starting_offer(g.career.offers[0]);g._activate_ui('competitions');cup=g.career.world_competitions.tournaments['ucl'];f=cup.fixtures[0]
            g.career.apply_names({'version':1,'clubs':{f['home']:'Imported Cross Country Club'}})
            g._activate_ui('competition_open','ucl');settle()
            self.assertTrue(any('Imported Cross Country Club' in w.text for w in g.walk() if isinstance(w,Label)))
            g.career.fixture_history.append({'date':g.career.current_date.isoformat(),'competition':cup.title,'country':'Portugal','home':cup.teams[f['home']]['name'],'away':cup.teams[f['away']]['name'],'home_uid':f['home'],'away_uid':f['away'],'status':'1-0','played':True})
            g.view='calendar';g.draw();settle();table=next(w for w in g.walk() if isinstance(w,CompactTable))
            self.assertTrue(any('Imported Cross Country Club' in str(row) for row in table.rows))

    def test_phone_views_and_translations_keep_actions_accessible(self):
        old=Window.size
        try:
            Window.size=(320,240)
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                g.size=(320,240);g.career.accept_starting_offer(g.career.offers[0]);g._activate_ui('competitions')
                for lang in ('en','pt','es','de','it','ko','ja','zh','vi'):
                    g.i18n.choose(lang)
                    for view in ('competitions','competition'):
                        g.competition_key='ucl';g.view=view;g.draw();settle();self.assertIsNotNone(g._menu.scroll)
                        for w in g._menu.body.walk():
                            if isinstance(w,Button):self.assertGreaterEqual(w.height,47)
                    if lang!='en':self.assertNotEqual(g.i18n.tr('VIEW COMPETITION'),'VIEW COMPETITION')
        finally:Window.size=old
