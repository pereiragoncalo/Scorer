"""Approved retro actor presentation. Reads game state; never advances simulation.

World positions, keeper skeleton, ball and collision volumes remain authoritative.
The authored dive's root motion is removed by aligning its hip with the existing
world skeleton; this prevents adding the PNG's travel to physical keeper travel.
"""
from dataclasses import dataclass
import math
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate, Rotate, Ellipse
from sprite_animation import Animation, load_manifest
from sprite_textures import TextureCache

PLAYER_HEIGHT_METRES = 1.80

def projected_scale(game,position,character,world_height=PLAYER_HEIGHT_METRES):
    """Scale the upright ink, not the transparent canvas or old physics scales."""
    x,y,_=position
    foot=game.project(x,y,0.)
    top=game.project(x,y,world_height)
    return max(.15,math.hypot(top[0]-foot[0],top[1]-foot[1])/character.get('standing_height_pixels',character['nominal_height']))

@dataclass(frozen=True)
class Pose:
    state: str
    age: float = 0.0
    frame: object = None
    view: str = 'front'
    flipped: bool = False


def kit_palette(kit):
    """Game order: shirt/shorts/socks/trim. Sprite order: shirt/trim/shorts/socks/gloves."""
    def colour(rgba):
        return ''.join(f'{max(0,min(255,round(c*255))):02X}' for c in rgba[:3])
    shirt,shorts,socks,trim=kit
    return (colour(shirt),colour(trim),colour(shorts),colour(socks),'F9FDF1')


def hero_pose(game,flipped=False):
    if game.state==game.STATE_BUILDUP:
        return Pose('RUN',game.state_age,view='back',flipped=flipped)
    state='HEADER' if game.shot_type=='header' else 'SHOOT'
    if game.state==game.STATE_AIMING:
        # Wind-up occurs before launch. Launch is still immediate at the real
        # physics event; the first post-launch frame is the authored contact.
        frame=min(1 if state=='HEADER' else 2,int(game.state_age*10))
    else:
        # Existing headers arrive at 1.31m. At the new 1.80m standing size,
        # meet these low balls crouched, rather than jumping above them.
        contact=5 if state=='HEADER' else 3
        frame=min(7,contact+int(game.player_kick_progress*(3 if state=='HEADER' else 5)))
    return Pose(state,frame=frame,view='back',flipped=flipped)


def field_pose(game,player,flipped=False):
    if game.state!=game.STATE_BUILDUP:
        # Existing match actors freeze during aiming. Do not invent tackles
        # or falls when the simulation has emitted no such action.
        age=game.frozen_scene_time if game.frozen_scene_time is not None else game.elapsed
        return Pose('IDLE',age+player.phase,flipped=flipped)
    delivery=game.current_opportunity
    if player in game.buildup_actors:
        if delivery.kind=='cutback' and game.buildup_progress<.5:
            return Pose('DRIBBLE',game.state_age,flipped=flipped)
        start=delivery.duration*.5 if delivery.kind=='cutback' else 0.
        age=max(0.,game.state_age-start)
        state='SHOOT' if delivery.kind=='rebound' else 'PASS'
        contact=3 if state=='SHOOT' else 2
        fps=12 if state=='SHOOT' else 10
        end=7 if state=='SHOOT' else 5
        if age>(end-contact+1)/fps:return Pose('IDLE',age,flipped=flipped)
        return Pose(state,frame=min(end,contact+int(age*fps)),flipped=flipped)
    if player is game.buildup_blocker:
        # This is the existing rebound block, not a new tackling mechanic.
        age=game.state_age-delivery.duration*.5
        if -.18<=age<=.45:
            return Pose('TACKLE',max(0.,age+.18),flipped=flipped)
    return Pose('RUN',game.state_age+player.phase,flipped=flipped)


def keeper_pose(game,right_on_screen=True):
    if game.goalkeeper_holding:
        return Pose('CATCH',game.goalkeeper_catch_age)
    if game.goalkeeper_is_diving:
        if game.state==game.STATE_RESULT and not game.ball.active and game.state_age>1.0:
            return Pose('RECOVER',game.state_age-1.)
        high=game.goalkeeper_high_reach
        if high>.6 and game.goalkeeper_dive_amount<.35:state='HIGH_SAVE'
        elif game.goalkeeper_low_reach>.6 and game.goalkeeper_dive_amount<.35:state='LOW_SAVE'
        else:state='DIVE_RIGHT' if right_on_screen else 'DIVE_LEFT'
        # Match the original impulse/flight/landing interval, not the timer's
        # ever-increasing result-screen age.
        duration=.76 if high>.6 else .66
        count=6 if state=='LOW_SAVE' else 8
        frame=min(count-1,int(game.goalkeeper_dive_age/duration*count))
        return Pose(state,frame=frame)
    return Pose('MOVE' if abs(game.goalkeeper_vx)>.08 else 'READY',game.elapsed)


class RetroSprites:
    def __init__(self):
        self.manifest=load_manifest()
        self.cache=TextureCache(self.manifest,limit=24)
        self.clocks={}

    def sample(self,key,role,pose):
        character=self.manifest['characters'][role]
        if key not in self.clocks:self.clocks[key]=(Animation(character,pose.state),None)
        animation,last_age=self.clocks[key]
        if animation.state!=pose.state or last_age is None or pose.age<last_age:
            animation.select(pose.state);last_age=0.
        animation.repeat=False
        animation.update(max(0.,pose.age-last_age))
        self.clocks[key]=(animation,pose.age)
        frame=animation.frame if pose.frame is None else int(pose.frame)
        clip=character['animations'][pose.state]
        return character,clip,min(clip['frames']-1,max(0,frame))

    def clear_field(self,live_keys):
        for key in list(self.clocks):
            if isinstance(key,int) and key not in live_keys:del self.clocks[key]

    def draw(self,game,key,role,pose,position,world_height,colours,joint=None,target=None,rotation=0.):
        character,clip,frame=self.sample(key,role,pose)
        texture,uv=self.cache.frame(character,clip,pose.view,frame,colours)
        w,h=character['canvas'];ax,ay=character['anchor']
        if joint is not None:
            joints=clip['joints'][pose.view][frame]
            names=joint if isinstance(joint,tuple) else (joint,)
            ax=sum(joints[n][0]+.5 for n in names)/len(names)
            ay=sum(joints[n][1]+.5 for n in names)/len(names)
        if pose.flipped:
            ax=w-ax
            uv=(uv[2],uv[3],uv[0],uv[1],uv[6],uv[7],uv[4],uv[5])
        x,y,z=position
        foot=game.project(x,y,0.)
        scale=projected_scale(game,position,character,world_height)
        sx,sy=target if target is not None else game.project(x,y,z)
        Color(0.01,.025,.015,.28)
        Ellipse(pos=(foot[0]-scale*5,foot[1]-scale*1.2),size=(scale*10,scale*2.4))
        Color(1,1,1,1)
        PushMatrix();Translate(sx,sy,0)
        if rotation:Rotate(angle=rotation,axis=(0,0,1))
        Rectangle(texture=texture,tex_coords=uv,pos=(-ax*scale,-(h-ay)*scale),size=(w*scale,h*scale))
        PopMatrix()
