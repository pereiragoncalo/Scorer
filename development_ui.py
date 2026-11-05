"""Player goals, focused practice and visible selection rules."""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.metrics import dp
from menu_ui import MenuTile,Card
from player_development import FOCI,NAMES,HINTS,needed

class DevelopmentScreen(BoxLayout):
    def __init__(self,menu):
        super().__init__(orientation='vertical',spacing=dp(8))
        self.menu=menu;self.g=menu.game;self.c=self.g.career;self.loc=self.g.i18n
        self.state=self.c._ensure_development()
        self.tab=getattr(self.g,'development_tab','objectives')
        tabs=self.tabs=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(6))
        for title,key in (('OBJECTIVES','objectives'),('SKILLS','skills'),('COACH TRUST','trust')):
            tabs.add_widget(MenuTile(title,lambda k=key:menu.action('development_tab',k),accent=self.tab==key))
        self.add_widget(tabs)
        self.scroll=ScrollView(do_scroll_x=False,scroll_y=getattr(self.g,'_development_scroll_y',1.))
        self.content=GridLayout(cols=1,spacing=dp(8),size_hint_y=None,padding=[0,0,dp(4),dp(8)])
        self.content.bind(minimum_height=self.content.setter('height'));self.scroll.add_widget(self.content);self.add_widget(self.scroll)
        getattr(self,self.tab)()
    def card(self,title):
        card=Card();card.spacing=dp(5);card.label(title,heading=True);self.content.add_widget(card);return card
    def text(self,card,text,**values):
        label=card.label(self.loc.tr(text,**values));label.halign='justify';return label
    def objective(self,card,text,value,maximum,complete=False):
        card.label(text,localize=False)
        card.add_widget(ProgressBar(max=max(1,maximum),value=min(maximum,value),size_hint_y=None,height=dp(10)))
        card.label('COMPLETED' if complete else 'IN PROGRESS',muted=True)
    def objectives(self):
        d=self.state;card=self.card('SEASON GOALS')
        self.objective(card,self.loc.tr('Club goals: {goals}/{target}',goals=d['season_goals'],target=d['goal_target']),d['season_goals'],d['goal_target'],'goals'in d['season_earned'])
        self.objective(card,self.loc.tr('Best coach trust: {trust}/70',trust=d['peak_trust']),d['peak_trust'],70,'trust'in d['season_earned'])
        card.label('Top-three league finish',heading=True)
        goals=self.c.current_league.scorer_goals.get(self.c.player_name,0)
        rank=1+sum(g>goals for name,g in self.c.current_league.scorer_goals.items() if name!=self.c.player_name)
        self.text(card,'League scorer rank: {rank}',rank=rank if goals else '—')
        card.label('COMPLETED' if 'top3'in d['season_earned'] else 'Confirmed at season end.',muted=True)
        card=self.card('CAREER MILESTONES')
        for target in (50,100):
            self.objective(card,self.loc.tr('Tracked club goals: {goals}/{target}',goals=d['career_goals'],target=target),d['career_goals'],target,d['career_goals']>=target)
        self.objective(card,self.loc.tr('Transfers: {count}/1',count=d['transfers']),d['transfers'],1,d['transfers']>=1)
        self.objective(card,self.loc.tr('International appearances: {count}/1',count=self.c.international_caps),self.c.international_caps,1,self.c.international_caps>=1)
        self.text(card,'Tracking began in {season}. Earlier seasons are not reconstructed.',season=d['tracked_since'])
        if d['archive']:
            card=self.card('PREVIOUS SEASONS')
            for row in reversed(d['archive'][-5:]):
                self.text(card,'{season}: {goals}/{target} goals · {count}/3 objectives',season=row['season'],goals=row['goals'],target=row['target'],count=len(row['earned']))
    def skills(self):
        card=self.card('TRAINING FOCUS')
        if self.c.message.startswith(('Unable ','Could not ')):self.text(card,self.c.message)
        self.text(card,'Three shots earn 12 XP, plus 4 XP per goal on focus. Each level needs 60 + 20 times the current level XP.')
        if self.c.training_used_this_week:self.text(card,'Finish the next match before changing focus.')
        grid=GridLayout(cols=2 if self.width>=dp(600) else 1,spacing=dp(8),size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'));self.content.add_widget(grid)
        self.bind(width=lambda _,w:setattr(grid,'cols',2 if w>=dp(600) else 1))
        for focus in FOCI:
            panel=Card();panel.spacing=dp(5);panel.label(NAMES[focus],heading=True)
            skill=self.state['skills'][focus];level=skill['level'];cost=needed(level)
            if level==10:panel.label('MAXIMUM LEVEL')
            else:self.text(panel,'Level {level}/10 · XP {xp}/{needed}',level=level,xp=skill['xp'],needed=cost)
            panel.add_widget(ProgressBar(max=cost,value=cost if level==10 else skill['xp'],size_hint_y=None,height=dp(10)))
            self.text(panel,HINTS[focus])
            selected=focus==self.c.training_focus
            button=MenuTile('SELECTED' if selected else 'SELECT',lambda f=focus:self.menu.action('training_focus',f),accent=selected)
            button.disabled=selected or self.c.training_used_this_week;panel.add_widget(button);grid.add_widget(panel)
    def trust(self):
        d=self.state;card=self.card('COACH TRUST')
        if not self.c.club:
            card.label('Choose a club before meeting your coach.');return
        self.text(card,'Trust {trust}/100 · {role}',trust=d['trust'],role=self.loc.tr(self.c.team_role))
        card.add_widget(ProgressBar(max=100,value=d['trust'],size_hint_y=None,height=dp(12)))
        entry,exit=self.c.playing_window()
        self.text(card,'Expected playing time: {minutes} minutes',minutes=exit-entry)
        self.text(card,'Substitute below 45; starter from 45; key player from 80.')
        self.text(card,'Substitutes enter after 60 minutes. Starters below 60 trust play 75 minutes, or the full match on key occasions. Higher trust brings 90 minutes.')
        self.text(card,'Role changes the chance frequency slightly. Training and morale minimums always apply.')
        card=self.card('HOW TRUST CHANGES')
        self.text(card,'Training +2. Goals +6 each, up to +12. A key-game goal adds +2. No goal: -3, or -4 after three misses. No chances: -1.')
        self.text(card,'Training and goals rebuild trust. A new club starts at 50. International games do not change club trust.')
        if d['last_minutes']:
            self.text(card,'Last appearance: {minutes} min · Trust change: {change}',minutes=d['last_minutes'],change=('+' if d['last_change']>=0 else '')+str(d['last_change']))
