"""Club identity, factual history and a capacity-selected retro stadium portrait."""
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.metrics import dp,sp
from menu_ui import Card,BoundedLabel,FlowLabel,ClubButton,GREEN
from club_profiles import profile,career_titles,stadium_capacity,stadium_variant
from stadium_portraits import portrait

class ClubScreen(BoxLayout):
    def __init__(self,menu):
        super().__init__(orientation='vertical',spacing=dp(8));c=menu.game.career;loc=menu.game.i18n
        self.club=c.club;self.facts=profile(self.club)
        self.title=ClubButton(menu);self.title.height=dp(52);self.add_widget(self.title)
        self.scroll=ScrollView(do_scroll_x=False);self.card=Card();self.scroll.add_widget(self.card);self.add_widget(self.scroll)
        self.stadium_variant=stadium_variant(stadium_capacity(self.club))
        palette=c.kit_for_club(self.club)if self.club else ((.2,.4,.7,1),(.9,.9,.85,1))
        self.overview=BoxLayout(size_hint_y=None,spacing=dp(12))
        self.facts_box=BoxLayout(orientation='vertical',spacing=dp(6),size_hint_y=None)
        self.overview.add_widget(self.facts_box)
        self.stadium_picture=Image(texture=portrait(menu.game,stadium_capacity(self.club),palette),fit_mode='contain')
        self.overview.add_widget(self.stadium_picture);self.card.add_widget(self.overview)
        unavailable=loc.tr('Not available');league=c.current_league
        values=(('CLUB NAME',c.display_club(self.club)if self.club else unavailable),('COUNTRY',loc.country(league.country)),('LEAGUE',loc.league(c,league)),('FOUNDED',str(self.facts['founded'])if self.facts['founded']else unavailable),('STADIUM',self.facts['stadium']or unavailable),('CAPACITY',f"{self.facts['capacity']:,}"if self.facts['capacity']else unavailable))
        self.fact_rows={};self.fact_values={}
        for label,value in values:
            row=BoxLayout(size_hint_y=None,height=dp(36),spacing=dp(10))
            row.add_widget(BoundedLabel(text=label,font_size=sp(12),color=GREEN,size_hint_x=.28))
            text=FlowLabel(text=value,localize=False,font_size=sp(14),pos_hint={'center_y':.5});row.add_widget(text)
            text.bind(height=lambda widget,height,target=row:setattr(target,'height',max(dp(36),height)))
            self.facts_box.add_widget(row);self.fact_rows[label]=row;self.fact_values[label]=text
        def fit(*_):
            horizontal=self.card.width>=dp(600)
            self.overview.orientation='horizontal'if horizontal else'vertical'
            self.facts_box.height=self.facts_box.minimum_height
            self.facts_box.size_hint_x=.55 if horizontal else 1
            self.stadium_picture.size_hint=(.45,1)if horizontal else(1,None)
            photo=min(dp(280),max(dp(140),self.card.width*.35))
            self.stadium_picture.height=photo
            self.overview.height=max(self.facts_box.height,photo)if horizontal else self.facts_box.height+photo+dp(12)
        self.card.bind(width=fit);self.facts_box.bind(minimum_height=fit);fit()
        self.card.label('HISTORICAL TITLES',heading=True)
        for award in self.facts['honours']:self.card.label(str(award['count'])+' · '+award['title'],localize=False)
        if not self.facts['honours']:self.card.label('Not available')
        self.card.label('CAREER TITLES',heading=True)
        awards=career_titles(c,self.club.uid)if self.club else[]
        for award in awards:self.card.label(str(award['season'])+' · '+loc.competition(c,award['title'],award['country']),localize=False)
        if not awards:self.card.label('None recorded')
