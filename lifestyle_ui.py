"""A one-screen local contract and illustrated catalogue. No billing or real money."""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.metrics import dp,sp
from menu_ui import MenuTile,BoundedLabel,DashboardField,LocalizedPopup,GREEN
from career_life import ITEMS,age,purchase,retirement
class LifestyleScreen(BoxLayout):
 def __init__(self,menu):
  super().__init__(orientation='vertical',spacing=dp(10));self.menu=menu
  c=menu.game.career;tr=menu.game.i18n.tr
  header=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(6));self.add_widget(header)
  header.add_widget(BoundedLabel(text='LIFESTYLE',halign='center',font_size=sp(20),color=GREEN))
  help=MenuTile('HELP',lambda:menu.action('help'));help.size_hint_x=None;help.width=dp(80);header.add_widget(help)
  text=tr('Age {age} · Salary €{salary}/week',age=age(c),salary=f"{c.life['salary']:,}".replace(',',' '))+'\n'+tr('Balance €{balance}',balance=f"{c.life['balance']:,}".replace(',',' '))
  summary=DashboardField(compact_text=text.replace('\n',' · '),text=text,localize=False,halign='center',font_size=sp(16));self.add_widget(summary)
  buttons=BoxLayout(spacing=dp(12),size_hint_y=None,height=dp(64));self.add_widget(buttons)
  buttons.add_widget(MenuTile('SHOPPING',lambda:menu.action('shopping'),accent=True));buttons.add_widget(MenuTile('MY ASSETS',lambda:menu.action('possessions')))
  self.add_widget(BoundedLabel(text='',size_hint_y=.3))
  self.add_widget(MenuTile('BACK',lambda:menu.action('hub')))
class EstateScreen(BoxLayout):
 def __init__(self,menu):
  super().__init__(orientation='vertical',spacing=dp(6));self.menu=menu;c=menu.game.career;tr=menu.game.i18n.tr
  header=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(6));self.add_widget(header)
  header.add_widget(DashboardField(compact_text=tr('MY ASSETS')+' · '+c.player_name,text=tr('MY ASSETS')+' · '+c.player_name,localize=False,halign='center',font_size=sp(18),color=GREEN))
  help=MenuTile('HELP',lambda:menu.action('help'));help.size_hint_x=None;help.width=dp(72);header.add_widget(help)
  from estate_portrait import EstatePortrait
  self.portrait=EstatePortrait(c);self.add_widget(self.portrait)
  names=BoxLayout(size_hint_y=None,height=dp(32),spacing=dp(6));self.add_widget(names)
  for kind in ('home','clothes','car'):
   row=self.portrait.selection[kind];text=tr(row[2]) if row else '—'
   names.add_widget(DashboardField(compact_text=text,text=text,localize=False,halign='center',font_size=sp(12)))
  actions=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(6));self.add_widget(actions)
  actions.add_widget(MenuTile('COLLECTION',lambda:menu.action('collection')));actions.add_widget(MenuTile('BACK',lambda:menu.action('lifestyle')))
