"""Club information: factual values and separately observed career honours."""
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp,sp
from menu_ui import Card,BoundedLabel,FlowLabel,ClubButton,GREEN
from club_profiles import profile,career_titles,stadium_capacity,stadium_variant
from kivy.uix.image import Image
from retro_props import cache

class ClubScreen(BoxLayout):
    def __init__(self,menu):
        super().__init__(orientation='vertical',spacing=dp(8));c=menu.game.career;loc=menu.game.i18n
        self.club=c.club;self.facts=profile(self.club)
        self.title=ClubButton(menu);self.title.height=dp(52);self.add_widget(self.title)
        self.scroll=ScrollView(do_scroll_x=False);self.card=Card();self.scroll.add_widget(self.card);self.add_widget(self.scroll)
        self.stadium_variant=stadium_variant(stadium_capacity(self.club))
        palette=c.kit_for_club(self.club) if self.club else ((.2,.4,.7,1),(.9,.9,.85,1))
        self.overview=BoxLayout(size_hint_y=None,height=dp(180),spacing=dp(12))
        self.facts_box=BoxLayout(orientation='vertical',spacing=dp(6),size_hint=(.52,None),pos_hint={'center_y':.5})
        self.facts_box.bind(minimum_height=self.facts_box.setter('height'))
        self.overview.add_widget(self.facts_box)
        self.stadium_picture=Image(texture=cache(menu.game).get('stadium_'+self.stadium_variant+'.png',palette),fit_mode='contain',size_hint_x=.48)
        self.overview.add_widget(self.stadium_picture);self.card.add_widget(self.overview)
        def fit_overview(*_):self.overview.height=max(self.facts_box.minimum_height,min(dp(210),max(dp(120),self.card.width*.25)))
        self.card.bind(width=fit_overview);self.facts_box.bind(minimum_height=fit_overview)
        unavailable=loc.tr('Not available')
        for label,value in (('FOUNDED',str(self.facts['founded']) if self.facts['founded'] else unavailable),('STADIUM',self.facts['stadium'] or unavailable),('CAPACITY',f"{self.facts['capacity']:,}" if self.facts['capacity'] else unavailable)):
            row=BoxLayout(size_hint_y=None,height=dp(36),spacing=dp(10));row.add_widget(BoundedLabel(text=label,font_size=sp(12),color=GREEN,size_hint_x=.28));value_label=FlowLabel(text=value,localize=False,font_size=sp(14),pos_hint={'center_y':.5});row.add_widget(value_label);value_label.bind(height=lambda widget,height,target=row:setattr(target,'height',max(dp(36),height)));self.facts_box.add_widget(row)
        self.card.label('HISTORICAL TITLES',heading=True)
        for award in self.facts['honours']:self.card.label(str(award['count'])+' · '+award['title'],localize=False)
        if not self.facts['honours']:self.card.label('Not available')
        self.card.label('CAREER TITLES',heading=True)
        awards=career_titles(c,self.club.uid)
        for award in awards:self.card.label(str(award['season'])+' · '+loc.competition(c,award['title'],award['country']),localize=False)
        if not awards:self.card.label('None recorded')
