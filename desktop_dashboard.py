"""Dense Windows Free hub: upcoming league fixtures and league scorers."""
from math import ceil
from kivy.clock import Clock
from kivy.graphics import Color,RoundedRectangle
from kivy.metrics import dp,sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from menu_ui import MainDashboard,BoundedLabel,MenuTile,GREEN,MUTED,INK
from dashboard_data import dashboard_data


class DashboardRow(BoxLayout):
    def __init__(self,row,kind,number,**kwargs):
        super().__init__(spacing=dp(8),padding=[dp(8),0],size_hint_y=None,**kwargs)
        self.focused=row.focus
        with self.canvas.before:
            Color(*((0.09,0.32,0.25,0.95) if row.focus else (0.05,0.13,0.16,0.70) if number%2==0 else (0.03,0.09,0.12,0.55)))
            self.background=RoundedRectangle(radius=[dp(5)])
        self.bind(pos=self._rect,size=self._rect)
        if kind=='fixtures':
            for text,hint,align in ((row.home,.46,'right'),('vs',.08,'center'),(row.away,.46,'left')):
                self.add_widget(BoundedLabel(text=text,localize=False,font_size=sp(15),bold=row.focus,
                                             max_lines=1,color=GREEN if row.focus else INK,halign=align,size_hint_x=hint))
        else:
            self.add_widget(BoundedLabel(text=str(row.rank),localize=False,color=GREEN if row.focus else MUTED,
                                         size_hint_x=None,width=dp(24),font_size=sp(13),max_lines=1))
            player=BoxLayout(orientation='vertical')
            player.add_widget(BoundedLabel(text=row.player,localize=False,font_size=sp(14),bold=row.focus,max_lines=1,
                                            color=GREEN if row.focus else INK))
            if row.club:player.add_widget(BoundedLabel(text=row.club,localize=False,font_size=sp(11),color=MUTED,max_lines=1,size_hint_y=.7))
            self.add_widget(player)
            self.add_widget(BoundedLabel(text=str(row.goals),localize=False,font_size=sp(18),bold=True,halign='right',
                                         size_hint_x=None,width=dp(44),max_lines=1,color=GREEN if row.focus else INK))
    def _rect(self,*_):self.background.pos,self.background.size=self.pos,self.size


class DashboardRows(BoxLayout):
    """Fit rows to available space; bounded paging instead of main-menu scrolling."""
    def __init__(self,data,kind):
        super().__init__(orientation='vertical',spacing=dp(4))
        self.data,self.kind=tuple(data),kind
        self.page=0;self.capacity=1;self.page_count=1;self.visible_rows=[];self.user_paged=False
        self.rows=BoxLayout(orientation='vertical',spacing=dp(2 if kind=='fixtures' else 3));self.add_widget(self.rows)
        self.pager=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(6))
        self.previous=MenuTile('PREV',lambda:self.move(-1));self.following=MenuTile('NEXT',lambda:self.move(1))
        for button in (self.previous,self.following):button.size_hint_x=None;button.width=dp(70);button.height=dp(48)
        self.page_label=BoundedLabel(text='',halign='center',font_size=sp(12),max_lines=1)
        for widget in (self.previous,self.page_label,self.following):self.pager.add_widget(widget)
        self._trigger=Clock.create_trigger(self._render,0)
        self.bind(size=lambda *_:self._trigger());self._trigger()

    def move(self,delta):
        self.user_paged=True;self.page=max(0,min(self.page_count-1,self.page+delta));self._trigger()

    def _render(self,*_):
        minimum=dp(24 if self.kind=='fixtures' else 38);gap=dp(2 if self.kind=='fixtures' else 3)
        capacity=max(1,int((self.height+gap)/(minimum+gap)))
        needs_pager=self.kind=='fixtures' and len(self.data)>capacity
        available=max(1,self.height-(dp(52) if needs_pager else 0))
        if needs_pager:capacity=max(1,int((available+gap)/(minimum+gap)))
        self.capacity=capacity;self.page_count=max(1,ceil(len(self.data)/capacity)) if self.kind=='fixtures' else 1
        if not self.user_paged and self.kind=='fixtures':
            focus=next((index for index,row in enumerate(self.data) if row.focus),0)
            self.page=focus//capacity
        self.page=min(self.page,self.page_count-1)
        if needs_pager and self.pager.parent is None:self.add_widget(self.pager)
        elif not needs_pager and self.pager.parent is self:self.remove_widget(self.pager)
        self.previous.disabled=self.page==0;self.following.disabled=self.page>=self.page_count-1
        self.page_label.text=f'{self.page+1} / {self.page_count}'
        self.rows.clear_widgets();self.visible_rows=[]
        chunk=self.data[self.page*capacity:(self.page+1)*capacity]
        row_height=max(1,min(dp(48 if self.kind=='fixtures' else 46),(available-len(chunk)*gap)/max(1,len(chunk))))
        if not chunk:
            self.rows.add_widget(BoundedLabel(text='League season complete' if self.kind=='fixtures' else 'No league goals yet',
                                              font_size=sp(14),color=MUTED,size_hint_y=None,height=dp(36)))
        for index,row in enumerate(chunk):
            widget=DashboardRow(row,self.kind,self.page*capacity+index,height=row_height)
            self.visible_rows.append(widget);self.rows.add_widget(widget)
        self.rows.add_widget(Widget())


