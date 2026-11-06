"""Paged standings for every current-season competition involving the player."""
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from menu_ui import MenuTile,CompactTable,BoundedLabel,EdgePanel
from competition_views import involved_competitions

class StandingsScreen(BoxLayout):
    def __init__(self,menu):
        super().__init__(orientation='vertical',spacing=dp(4))
        self.menu=menu;self.game=menu.game;self.c=self.game.career
        self.entries=involved_competitions(self.c)
        key=getattr(self.game,'standings_key','')
        if key not in dict(self.entries):key=self.entries[0][0]
        self.game.standings_key=key
        self.key=key;self.competition=dict(self.entries)[key]
        cup=self.competition
        if key.startswith('league:'):
            league=cup
            rows=[(menu._standing_position(league,i+1),self.c.display_club(club),club.played,club.won,club.drawn,club.lost,club.goals_for,club.goals_against,club.goal_difference,club.points) for i,club in enumerate(league.table())]
            self.table=CompactTable(self.title(key,cup),('POS','CLUB','P','W','D','L','GF','GA','GD','PTS'),rows,focus=self.c.display_club(self.c.club) if self.c.club and self.c.club in league.clubs else None,summary=(0,1,2,8,9),detail=(0,1,3,4,5,6,7),title_localize=False,zones=menu._table_zones(league))
        else:
            group=getattr(self.game,'standings_group',0)%max(1,len(cup.groups))
            self.game.standings_group=group
            group_stage=cup.groups and cup.stage in ('League phase','Awaiting Libertadores')
            tab=getattr(self.game,'standings_tab','auto')
            show_table=bool(cup.groups) and (tab=='table' or tab=='auto' and group_stage)
            if cup.groups:
                options=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(4))
                options.add_widget(MenuTile(self.game.i18n.tr('Group {number}',number=group+1),lambda:self.group(1),localize=False))
                options.add_widget(MenuTile('FIXTURES' if show_table else 'STANDINGS',lambda:self.tab('fixtures' if show_table else 'table')))
                self.add_widget(options)
            if show_table:
                rows=[]
                for i,r in enumerate(cup.table(group)):
                    rows.append((i+1,menu._competition_team_name(cup.teams[r['uid']]),r['p'],r['w'],r['d'],r['l'],r['gf'],r['ga'],r['gf']-r['ga'],r['pts']))
                self.table=CompactTable(self.title(key,cup),('POS','CLUB','P','W','D','L','GF','GA','GD','PTS'),rows,summary=(0,1,2,8,9),detail=(0,1,3,4,5,6,7),title_localize=False)
            else:
                from international_calendar import match_date
                rows=[]
                for _,f in sorted(enumerate(cup.fixtures),key=lambda item:(item[1]['week'],item[1].get('date',''),item[0])):
                    score='–' if f['score'] is None else '{}–{}'.format(*f['score'])
                    if f.get('penalties'):score+=' ({}–{})'.format(*f['penalties'])
                    d=match_date(self.c.season,cup,f)
                    stage=f['stage'] if f['group'] is None else self.game.i18n.tr('Group {number}',number=f['group']+1)
                    rows.append((d.strftime('%d/%m'),menu._competition_team_name(cup.teams[f['home']])+' vs '+menu._competition_team_name(cup.teams[f['away']]),self.game.i18n.tr(stage),score))
                self.table=CompactTable(self.title(key,cup),('DATE','MATCH','COMPETITION','STATUS'),rows,summary=(0,1,2,3),title_localize=False)
        self.add_widget(self.table)

    def title(self,key,cup):
        return self.game.i18n.league(self.c,cup) if key.startswith('league:') else self.game.i18n.tr(cup.title)
    def select(self,key):
        cup=dict(self.entries)[key];group=0
        if not key.startswith('league:'):
            actor='nation:'+self.c.nationality if cup.national else self.c.club.uid if self.c.club else ''
            group=next((i for i,ids in enumerate(cup.groups) if actor in ids),0)
        self.game.standings_key=key;self.game.standings_group=group;self.game.standings_tab='auto';self.menu._signature=None;self.game.draw()
    def move(self,step):
        keys=[k for k,_ in self.entries];self.select(keys[(keys.index(self.key)+step)%len(keys)])
    def group(self,step):
        self.game.standings_group=(self.game.standings_group+step)%len(self.competition.groups);self.game.standings_tab='table';self.menu._signature=None;self.game.draw()
    def tab(self,tab):
        self.game.standings_tab=tab;self.menu._signature=None;self.game.draw()
    def choose(self):
        popup=ModalView(size_hint=(.94,.92),auto_dismiss=False)
        panel=EdgePanel(orientation='vertical');scroll=ScrollView(do_scroll_x=False);list_=GridLayout(cols=1,size_hint_y=None,spacing=dp(4));list_.bind(minimum_height=list_.setter('height'))
        for key,cup in self.entries:
            def select(key=key):popup.dismiss();self.select(key)
            list_.add_widget(MenuTile(self.title(key,cup),select,localize=False))
        scroll.add_widget(list_);panel.add_widget(scroll);panel.add_widget(MenuTile('CLOSE',popup.dismiss));popup.add_widget(panel)
        self.game._standings_picker=popup;popup.bind(on_dismiss=lambda *_:setattr(self.game,'_standings_picker',None));popup.open()
