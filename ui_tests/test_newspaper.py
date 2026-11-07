import copy,unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.image import Image
from newspaper import PHOTOS
from menu_ui import MenuTile
from newspaper_ui import NewspaperScreen
from test_menus import isolated_game,settle


class NewspaperUI(unittest.TestCase):
    def played(self,g,goals=0,misses=1):
        c=g.career;c.accept_starting_offer(c.offers[0]);c.attend_coach_meeting();g._career_started=True
        h,a=c.next_fixture();score=[1,1];score[0 if h.uid==c.club.uid else 1]=goals if goals>=2 else 1
        c.finish_match(h,a,goals,misses,forced_score=tuple(score));return c

    def test_button_opens_real_last_score_paper_photo_and_back(self):
        with isolated_game() as g:
            c=self.played(g,2,0);g.view='hub';g.draw();settle()
            self.assertEqual(g.view,'newspaper')
            g._activate_ui('newspaper');g.draw();settle();paper=g._menu.body
            self.assertIsInstance(paper,NewspaperScreen);self.assertTrue(paper.article['mentions_player'])
            texts=[w.text for w in paper.walk() if isinstance(w,Label)]
            printed=''.join(part['text'] for page in paper.pages for part in page)
            self.assertIn(''.join(c.player_name.split()),''.join(printed.split()));self.assertTrue(any('2-1' in t or '1-2' in t for t in texts))
            self.assertEqual(paper.photo.source,PHOTOS[0]);self.assertLessEqual(paper.photo.width,240)
            c.life['private_meeting']='';g._activate_ui('hub');self.assertEqual(g.view,'coach')

    def test_ordinary_player_is_omitted_aliases_are_used_and_opening_is_read_only(self):
        with patch('edition.WORLD_BUILD',True),isolated_game() as g:
            c=self.played(g);r=c.press_state['report'];c.display_aliases['clubs'][r['home_uid']]='Imported Home';c.alias_revision+=1
            state=copy.deepcopy(c.press_state);rng=c.rng.getstate()
            for _ in range(2):
                g._activate_ui('newspaper');g.draw();settle();p=g._menu.body
                self.assertFalse(p.article['mentions_player']);self.assertIn('Imported Home',' '.join(p.article['paragraphs']))
                self.assertNotIn(c.player_name,' '.join(p.article['paragraphs']))
            self.assertEqual(c.press_state,state);self.assertEqual(c.rng.getstate(),rng)

    def test_small_layouts_and_all_nine_languages_keep_back_reachable(self):
        old=Window.size
        try:
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                self.played(g,2,0)
                for size in ((320,240),(640,360),(360,640)):
                    Window.size=size;g.size=size
                    for lang in ('en','pt','es','de','it','ko','ja','zh','vi'):
                        g.i18n.choose(lang);g._activate_ui('newspaper');g.draw();settle()
                        p=g._menu.body;self.assertIsInstance(p,NewspaperScreen);self.assertIsNone(p.scroll);self.assertTrue(p.layout_fits,(size,lang))
                        back=next(w for w in p.walk() if isinstance(w,MenuTile))
                        x,y=back.to_window(back.x,back.y)
                        self.assertGreaterEqual(y,0);self.assertLessEqual(y+back.height,size[1]+1);self.assertGreaterEqual(back.height,48)
                        self.assertGreaterEqual(p.photo.width,40);self.assertLessEqual(p.photo.width,size[0])
        finally:Window.size=old

    def test_empty_new_career_has_no_invented_news_or_photo(self):
        with isolated_game() as g:
            g.career.accept_starting_offer(g.career.offers[0]);g.career.attend_coach_meeting();g._activate_ui('newspaper');g.draw();settle()
            self.assertFalse(any(isinstance(w,Image) for w in g._menu.body.walk()))
            printed=''.join(part['text'] for page in g._menu.body.pages for part in page)
            self.assertIn('firstmatchreport',''.join(printed.split()))

    def test_actual_goal_minutes_enter_report_once_and_ai_minutes_use_event_time(self):
        with isolated_game(saved=True) as g:
            g.career.load();g.career.last_training_week=g.career.week;g.start_career_match()
            g.match_chance_minutes=[];g.match_report_events=[];g.match_half=2;g.match_first_stoppage=2;g.match_minute=87
            g.match_goal_events=[(88,'away')];g.match_goal_event_index=0;g._update_career_match(1)
            self.assertEqual(g.match_report_events,[dict(minute=86,half=2,side='away')])
            g._match_shot_goal_counted=False;g._record_player_match_goal();g._record_player_match_goal()
            self.assertEqual(len(g.match_report_events),2)
            self.assertEqual(g.match_report_events[-1]['minute'],88)


    def test_entire_page_fits_with_long_names_and_negative_story_without_scroll(self):
        from kivy.uix.scrollview import ScrollView
        from newspaper_ui import text_height
        old=Window.size
        try:
            Window.size=(320,240)
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                c=self.played(g);g.size=(320,240);r=c.press_state['report']
                r['negative_run']=12;r['standout']=False;r['goals']=0
                for lang,char in (('en','W'),('de','W'),('pt','W'),('ja','選'),('ko','선'),('zh','名')):
                    c.display_aliases['clubs'][r['home_uid']]=char*56
                    c.display_aliases['clubs'][r['away_uid']]=char*55+'B'
                    c.player_name=char*40;g.i18n.choose(lang);g._activate_ui('newspaper');g.draw();settle();p=g._menu.body
                    self.assertFalse(any(isinstance(w,ScrollView) for w in p.walk()))
                    self.assertTrue(p.layout_fits,(lang,p.body.y,p.y,p.body.text,p.headline.text))
                    self.assertGreaterEqual(p.body_font_size,6)
                    self.assertIn(c.player_name,p.story_text)
                    printed=''.join(part['text'] for page in p.pages for part in page)
                    self.assertEqual(''.join(printed.split()),''.join(p.story_text.split()))
                    for label in (p.headline,p.score,p.body,p.dateline):
                        self.assertFalse(label.shorten)
                        self.assertGreaterEqual(label.y,p.y-1,(lang,label.text))
                        self.assertLessEqual(label.top,p.top+1)
                        required=text_height(str(label.text),round(label.width),label.font_name,round(label.font_size,2),label.bold)
                        self.assertLessEqual(required,label.height+1,(lang,label.text))
        finally:Window.size=old


    def test_folded_window_embedded_photo_and_custom_fonts(self):
        old=Window.size
        try:
            Window.size=(1280,720)
            with isolated_game() as g:
                c=self.played(g,2,0);g.size=(1280,720);g._activate_ui('newspaper');g.draw();settle();p=g._menu.body
                x,y,w,h=p.sheet_bounds
                self.assertGreater(x,p.x);self.assertGreater(y,p.y);self.assertLess(w,p.width);self.assertLess(h,p.height)
                self.assertIn('ScorerRetro',p.masthead.font_name)
                self.assertTrue(all('ScorerRetro' in part['font'] for page in p.pages for part in page))
                self.assertLess(p.photo.right,p.fragments[0].x)
                self.assertTrue(p.layout_fits)
        finally:Window.size=old

    def test_all_four_goals_and_summary_survive_flow_and_leaf_turns(self):
        old=Window.size
        try:
            Window.size=(320,240)
            with isolated_game() as g:
                c=self.played(g);g.size=(320,240);r=c.press_state['report'];r['score']=[3,1];r['status']='3-1'
                r['events']=[dict(minute=m,half=1 if m<46 else 2,side=s) for m,s in ((32,'home'),(51,'away'),(67,'home'),(90,'home'))]
                g._activate_ui('newspaper');g.draw();settle();p=g._menu.body
                self.assertEqual(len(p.article['goals']),4)
                printed=''.join(part['text'] for page in p.pages for part in page)
                self.assertEqual(''.join(printed.split()),''.join(p.story_text.split()))
                for event in p.article['goals']:self.assertIn(event['minute']+"'",printed)
                self.assertEqual(len(p.pages),1)
                self.assertTrue(p.layout_fits)
                if len(p.pages)>1:
                    p.turn(1);settle();self.assertEqual(p.page,1);self.assertTrue(p.layout_fits)
        finally:Window.size=old


    def test_example_four_goal_report_fits_original_phone_proportions(self):
        from kivy.metrics import Metrics
        old=Window.size;density=Metrics.density
        try:
            Metrics.density=1.4;Window.size=(1280,591)
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                c=self.played(g);g.size=(1280,591);g.i18n.choose('pt');r=c.press_state['report']
                c.display_aliases['clubs'][r['home_uid']]='Ponte Preta';c.display_aliases['clubs'][r['away_uid']]='Londrina'
                r['score']=[3,1];r['status']='3-1';r['negative_run']=6;r['goals']=0;r['standout']=False
                r['events']=[dict(minute=m,half=1 if m<46 else 2,side=s) for m,s in ((32,'home'),(51,'away'),(67,'home'),(90,'home'))]
                g._activate_ui('newspaper');g.draw();settle();p=g._menu.body
                self.assertEqual(len(p.pages),1);self.assertTrue(p.layout_fits);self.assertEqual(len(p.article['goals']),4)
        finally:Metrics.density=density;Window.size=old

    def test_no_caption_and_story_reclaims_space_beside_and_below_photo(self):
        old=Window.size
        try:
            Window.size=(1280,591)
            with patch('edition.WORLD_BUILD',True),isolated_game() as g:
                self.played(g,2,0);g.size=Window.size;g.i18n.choose('en')
                g._activate_ui('newspaper');g.draw();settle();p=g._menu.body
                self.assertIsNone(p.caption)
                self.assertFalse(any(isinstance(w,Label) and w.text==g.i18n.tr('Illustration') for w in p.walk()))
                beside=[w for w in p.fragments if w.x>=p.photo.right]
                below=[w for w in p.fragments if w.x<p.photo.right and w.top<=p.photo.y]
                self.assertTrue(beside);self.assertTrue(below)
                self.assertTrue(p.layout_fits);self.assertEqual(len(p.pages),1)
                printed=''.join(w.text for w in p.fragments)
                self.assertEqual(''.join(printed.split()),''.join(p.story_text.split()))
        finally:Window.size=old
