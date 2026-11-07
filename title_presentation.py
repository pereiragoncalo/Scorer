"""A title-winning squad carries its trophy to its own supporters."""
from kivy.graphics import Color,Rectangle
from kivy.metrics import dp
from title_events import pending
from retro_props import cache
from retro_sprites import Pose,PLAYER_HEIGHT_METRES,kit_palette,projected_scale

def prepare(g):
    event=pending(g.career)
    if not event:return
    if getattr(g,'_title_scene_id',None)==event['id']:return
    g._title_scene_id=event['id'];g._title_started=g.elapsed
    g.match_home=g.career._competition_club(event['scene']['home']);g.match_away=g.career._competition_club(event['scene']['away']) if event['scene']['away']['uid']!=event['scene']['home']['uid'] else None
    g.match_is_international=event['team_uid'].startswith('nation:');g.shot_context='match'
    g.match_opportunity_seed=('title',event['id'])
    token=(g.match_home.uid,getattr(g.match_away,'uid',''),repr(g.match_opportunity_seed))
    g._attendance_snapshot=(token,dict(event['scene']['turnout']))
    g._celebrating_side='home' if g.match_home.uid==event['team_uid'] else 'away'
    g._crowd_celebration_started=g.elapsed;g._crowd_celebrate_until=g.elapsed+3600.

def position(age,index,home,extended):
    target=(-9.,-1.9) if home else (32.5 if extended else 33.,-1.9)
    # Captain at front; teammates gather behind, then all celebrate with fans.
    dx=((index+1)//2)*(.55 if index%2 else -.55) if index else 0.
    end=(target[0]+dx,target[1]+.35*(index//3))
    start=(index*.8-4,13.+(index%3)*.7);delay=index*.12;t=max(0.,min(1.,(age-delay)/4.8))
    return tuple(a+(b-a)*t for a,b in zip(start,end)),('RUN' if t<1 else 'CELEBRATE'),max(0.,age-delay)

def draw(g):
    prepare(g);event=pending(g.career)
    if not event:return
    from stadium_scene import context
    ctx=context(g);age=max(0,g.elapsed-g._title_started);home=g._celebrating_side=='home'
    winner=g.match_home if home else g.match_away;colours=kit_palette(g.career.kit_for_club(winner));renderer=g._retro_renderer()
    actors=[]
    for i in range(11):
        (x,y),state,clock=position(age,i,home,ctx['away_sector'].extended)
        actors.append((y,i,x,state,clock))
    captain=None
    for y,i,x,state,clock in sorted(actors):
        # Keep the walk articulated, then lift the trophy with the raised-hands pose.
        pose=Pose('CARRY' if i==0 and state=='RUN' else state,age=clock,view='back',flipped=not home)
        renderer.draw(g,'title_'+str(i),'players',pose,(x,y,0),PLAYER_HEIGHT_METRES,colours)
        if i==0:
            character,clip,frame=renderer.sample('title_0','players',pose)
            joints=clip['joints'][pose.view][frame];a,b=joints['wrist_0'],joints['wrist_1'];mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
            ax,ay=character['anchor'];scale=projected_scale(g,(x,y,0),character);px,py=g.project(x,y,0)
            if pose.flipped:mx=character['canvas'][0]-mx;ax=character['canvas'][0]-ax
            captain=(px+(mx-ax)*scale,py+(ay-my)*scale,scale*.65)
    px,py,scale=captain
    t=cache(g).get('trophy.png');Color(1,1,1,1);Rectangle(texture=t,pos=(px-12*scale,py-5*scale),size=(24*scale,28*scale))
    g._draw_text('CHAMPIONS',g.center_x,g.top-dp(35),dp(23),(1,.83,.23,1),'center',max_width=g.width-dp(24))
    g._draw_text(event['title']+' · '+g.career.display_club(winner),g.center_x,g.top-dp(65),dp(13),(1,1,1,1),'center',max_width=g.width-dp(24))
    if getattr(g,'_title_button',None) is None:
        from menu_ui import MenuTile
        g._title_button=MenuTile('CONTINUE',lambda:g._activate_ui('title_continue'),accent=True)
        g._title_button.size_hint=(None,None);g.add_widget(g._title_button)
    g._title_button.size=(dp(160),dp(52));g._title_button.pos=(g.right-dp(176),g.y+dp(12))

    if g._title_button.canvas not in g.canvas.children:g.canvas.add(g._title_button.canvas)