class CatalogueScreen(BoxLayout):
 def __init__(self,menu,owned=False):
  super().__init__(orientation='vertical',spacing=dp(6));self.menu=menu;self.owned=owned;c=menu.game.career;d=c.life;tr=menu.game.i18n.tr
  header=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(5));self.add_widget(header)
  summary=tr('COLLECTION' if owned else 'SHOPPING')+' · '+tr('Balance €{balance}',balance=f"{d['balance']:,}".replace(',',' '))
  header.add_widget(BoundedLabel(text=summary,localize=False,halign='center',color=GREEN,font_size=sp(13)))
  help=MenuTile('HELP',lambda:menu.action('help'));help.size_hint_x=None;help.width=dp(72);header.add_widget(help)
  category=getattr(menu.game,'_shop_category',0)%4;kind=('home','car','gift','clothes')[category]
  rows=[i for i in ITEMS if i[1]==kind and (not owned or i[0] in d['owned'])]
  index=getattr(menu.game,'_shop_pos',0)%max(1,len(rows));menu.game._shop_pos=index
  panel=BoxLayout(spacing=dp(10));self.add_widget(panel)
  if rows:
   key,_,name,price=rows[index];image=Image(source='assets/lifestyle/'+key+'.png',fit_mode='contain');image.texture.mag_filter=image.texture.min_filter='nearest';panel.add_widget(image)
   info=BoxLayout(orientation='vertical');panel.add_widget(info)
   info.add_widget(BoundedLabel(text=name,font_size=sp(21),halign='center'))
   info.add_widget(BoundedLabel(text='€ '+f'{price:,}'.replace(',',' '),localize=False,font_size=sp(22),halign='center',color=GREEN))
   count=d['owned'].get(key,0)
   info.add_widget(BoundedLabel(text=tr('Owned: {count}',count=count) if count else '',localize=False,halign='center'))
  else:panel.add_widget(BoundedLabel(text='No purchases yet.',font_size=sp(20),halign='center'))
  tabs=GridLayout(cols=4,size_hint_y=None,height=dp(52),spacing=dp(4));self.add_widget(tabs)
  for i,title in enumerate(('HOMES','CARS','GIFTS','CLOTHES')):tabs.add_widget(MenuTile(title,lambda n=i:self.category(n),accent=category==i))
  actions=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(5));self.add_widget(actions)
  for title,delta in (('PREVIOUS',-1),('NEXT',1)):
   button=MenuTile(title,lambda n=delta:self.move(n));button.disabled=len(rows)<2;actions.add_widget(button)
  if not owned:
   buy=MenuTile('BUY',lambda:self.buy(key),accent=True);buy.disabled=not rows or d['balance']<price or bool(count and kind!='gift');actions.add_widget(buy)
  actions.add_widget(MenuTile('BACK',lambda:menu.action('possessions' if owned else 'lifestyle')))
 def category(self,n):self.menu.game._shop_category=n;self.menu.game._shop_pos=0;self.refresh()
 def move(self,n):self.menu.game._shop_pos+=n;self.refresh()
 def refresh(self):self.menu._signature=None;self.menu.game.draw()
 def buy(self,key):purchase(self.menu.game.career,key);self.refresh()
class FavouritePicker(LocalizedPopup):
 def __init__(self,screen):
  self.screen=screen;self.page=0;c=screen.game.career
  self.teams=sorted((c.display_club(t),t.country,t.uid) for l in c.domestic_leagues() for t in l.clubs)
  body=BoxLayout(orientation='vertical',spacing=dp(5));self.search=TextInput(multiline=False,hint_text='Search club',size_hint_y=None,height=dp(48));body.add_widget(self.search)
  self.grid=GridLayout(cols=2,spacing=dp(4));body.add_widget(self.grid);nav=BoxLayout(size_hint_y=None,height=dp(48));body.add_widget(nav)
  nav.add_widget(MenuTile('PREVIOUS',lambda:self.move(-1)));nav.add_widget(MenuTile('NEXT',lambda:self.move(1)));nav.add_widget(MenuTile('CANCEL',self.dismiss));self.search.bind(text=lambda *_:self.render(True))
  super().__init__(title='FAVOURITE CLUB',content=body,size_hint=(.96,.96));self.render()
 def move(self,n):self.page+=n;self.render()
 def render(self,reset=False):
  if reset:self.page=0
  rows=[x for x in self.teams if self.search.text.casefold() in (x[0]+' '+x[1]).casefold()];self.page=max(0,min(max(0,(len(rows)-1)//6),self.page));self.grid.clear_widgets()
  for name,country,uid in rows[self.page*6:self.page*6+6]:self.grid.add_widget(MenuTile(name+' · '+self.screen.game.i18n.country(country),lambda k=uid,n=name:self.pick(k,n),localize=False))
 def pick(self,uid,name):self.screen.draft['favourite']=uid;self.screen.favourite.text=name;self.dismiss()
def retirement_prompt(g):
 if getattr(g,'_retirement_popup',None):return
 body=BoxLayout(orientation='vertical',spacing=dp(8));body.add_widget(BoundedLabel(text='Would you like to retire or play another season?',halign='center'))
 popup=LocalizedPopup(title='RETIREMENT',content=body,size_hint=(.85,.7),auto_dismiss=False);g._retirement_popup=popup
 popup.bind(on_dismiss=lambda *_:setattr(g,'_retirement_popup',None))
 def choose(retire):
  if retirement(g.career,retire):popup.dismiss();g._retirement_popup=None;g.view='profile' if retire else 'hub';g.draw()
 row=BoxLayout(size_hint_y=None,height=dp(52));body.add_widget(row);row.add_widget(MenuTile('PLAY ANOTHER SEASON',lambda:choose(False),accent=True));row.add_widget(MenuTile('RETIRE',lambda:choose(True)));popup.open()
