"""Responsive paper-style reader, with a fixed Back action and offline photos."""
from pathlib import Path
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from menu_ui import FlowLabel, MenuTile
from newspaper import article,current_report

INK=(.10,.09,.075,1)
MUTED=(.34,.30,.25,1)


class NewspaperScreen(BoxLayout):
    def __init__(self,menu):
        super().__init__(orientation='vertical',padding=dp(12),spacing=dp(8))
        g=menu.game;c=g.career;loc=g.i18n
        with self.canvas.before:
            Color(.96,.935,.875,1);self.paper=Rectangle(pos=self.pos,size=self.size)
        self.bind(pos=self._paper,size=self._paper)
        bar=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(12))
        bar.add_widget(FlowLabel(text='NEWSPAPER',color=INK,font_size=sp(14),bold=True))
        back=MenuTile('BACK',lambda:menu.action('hub'));back.size_hint_x=None;back.width=dp(100);bar.add_widget(back)
        self.add_widget(bar)
        self.scroll=ScrollView(do_scroll_x=False,bar_width=dp(4))
        self.story=BoxLayout(orientation='vertical',size_hint_y=None,spacing=dp(12),padding=[dp(8),0,dp(8),dp(24)])
        self.story.bind(minimum_height=self.story.setter('height'));self.scroll.add_widget(self.story);self.add_widget(self.scroll)
        self.story.add_widget(FlowLabel(text='SCORER DAILY',localize=False,color=INK,font_size=sp(34),bold=True,halign='center',font_name='assets/fonts/BarlowCondensed-ExtraBoldItalic.ttf'))
        self.rule()
        report=current_report(c)
        if report is None:
            self.story.add_widget(FlowLabel(text='Your first match report will appear here after you play.',color=INK,font_size=sp(18)))
            return
        def team(entry,side):
            uid=entry.get(side+'_uid','')
            if uid.startswith('nation:'):return loc.country(uid[7:])
            club=next((cl for league in c.leagues.values() for cl in league.clubs if cl.uid==uid),None) if uid else None
            return c.display_club(club) if club else c.display_text(entry.get(side,''),entry.get('country'))
        competition=loc.competition(c,report['competition'],report['country'])
        data=article(report,loc.tr,team,c.player_name,competition)
        self.article=data
        self.story.add_widget(FlowLabel(text=report['date']+'  ·  '+str(competition),localize=False,color=MUTED,font_size=sp(12)))
        self.story.add_widget(FlowLabel(text=data['headline'],localize=False,color=INK,font_size=sp(27),bold=True))
        score=team(report,'home')+'  '+loc.tr(report['status'])+'  '+team(report,'away')
        self.story.add_widget(FlowLabel(text=score,localize=False,color=INK,font_size=sp(15),bold=True))
        self.photo=Image(source=data['photo'],size_hint=(None,None),width=dp(240),height=dp(160),pos_hint={'center_x':.5},fit_mode='contain')
        self.story.add_widget(self.photo)
        self.story.bind(width=self._photo_size)
        self.story.add_widget(FlowLabel(text='Match illustration',color=MUTED,font_size=sp(11),halign='center'))
        self.rule()
        for paragraph in data['paragraphs']:
            font=loc.font(paragraph)
            if 'NotoSansCJK' not in str(font):font='assets/fonts/LiberationSerif-Regular.ttf'
            self.story.add_widget(FlowLabel(text=paragraph,localize=False,color=INK,font_size=sp(18),font_name=font,line_height=1.2))
        self.rule()
        self.story.add_widget(FlowLabel(text='MATCH REPORT',color=MUTED,font_size=sp(11),halign='right'))

    def _photo_size(self,*_):
        self.photo.width=min(dp(240),max(dp(80),self.story.width-dp(16)))
        self.photo.height=self.photo.width*2/3

    def rule(self):
        line=Widget(size_hint_y=None,height=dp(1))
        with line.canvas:
            Color(*MUTED);rect=Rectangle(pos=line.pos,size=line.size)
        line.bind(pos=lambda w,v:setattr(rect,'pos',v),size=lambda w,v:setattr(rect,'size',v))
        self.story.add_widget(line)

    def _paper(self,*_):self.paper.pos,self.paper.size=self.pos,self.size
