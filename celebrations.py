"""Goal presentation only: no scoring, physics, career RNG or future outcomes."""
from dataclasses import dataclass
import math

def crowd_jump(age,seed):
    """Each seat gets its own frequency, height, phase and reaction delay."""
    return jump_displacement(age,crowd_profile(seed))

def crowd_profile(seed):
    seed=int(seed)&0xffffffff
    return (6.+8.*(seed&1023)/1023,math.tau*((seed>>10)&1023)/1023,
            2.+5.*((seed>>20)&127)/127,.45*((seed>>27)&31)/31)

def jump_displacement(age,profile):
    frequency,phase,height,delay=profile
    t=age-delay
    if t<=0:return 0.
    return height*min(1.,t/.18)*max(0.,math.sin(t*frequency+phase))

def decisive_now(game):
    """Observed late go-ahead goal; never predict the eventual winner."""
    stakes=getattr(game,'match_stakes',{})
    if not stakes.get('late_allowed',True):return False
    home=game._player_match_is_home()
    own,other=(game.match_home_score,game.match_away_score) if home else (game.match_away_score,game.match_home_score)
    minute=game.match_minute-(game.match_first_stoppage if game.match_half==2 else 0)
    threshold=70 if stakes.get('kind') in ('final','playoff') else 80
    return game.match_half==2 and minute>=threshold and own==other+1

def mix(a,b,t):return tuple(x+(y-x)*t for x,y in zip(a,b))
def smooth(t):return t*t*(3-2*t)

@dataclass(frozen=True)
class GoalCelebration:
    started:float
    side:str
    decisive:bool
    origin:tuple
    target:tuple
    fans:tuple
    run_seconds:float
    slide_start:tuple
    retrieving:bool=False
    pickup:tuple=(0.,-.25)

    @property
    def duration(self):return 6. if self.retrieving else self.run_seconds+(1.1 if self.decisive else 0.)+2.6

    def actor(self,age,index=0):
        age=max(0.,age)
        if self.retrieving:
            if age<2.:return mix(self.origin,self.pickup,min(1.,age/2.)),'RUN',age
            if age<2.6:return self.pickup,'TACKLE',age-2.
            return mix(self.pickup,(0.,52.5),min(1.,(age-2.6)/7.)),'BALL_RUN',age-2.6
        run=self.run_seconds
        slide=1.1 if self.decisive else 0.
        if index==0:
            if age<run:return mix(self.origin,self.slide_start if self.decisive else self.target,age/run),'RUN',age
            if self.decisive and age<run+slide:
                t=(age-run)/slide
                return mix(self.slide_start,self.target,1-(1-t)**2.5),'KNEE_SLIDE',t*.65
            settle=age-run-slide
            if self.decisive and settle<.35:return self.target,'FALL',.5+settle
            return self.target,('HUG' if settle>.65 else 'CELEBRATE'),max(0.,settle-.65) if settle>.65 else settle
        slots=((-0.45,.12),(.45,.12),(0.,-.42))
        dx,dy=slots[(index-1)%3]
        target=(self.target[0]+dx,self.target[1]+dy)
        start=(self.origin[0]+(index-2)*1.25,self.origin[1]+1.1+index*.25)
        delay=.18*index
        arrive=run+slide+.65+index*.07
        t=max(0.,min(1.,(age-delay)/(arrive-delay)))
        if age<=delay:return start,'IDLE',age
        if t<1:return mix(start,target,t),'RUN',max(0.,age-delay)
        return target,'HUG',age-arrive

