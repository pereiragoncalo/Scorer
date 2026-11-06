import copy,unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from test_menus import isolated_game,settle
from world_competitions import Tournament
from contextual_help import topics

class ContextualStandingsTests(unittest.TestCase):
    def sign(self,g):
        c=g.career;c.accept_starting_offer(c.offers[0]);c._ensure_competitions();return c
    def test_standings_selector_opens_all_involved_cups_without_simulating_results(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=self.sign(g);g._activate_ui('standings');settle();screen=g._menu.body
            keys={k for k,_ in screen.entries};self.assertIn('domestic:'+c.current_league.country,keys)
            before=copy.deepcopy(c.world_competitions.to_dict());rng=c.rng.getstate()
            screen.choose();settle();self.assertIsNotNone(g._standings_picker);g._on_key_down(Window,27,0,'',[])
            for key,_ in screen.entries:
                g._menu.body.select(key);settle();self.assertTrue(g._menu.body.table.rows)
            self.assertEqual(before,c.world_competitions.to_dict());self.assertEqual(rng,c.rng.getstate())
    def test_group_tables_knockouts_and_aliases_on_small_screen(self):
        old=Window.size
        try:
            Window.size=(640,360)
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                c=self.sign(g);g.size=Window.size
                own=dict(uid=c.club.uid,name=c.club.name,country=c.club.country,tier=1,rating=75)
                others=[dict(uid=t.uid,name=t.name,country=t.country,tier=1,rating=t.rating) for t in c.current_league.clubs if t.uid!=own['uid']][:7]
                cup=Tournament('qa:groups','QA Cup',[own]+others,'groups',groups=2,rounds=6)
                c.world_competitions.tournaments[cup.key]=cup;c.apply_names({'version':1,'clubs':{own['uid']:'Edited club'}})
                g._activate_ui('standings');g._menu.body.select(cup.key);settle()
                screen=g._menu.body;previous=g.standings_group;screen.group(1);settle();self.assertEqual(g.standings_group,(previous+1)%2)
                screen=g._menu.body;screen.tab('fixtures');settle()
                self.assertTrue(any('Edited club' in str(row) for row in g._menu.body.table.rows))
                cup.finish();g._menu._signature=None;g.draw();settle()
                self.assertTrue(g._menu.body.table.rows)
                for button in g._menu.walk():
                    if isinstance(button,Button):self.assertGreaterEqual(button.height,47)
        finally:Window.size=old
    def test_all_normal_screens_have_a_help_button_and_relevant_topics(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=self.sign(g)
            views=('start','offers','hub','profile','training','development','standings','scorers','calendar','agent','world','world_country','world_league','editor','language','club','newspaper','coach','data_notice','leaderboard','competitions','competition','privacy','family','record_safety')
            g.competition_key='ucl';g.world_league_key=c.league_key;g.editor_key=c.league_key
            for view in views:
                g.view=view;g.draw();settle()
                self.assertTrue(any(isinstance(w,Button) and w.text=='HELP' for w in g.walk()),view)
                g._activate_ui('help');settle();self.assertEqual(g._context_help.origin,view);self.assertEqual(g.view,view)
                for label in g._context_help.body.walk():
                    if isinstance(label,Label) and not label.bold:self.assertEqual(label.halign,'justify')
                g._on_key_down(Window,27,0,'',[]);self.assertIsNone(g._context_help)
    def test_help_preserves_profile_draft_and_post_match_gates(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=self.sign(g);g._profile_return='hub';g.view='profile';g.draw();settle();screen=g._menu.body;screen.name.text='Draft Player'
            g._activate_ui('help');g._activate_ui('help');self.assertEqual(g.view,'profile');g._activate_ui('help_back');g.draw();settle()
            self.assertIs(g._menu.body,screen);self.assertEqual(screen.name.text,'Draft Player')
            c.post_match_stage='newspaper';g.view='newspaper';g.draw();g._activate_ui('help');g._activate_ui('help_back');self.assertEqual(c.post_match_stage,'newspaper')
    def test_gameplay_help_pauses_clock_ball_timer_and_blocks_shooting(self):
        with isolated_game(saved=True) as g:
            g.career.load();g.career.attend_coach_meeting();g.start_training();g.draw();settle()
            self.assertIsNotNone(g._game_help);self.assertEqual(g._game_help.parent,g)
            g._activate_ui('help');before=(g.elapsed,g.state_age,g.shot_time_left,g.ball.x,g.ball.y,g.ball.z,g.attempts)
            for _ in range(10):g.update(.1)
            g.shoot();g._on_key_down(Window,ord('r'),0,'r',[])
            self.assertEqual(before,(g.elapsed,g.state_age,g.shot_time_left,g.ball.x,g.ball.y,g.ball.z,g.attempts))
            g._activate_ui('help_back');g.update(.01);self.assertGreater(g.elapsed,before[0])
    def test_help_touch_works_while_match_notice_is_open(self):
        from kivy.tests.common import UnitTestTouch
        with isolated_game(saved=True) as g:
            c=g.career;c.load();c.attend_coach_meeting();c.begin_training()
            for _ in range(3):c.record_training_shot(False)
            c.complete_training(0);g.start_career_match();g.awaiting_chance=True;g.draw();settle()
            self.assertIsNotNone(g._match_notice)
            self.assertLessEqual(g._scoreboard_bounds()[0]+g._scoreboard_bounds()[2],g._game_help.x)
            touch=UnitTestTouch(*g._game_help.center);touch.touch_down();touch.touch_up();settle()
            self.assertIsNotNone(g._context_help);self.assertEqual(g.view,'match')
            g._activate_ui('help_back');self.assertTrue(g.awaiting_chance)

    def test_context_topics_translate_and_do_not_leak_training_focus_elsewhere(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            self.sign(g)
            from contextual_help import TABLE
            for language in ('pt','es','de','it','ko','ja','zh','vi'):
                g.i18n.choose(language);self.assertNotEqual(g.i18n.tr(TABLE),TABLE)
            g.view='training';self.assertTrue(any('FOCUS' in title for title,_ in topics(g)))
            for view in ('hub','profile','development','standings','coach'):
                g.view=view;self.assertFalse(any('FOCUS' in title for title,_ in topics(g)))
