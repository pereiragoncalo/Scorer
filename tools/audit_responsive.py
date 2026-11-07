import sys,json,os,argparse
from pathlib import Path
parser=argparse.ArgumentParser(description="Audit native World layouts at representative phone resolutions, densities and font scales.")
parser.add_argument("--output",type=Path,required=True)
parser.add_argument("--source",type=Path,help="Read runtime and fixtures from this clean checkout")
parser.add_argument('--views',nargs='+',help='Audit only the named views')
args=parser.parse_args();output=args.output.resolve();output.parent.mkdir(parents=True,exist_ok=True)
root=args.source.resolve() if args.source else Path(__file__).resolve().parents[1];os.chdir(root)
sys.path[:0]=[str(root),str(root/'ui_tests')]
from unittest.mock import patch
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import Metrics,dp
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.text import Label as CoreLabel
from menu_ui import TouchButton
from test_menus import isolated_game
from newspaper import make_report,fresh_state
from coach import fresh_state as coach_fresh
profiles=[('800x480',800,480,1.5,1),('1280x720',1280,720,2,1),('1920x1080',1920,1080,3,1),('2400x1080',2400,1080,3,1),('2340x1080',2340,1080,2.75,1),('2532x1170',2532,1170,3,1),('2960x1440',2960,1440,4,1),('foldable',2208,1768,2.75,1),('owner',1280,591,1.4,1),('compact',960,540,2,1),('largefont',1920,1080,3,1.3)]
views=['club','development', 'splash','data_notice','start','profile','offers','hub','injured_hub','training','standings','scorers','calendar','agent','world','world_country','world_league','editor','competitions','competition','leaderboard','help','language','family','record_safety','privacy','newspaper','coach','title_coach','private_coach','lifestyle','shopping','possessions','trophy','match','shot','chance_notice']
if args.views:
 unknown=set(args.views)-set(views)
 if unknown:parser.error('Unknown views: '+', '.join(sorted(unknown)))
 views=args.views
rows=[]
def settle():
 for _ in range(8):Clock.tick();Clock.tick_draw()
def in_scroll(w):
 p=w.parent;seen=set()
 while p and id(p) not in seen:
  seen.add(id(p))
  if isinstance(p,ScrollView):return True
  p=p.parent
 return False
def visible(w):
 p=w;seen=set()
 while p and id(p) not in seen:
  seen.add(id(p))
  if p.opacity<=0:return False
  p=p.parent
 return True