class WindowsDashboard(MainDashboard):
    def __init__(self,menu):
        super().__init__(menu)
        c=menu.game.career;self.data=dashboard_data(c)
        self.match.clear_widgets();self.season.clear_widgets()
        self.match.add_widget(BoundedLabel(text=f'LEAGUE MATCHDAY {self.data.round_number}' if self.data.fixtures else 'LEAGUE SEASON COMPLETE',
                                           color=GREEN,bold=True,font_size=sp(17),size_hint_y=None,height=dp(28)))
        if self.data.next_match:
            kind,home,away=self.data.next_match
            competition=c.cup_name if kind=='cup' else 'League'
            upcoming=f'NEXT · {menu.game.i18n.date(c.current_date)} · {competition} · {home} vs {away}'
        else:upcoming='No upcoming match'
        self.match.add_widget(BoundedLabel(text=upcoming,localize=False,color=MUTED,font_size=sp(12),size_hint_y=None,height=dp(32)))
        columns=BoxLayout(size_hint_y=None,height=dp(20),padding=[dp(8),0],spacing=dp(8))
        for title,hint,align in (('HOME',.46,'right'),('',.08,'center'),('AWAY',.46,'left')):
            columns.add_widget(BoundedLabel(text=title,color=MUTED,font_size=sp(10),size_hint_x=hint,halign=align))
        self.match.add_widget(columns)
        self.fixtures=DashboardRows(self.data.fixtures,'fixtures');self.match.add_widget(self.fixtures)
        self.match.add_widget(self.footer)
        self.season.add_widget(BoundedLabel(text='TOP SCORERS',color=GREEN,bold=True,font_size=sp(17),size_hint_y=None,height=dp(28)))
        scoring_columns=BoxLayout(size_hint_y=None,height=dp(20),spacing=dp(8),padding=[dp(8),0])
        scoring_columns.add_widget(BoundedLabel(text='#',color=MUTED,font_size=sp(10),size_hint_x=None,width=dp(24)))
        scoring_columns.add_widget(BoundedLabel(text='PLAYER / CLUB',color=MUTED,font_size=sp(10)))
        scoring_columns.add_widget(BoundedLabel(text='GOALS',color=MUTED,font_size=sp(10),halign='right',size_hint_x=None,width=dp(44)))
        self.season.add_widget(scoring_columns)
        self.scorers=DashboardRows(self.data.scorers,'scorers');self.season.add_widget(self.scorers)
        self.season.add_widget(BoundedLabel(text=f'YOU · #{self.data.hero_rank} · {self.data.hero_league_goals} league {'goal' if self.data.hero_league_goals==1 else 'goals'}',
                                            color=GREEN,font_size=sp(12),size_hint_y=None,height=dp(26),max_lines=1))
        self.season.add_widget(BoundedLabel(text=f'YOUR SEASON · {c.matches} {'match' if c.matches==1 else 'matches'} · {c.goals} {'goal' if c.goals==1 else 'goals'}',
                                            color=MUTED,font_size=sp(12),size_hint_y=None,height=dp(26),max_lines=1))
        self.season.add_widget(BoundedLabel(text=menu.game.i18n.league(c,c.current_league),localize=False,
                                            color=MUTED,font_size=sp(11),size_hint_y=None,height=dp(22),max_lines=1))
