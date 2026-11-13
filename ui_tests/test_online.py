import unittest
from unittest.mock import patch
from test_menus import isolated_game,settle

class OnlineUITests(unittest.TestCase):
    def test_leaderboard_is_direct_read_only_and_old_join_does_not_publish(self):
        with isolated_game(saved=True) as g:
            g.family.social=False
            with patch.object(g.leaderboard,'request',return_value=dict(schema=5,division=1,entries=[])) as request:
                g.view='hub';g._activate_ui('leaderboard');settle()
                self.assertEqual(g.view,'leaderboard');g._activate_ui('leaderboard_join');settle()
                self.assertFalse(g.leaderboard.enabled);self.assertIsNone(g._records_popup)
                self.assertTrue(all(call.args[0].startswith('/v5/records?')and len(call.args)==1 for call in request.call_args_list))
    def test_end_of_season_asks_for_name_only_after_explicit_publication(self):
        from season_sharing import ask_name
        with isolated_game(saved=True) as g:
            c=g.career;c.load();c._finish_season();c.post_match_stage='';c.title_events['queue']=[];c.life['private_meeting']=''
            c.season_review['public_records']=[dict(division=2,season=c.season-1,player=c.player_name,goals=8)]
            g.view='hub';g._career_started=True;g.draw();settle();name=c.player_name
            self.assertIsNotNone(g._menu.body.publish_button)
            with patch.object(g.leaderboard,'flush_approved'):
                ask_name(g._menu);settle();popup=g._season_share_popup
                self.assertEqual(popup.name_field.text,'');popup.confirm();self.assertTrue(c.season_review['pending'])
                popup.name_field.text='Chosen public name';popup.confirm();settle()
            self.assertIsNone(g._season_share_popup);self.assertFalse(c.season_review['pending']);self.assertEqual(c.player_name,name)
            self.assertEqual(g.leaderboard.approved_seasons[0]['record']['player'],'Chosen public name')
            self.assertFalse(g.family.social)

    def test_main_menu_exposes_leaderboard_without_enabling_any_collection(self):
        from kivy.uix.button import Button
        from kivy.core.window import Window
        for world in (False,True):
            with patch('edition.WORLD_BUILD',world),isolated_game(saved=True) as g:
                g.view='hub';g.draw();settle()
                labels={w.text for w in g.walk() if isinstance(w,Button)}
                self.assertIn('LEADERBOARD',labels)
                self.assertFalse(g.leaderboard.enabled);self.assertFalse(g.usage.enabled)

    def test_records_layout_has_separate_controls_table_and_pages_at_phone_sizes(self):
        from kivy.core.window import Window
        from kivy.metrics import Metrics,dp
        from kivy.uix.scrollview import ScrollView
        from menu_ui import SeasonRecordsScreen
        old=Metrics.density;old_size=Window.size
        try:
            for density,size in ((1,(640,360)),(1.64,(1280,591)),(1,(320,240)),(1,(1366,697))):
                Metrics.density=density;Window.size=size
                with isolated_game(saved=True) as g:
                    g.size=size;g.view='leaderboard'
                    g.leaderboard.entries=[dict(player='João Silva '+str(i),goals=30-i,publisher=f'{i:032x}') for i in range(20)]
                    g.draw();settle();screen=g._menu.body
                    self.assertIsInstance(screen,SeasonRecordsScreen)
                    self.assertFalse(any(isinstance(w,ScrollView) for w in g._menu.walk()))
                    self.assertLessEqual(screen.table.top,screen.status.y+1)
                    self.assertEqual(len(screen.category_buttons),2)
                    from kivy.uix.textinput import TextInput
                    self.assertFalse(any(isinstance(w,TextInput)for w in screen.walk()))
                    self.assertGreaterEqual(screen.table.controls.height,dp(48)-1)
                    for row in screen.table.lines.children:
                        self.assertGreaterEqual(row.y,screen.table.controls.top-1)
                        self.assertLessEqual(row.top,screen.table.head.y+1)
                    from kivy.uix.boxlayout import BoxLayout
                    records=[w for w in screen.table.lines.children if isinstance(w,BoxLayout)]
                    if records:self.assertLessEqual(abs(max(w.top for w in records)-screen.table.head.y),dp(5))
                    if len(screen.table.rows)>screen.table.page_size:
                        screen.table.move(1);settle();self.assertEqual(screen.table.page,1)
        finally:Metrics.density=old;Window.size=old_size