old=Window.size;density=Metrics.density;scale=Metrics.fontscale
try:
 for name,width,height,ratio,fontscale in profiles:
  Window.size=(width,height);Metrics.density=ratio;Metrics.fontscale=fontscale
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   Clock.unschedule(g.update)
   c=g.career;c.accept_starting_offer(c.offers[0]);g._career_started=True;g.size=(width,height)
   c._ensure_competitions();g.competition_key=next(iter(c.world_competitions.tournaments));g.world_country=c.club.country;g.world_league_key=g.editor_key=c.league_key;g._profile_return='hub'
   h,a=c.next_fixture();events=[dict(minute=m,half=1 if m<=45 else 2,side=s) for m,s in ((32,'home'),(51,'away'),(67,'home'),(90,'home'))]
   c.press_state=make_report(fresh_state(),dict(date='2026-10-04',competition=c.current_league.name,country=c.club.country,status='3-1'),h,a,c.club.uid,(3,1),1,1,[],events)
   for lang in ('pt','de','ja'):
    g.i18n.choose(lang)
    for view in views:
     issues=[]
     try:
      c.post_match_stage='';c.coach_state=coach_fresh(c.club.uid)
      c.life.update(injury_name='Calf strain',injury_games=2 if view=='injured_hub' else 0)
      if view in ('title_coach','trophy'):
       import honours,title_events
       honours.award(c,dict(season=c.season,competition='cup:qa:'+lang+':'+view,title='National Cup',team_uid=c.club.uid,team=c.club.name,country=c.club.country))
       if view=='title_coach':title_events.to_coach(c)
      else:
       from title_events import fresh
       c.title_events=fresh()
      if view=='private_coach':c.life['private_meeting']='drought'
      else:c.life['private_meeting']=''
      if view=='coach':c.coach_state.update(games=3,drought=3,recent=[0,0,0])
      else:c.attend_coach_meeting()
      if view in ('match','shot','chance_notice'):
       c.last_training_week=c.week;g.start_career_match()
       if view=='shot':g.awaiting_chance=True;g._begin_pending_chance()
      if view=='development':g.development_tab='skills'
      if view=='chance_notice':
       g.awaiting_chance=True;g.match_halftime=g.match_finished=False;g.match_opportunities=('long_cross',);g.match_chance_index=0;g.match_penalty_chance_index=g.match_easy_chance_index=-1;g.match_moment='equaliser'
      g.view='match' if view=='chance_notice' else 'hub' if view=='injured_hub' else view;g.draw();settle()
      if view=='chance_notice':
       notice=g._match_notice
       if not notice.layout_fits:issues.append(['notice_fit'])
       if notice.body.height>notice.scroll.height+2:issues.append(['notice_hidden_text'])
       for label in notice.body.children:
        ly=label.to_window(*label.pos)[1];sy=notice.scroll.to_window(*notice.scroll.pos)[1]
        if ly<sy-2 or ly+label.height>sy+notice.scroll.height+2:issues.append(['notice_text_bounds',label.text[:30]])
      menu=g._menu
      if menu:
       for child in menu.children:
        if child.y<menu.y-2 or child.top>menu.top+2:issues.append(['frame',type(child).__name__,round(child.y,1),round(child.top,1)])
       for w in menu.walk():
        if not visible(w):continue
        if isinstance(w,TouchButton):
         if w.height<dp(48)-2:issues.append(['touch_height',w.text,round(w.height/ratio,1)])
         if w.width<dp(48)-2:issues.append(['touch_width',w.text,round(w.width/ratio,1)])
         if not in_scroll(w):
          x,y=w.to_window(w.x,w.y)
          if x< -2 or y< -2 or x+w.width>width+2 or y+w.height>height+2:issues.append(['button_bounds',w.text,round(x,1),round(y,1),round(w.width,1),round(w.height,1)])
        elif isinstance(w,Label) and w.text and not w.shorten:
         # Core measurement reveals text clipped inside fixed-size labels.
         m=CoreLabel(text=w.text,text_size=(max(1,int(w.width)),None),font_name=w.font_name,font_size=w.font_size,bold=w.bold,line_height=w.line_height);m.refresh()
         if m.texture.size[1]>w.height+3:issues.append(['text_height',w.text[:45],m.texture.size[1],round(w.height,1)])
       if view in ('coach','title_coach','private_coach','newspaper'):
        if not menu.body.layout_fits:issues.append(['story_fit'])
        if any(isinstance(w,ScrollView) for w in menu.body.walk()):issues.append(['scroll'])
        if view=='newspaper' and len(menu.body.pages)!=1:issues.append(['pages'])
      else:
       for x,y,w,h,action,value in g.ui_buttons:
        if x< -2 or y< -2 or x+w>width+2 or y+h>height+2:issues.append(['canvas_button',action,x,y,w,h])
     except Exception as e:issues.append(['exception',type(e).__name__,str(e)])
     rows.append(dict(profile=name,pixels=[width,height],density=ratio,fontscale=fontscale,language=lang,view=view,issues=issues))
  output.with_suffix('.progress.json').write_text(json.dumps(rows,ensure_ascii=False))
  print(name,'complete',sum(bool(r['issues']) for r in rows if r['profile']==name),'cases with findings',flush=True)
finally:Window.size=old;Metrics.density=density;Metrics.fontscale=scale
out=dict(cases=len(rows),profiles=profiles,rows=rows)
output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('TOTAL',len(rows),'FINDINGS',sum(bool(r['issues']) for r in rows),flush=True)