def start(game):
    if game.shot_context!='match' or game.view!='shot':return
    if game.match_home is None or game.match_away is None:return
    from stadium_scene import context
    ctx=context(game);home=game._player_match_is_home()
    target=(-9.,-1.9) if home else (32.5 if ctx['away_sector'].extended else 33.,-1.9)
    fans=(-9.,-5.) if home else (37.,-5.5)
    from career import PLAYER_SCALE
    facing=0. if game.current_opportunity is not None and game.state in (game.STATE_BUILDUP,game.STATE_AIMING) else game.aim_x
    fx,fy=facing-game.shot_origin_x,-game.shot_origin_y
    length=max(.001,math.hypot(fx,fy));standoff=(.12 if game.shot_type=='header' else .52)*PLAYER_SCALE
    origin=(game.shot_origin_x-fx/length*standoff,game.shot_origin_y-fy/length*standoff)
    dx,dy=target[0]-origin[0],target[1]-origin[1];distance=max(.01,math.hypot(dx,dy))
    own,other=(game.match_home_score,game.match_away_score) if home else (game.match_away_score,game.match_home_score)
    retrieving=own<other
    decisive=not retrieving and (game.match_player_goals==3 or decisive_now(game))
    slide_start=(target[0]-dx/distance*2.6,target[1]-dy/distance*2.6) if decisive else target
    run_distance=math.dist(origin,slide_start)
    run=max(1.3,min(5.8,run_distance/7.0))
    celebration=GoalCelebration(game.elapsed,'home' if home else 'away',decisive,origin,target,fans,run,slide_start,retrieving,(game.ball.x,-.25))
    game.goal_celebration=celebration
    game._crowd_celebrate_until=game.elapsed+celebration.duration+.3

def active(game):
    c=getattr(game,'goal_celebration',None)
    return c is not None and game.view=='shot' and game.shot_context=='match' and game.elapsed<c.started+c.duration

def motion(celebration,age,index=0):
    position=celebration.actor(age,index)[0]
    before=celebration.actor(max(0.,age-.025),index)[0]
    after=celebration.actor(age+.025,index)[0]
    dx,dy=after[0]-before[0],after[1]-before[1]
    moving=math.hypot(dx,dy)>.0025
    return ((position[0]+dx,position[1]+dy) if moving else celebration.fans),moving

def draw(game):
    from retro_sprites import Pose,PLAYER_HEIGHT_METRES,kit_palette
    celebration=getattr(game,'goal_celebration',None)
    if celebration is None:return
    age=game.elapsed-celebration.started
    renderer=game._retro_renderer();colours=kit_palette(game._match_outfield_kits()[0])
    actors=[]
    for index in range(1 if celebration.retrieving else 4):
        (x,y),state,clock=celebration.actor(age,index)
        target,moving=motion(celebration,age,index)
        if state in ('RUN','BALL_RUN') and not moving:state='CARRY' if state=='BALL_RUN' else 'IDLE'
        origin=game.project(x,y,0);destination=game.project(*target,0)
        flip=destination[0]<origin[0]
        view=('back' if target[1]<y else 'front')
        actors.append((y,index,x,Pose(state,age=clock,view=view,flipped=flip)))
    for y,index,x,pose in sorted(actors):
        renderer.draw(game,'celebration_'+str(index),'players',pose,(x,y,0.),PLAYER_HEIGHT_METRES,colours)

        if index==0 and celebration.retrieving and age>=2.6:
            # A cosmetic held-ball sprite follows the athlete; match physics stay frozen.
            from retro_props import cache
            from kivy.graphics import Color,Rectangle
            from retro_sprites import projected_scale
            character,clip,frame=renderer.sample('celebration_0','players',pose)
            joints=clip['joints'][pose.view][frame];a,b=joints['wrist_0'],joints['wrist_1'];mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2;ax,ay=character['anchor']
            if pose.flipped:mx=character['canvas'][0]-mx;ax=character['canvas'][0]-ax
            scale=projected_scale(game,(x,y,0),character);px,py=game.project(x,y,0);px+=(mx-ax)*scale;py+=(ay-my)*scale;r=scale*3.
            from retro_props import uv
            texture=cache(game).get('ball.png')
            Color(1,1,1,1);Rectangle(texture=texture,tex_coords=uv(texture,0,0,8,1),pos=(px-r,py-r),size=(r*2,r*2))
