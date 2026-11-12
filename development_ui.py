"""Compact player objectives, coach values and a training-only skill picker."""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.metrics import dp,sp
from menu_ui import MenuTile,Card,FlowLabel,GREEN,INK
from ui_localization import LocalizedPopup
from player_development import FOCI,NAMES,needed

class ObjectivesSummary(GridLayout):
    """Two compact columns; every milestone stays visible without scrolling."""
    def __init__(self,menu):
        from menu_ui import DashboardField
        super().__init__(cols=2,spacing=dp(10),size_hint_y=None,height=dp(170))
        c=menu.game.career;loc=menu.game.i18n;d=c._ensure_development()
        def section(title):
            box=BoxLayout(orientation='vertical',spacing=dp(2))
            box.add_widget(DashboardField(text=loc.tr(title),compact_text=loc.tr(title),localize=False,color=GREEN,font_size=sp(12),max_lines=2))
            self.add_widget(box);return box
        def item(box,text,value,maximum,complete):
            box.add_widget(DashboardField(text=text,compact_text=text,localize=False,color=GREEN if complete else INK,font_size=sp(11),max_lines=2))
            box.add_widget(ProgressBar(max=max(1,maximum),value=min(maximum,value),size_hint_y=None,height=dp(4)))
        season=section('SEASON GOALS')
        item(season,loc.tr('Club goals: {goals}/{target}',goals=d['season_goals'],target=d['goal_target']),d['season_goals'],d['goal_target'],'goals'in d['season_earned'])
        item(season,loc.tr('Best coach trust: {trust}/70',trust=d['peak_trust']),d['peak_trust'],70,'trust'in d['season_earned'])
        goals=c.current_league.scorer_goals.get(c.player_name,0)
        rank=1+sum(g>goals for name,g in c.current_league.scorer_goals.items() if name!=c.player_name)
        for text in (loc.tr('Top-three league finish'),loc.tr('League scorer rank: {rank}',rank=rank if goals else '—')):
            season.add_widget(DashboardField(text=text,compact_text=text,localize=False,font_size=sp(11),max_lines=2))
        career=section('CAREER MILESTONES')
        for target in (50,100):
            item(career,loc.tr('Tracked club goals: {goals}/{target}',goals=d['career_goals'],target=target),d['career_goals'],target,d['career_goals']>=target)
        item(career,loc.tr('Transfers: {count}/1',count=d['transfers']),d['transfers'],1,d['transfers']>=1)
        item(career,loc.tr('International appearances: {count}/1',count=c.international_caps),c.international_caps,1,c.international_caps>=1)

class DevelopmentScreen(BoxLayout):
    """The coach-trust view contains values only."""
    def __init__(self,menu):
        super().__init__(orientation='vertical')
        c=menu.game.career;loc=menu.game.i18n;d=c._ensure_development()
        card=Card();card.label('COACH TRUST',heading=True)
        card.label(loc.tr('Trust {trust}/100 · {role}',trust=d['trust'],role=loc.tr(c.team_role)))
        card.add_widget(ProgressBar(max=100,value=d['trust'],size_hint_y=None,height=dp(12)))
        entry,exit=c.playing_window()
        card.label(loc.tr('Expected playing time: {minutes} minutes',minutes=exit-entry))
        if d['last_minutes']:
            card.label(loc.tr('Last appearance: {minutes} min · Trust change: {change}',minutes=d['last_minutes'],change=('+' if d['last_change']>=0 else '')+str(d['last_change'])))
        self.scroll=ScrollView(do_scroll_x=False);self.scroll.add_widget(card);self.add_widget(self.scroll)

class TrainingFocusPopup(LocalizedPopup):
    """Focus selection and skill values remain inside the training context."""
    def __init__(self,menu):
        g=menu.game;c=g.career;loc=g.i18n
        body=BoxLayout(orientation='vertical',spacing=dp(6))
        scroll=ScrollView(do_scroll_x=False)
        grid=GridLayout(cols=2,spacing=dp(6),size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for focus in FOCI:
            skill=c.development['skills'][focus];level=skill['level']
            stats=loc.tr('MAXIMUM LEVEL') if level==10 else loc.tr('Level {level}/10 · XP {xp}/{needed}',level=level,xp=skill['xp'],needed=needed(level))
            button=MenuTile(loc.tr(NAMES[focus])+'\n'+stats,lambda f=focus:self.choose(menu,f),accent=focus==c.training_focus,localize=False)
            button.font_size=sp(12);button.height=dp(64);button.disabled=c.training_used_this_week
            grid.add_widget(button)
        scroll.add_widget(grid);body.add_widget(scroll)
        body.add_widget(MenuTile('BACK',lambda:self.dismiss()))
        super().__init__(title='TRAINING FOCUS',content=body,size_hint=(None,None),size=(min(g.width-dp(16),dp(600)),min(g.height-dp(16),dp(280))))
    def choose(self,menu,focus):
        menu.action('training_focus',focus);self.dismiss()
