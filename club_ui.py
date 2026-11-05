"""Club information: factual values and separately observed career honours."""
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp,sp
from menu_ui import Card,BoundedLabel,FlowLabel,ClubButton,GREEN
from club_profiles import profile,career_titles

class ClubScreen(BoxLayout):
    def __init__(self,menu):
        super().__init__(orientation='vertical',spacing=dp(8));c=menu.game.career;loc=menu.game.i18n
        self.club=c.club;self.facts=profile(self.club)
        self.title=ClubButton(menu);self.title.height=dp(52);self.add_widget(self.title)
        self.scroll=ScrollView(do_scroll_x=False);self.card=Card();self.scroll.add_widget(self.card);self.add_widget(self.scroll)
        unavailable=loc.tr('Not available')
        for label,value in (('FOUNDED',str(self.facts['founded']) if self.facts['founded'] else unavailable),('STADIUM',self.facts['stadium'] or unavailable),('CAPACITY',f"{self.facts['capacity']:,}" if self.facts['capacity'] else unavailable)):
            row=BoxLayout(size_hint_y=None,height=dp(36),spacing=dp(10));row.add_widget(BoundedLabel(text=label,font_size=sp(12),color=GREEN,size_hint_x=.28));value_label=FlowLabel(text=value,localize=False,font_size=sp(14),pos_hint={'center_y':.5});row.add_widget(value_label);value_label.bind(height=lambda widget,height,target=row:setattr(target,'height',max(dp(36),height)));self.card.add_widget(row)
        self.card.label('HISTORICAL TITLES',heading=True)
        for award in self.facts['honours']:self.card.label(str(award['count'])+' · '+award['title'],localize=False)
        if not self.facts['honours']:self.card.label('Not available')
        self.card.label('CAREER TITLES',heading=True)
        awards=career_titles(c,self.club.uid)
        for award in awards:self.card.label(str(award['season'])+' · '+loc.competition(c,award['title'],award['country']),localize=False)
        if not awards:self.card.label('None recorded')
