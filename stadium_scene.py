"""Capacity-based ground geometry and separate home/away supporter batches."""
import math
import zlib
from kivy.graphics import Color,Mesh,PushMatrix,PopMatrix,Translate
from kivy.metrics import dp
from club_profiles import stadium_capacity,ground
from supporter_layout import AwaySector,STAIR_HALF_WIDTH
from attendance import fixture_snapshot,occupied_seats
from retro_props import cache as scene_cache,uv

def context(g):
    training=g.shot_context=='training'
    home=g.career.club if training or g.match_home is None else g.match_home
    away=None if training else g.match_away
    def kit(club):
        if club is None:return g.career.kit_for_club(g.career.club) if g.career.club else ((.2,.4,.7,1),)*4
        return g.career.kit_for_club(club)
    home_kit=kit(home);away_kit=kit(away)
    capacity=stadium_capacity(home)
    away_capacity=stadium_capacity(away) if away else 0
    home_uid=getattr(home,'uid','');away_uid=getattr(away,'uid','')
    seed=zlib.crc32((home_uid+'|'+away_uid).encode('utf-8'))
    turnout={'home':0.,'away':0.} if training else fixture_snapshot(g,home,away)
    key=(home_uid,away_uid,capacity,away_capacity,home_kit,away_kit,training,tuple(sorted(turnout.items())))
    return dict(turnout=turnout,home=home,away=away,home_kit=home_kit,away_kit=away_kit,ground=ground(capacity),away_sector=AwaySector(away_capacity,away is not None),crowd_seed=seed,key=key)

def seat_noise(x,y,z,code,seed=0):
    """Stable per-seat randomness, with no stripes or gameplay RNG consumption."""
    value=(seed ^ (round(x*100)*0x1f123bb5) ^ (round(y*100)*0x5f356495)
           ^ (round(z*100)*0x6c8e9cf5) ^ (code*0x9e3779b9)) & 0xffffffff
    value=((value^(value>>16))*0x7feb352d)&0xffffffff
    value=((value^(value>>15))*0x846ca68b)&0xffffffff
    return value^(value>>16)

def away_seat(x,y,tier=0,section='goal',capacity=40000):
    # Positive world x is left of the goal in the fixed broadcast camera.
    return AwaySector(capacity).contains(x,tier,section)

def build(g,ctx):
    spec=ctx['ground'];g.stadium_tiers=spec.tiers;g.stadium_capacity=spec.capacity
    g._crowd_specs=[];g._stand_mesh_builders={}
    sector=ctx['away_sector'];g.away_sector_extended=sector.extended
    g.steward_positions=[]
    edge=(.42,.46,.44,1);tread=(.25,.28,.27,1);riser=(.12,.16,.16,1)
    def quad(points,color):g._cache_stand_quad(color,tuple(g.project(*p) for p in points))
    lower_height=.3+spec.lower_rows*.27
    for tier,rows in enumerate((spec.lower_rows,spec.upper_rows)):
        if not rows:continue
        depth=0 if tier==0 else spec.lower_rows*.85+3.5
        base=.3 if tier==0 else lower_height+1.8
        g._stand_cache_section='tier:'+str(tier)
        for row in reversed(range(rows)):
            near=-4-depth-row*.85;far=near-.8;z=base+row*(.27 if tier==0 else .24)
            # Concrete steps behind the goal and down the far touchline.
            quad(((-36.2,near,z-.25),(36.2,near,z-.25),(36.2,near,z),(-36.2,near,z)),riser)
            quad(((-36.2,near,z),(36.2,near,z),(36.2,far,z),(-36.2,far,z)),tread)
            g._cache_stand_world_polyline(edge,[(-36.2,near,z),(36.2,near,z)],.65)
            sx=36.2+depth+row*.85
            quad(((sx,-4,z-.25),(sx,32,z-.25),(sx,32,z),(sx,-4,z)),riser)
            quad(((sx,-4,z),(sx,32,z),(sx+.8,32,z),(sx+.8,-4,z)),tread)
            g._cache_stand_world_polyline(edge,[(sx,-4,z),(sx,32,z)],.65)
            if tier==0 and sector.enabled:
                # Visible stair treads at the two ends of the visitor sector.
                left=sector.goal_stair_x-STAIR_HALF_WIDTH;right=sector.goal_stair_x+STAIR_HALF_WIDTH
                stair_colour=(.37,.39,.35,1)
                quad(((left,near,z+.006),(right,near,z+.006),(right,far,z+.006),(left,far,z+.006)),stair_colour)
                quad(((sx,-4.1,z+.006),(sx,-2.85,z+.006),(sx+.8,-2.85,z+.006),(sx+.8,-4.1,z+.006)),stair_colour)
                g.steward_positions.extend(sector.stewards(sx,near,z))
            # Connect the two straight stands with a real curved corner.
            radius=depth+row*.85
            def corner(r,angle,height):return (36.2+r*math.cos(angle),-4-r*math.sin(angle),height)
            for segment in range(12):
                a=segment*math.pi/24;b=(segment+1)*math.pi/24
                quad((corner(radius,a,z),corner(radius,b,z),corner(radius+.8,b,z),corner(radius+.8,a,z)),tread)
                quad((corner(radius,a,z-.25),corner(radius,b,z-.25),corner(radius,b,z),corner(radius,a,z)),riser)
            columns=max(2,min(72,round((radius+.4)*math.pi/.95)))
            for col in range(columns):
                code=col*23+row*41+tier*173
                x,y,_=corner(radius+.4,(col+.5)*math.pi/(2*columns),z)
                team='away' if sector.contains(x,tier,'corner') else 'home'
                g._crowd_specs.append((x,y,z,code,team,tier))
            for col in range(164):
                x=-35.5+col*71/163;code=col*17+row*31+tier*137
                if col%27 in (0,1) or sector.stair(x,near,tier):continue
                team='away' if sector.contains(x,tier) else 'home'
                g._crowd_specs.append((x,near-.4,z,code,team,tier))
            for col in range(80):
                code=col*19+row*31+tier*137
                y=-3.5+col*35/79
                if col%20 in (0,1) or sector.stair(sx,y,tier,'side'):continue
                g._crowd_specs.append((sx+.4,y,z,code,'home',tier))
        if tier:
            # Clear projecting balcony/concourse separates the upper deck from
            # the first tier, rather than merely adding more continuous rows.
            front=-4-depth
            fascia=tuple(v*.35 for v in ctx['home_kit'][0][:3])+(1,)
            quad(((-36.2,front,base-1.35),(36.2,front,base-1.35),(36.2,front,base-.1),(-36.2,front,base-.1)),fascia)
            g._cache_stand_world_polyline((.7,.73,.7,1),[(-36.2,front,base),(36.2,front,base)],1.4)
            x=36.2+depth
            quad(((x,-4,base-1.35),(x,32,base-1.35),(x,32,base-.1),(x,-4,base-.1)),fascia)
    g._stand_mesh_cache=[(color,vertices,indices) for (_,color),(vertices,indices) in g._stand_mesh_builders.items() if indices]
    g._stand_mesh_builders=None
    g.crowd_available=len(g._crowd_specs)
    seats=occupied_seats(g._crowd_specs,ctx['turnout'],lambda x,y,z,c:seat_noise(x,y,z,c,ctx['crowd_seed']))
    g.crowd_occupied_seats=tuple(seats);g.crowd_turnout=dict(ctx['turnout'])
    build_crowd(g,seats,ctx)
    build_stewards(g)
    g._crowd_specs=None

def build_crowd(g,spectators,ctx=None):
    from celebrations import crowd_profile
    ctx=ctx or context(g);batches={};g._crowd_textures={}
    visible=0;team_counts={'home':0,'away':0};g._crowd_motions=[];g._crowd_motion_scales=[];g._crowd_cells=[]
    for team in ('home','away'):
        kit=ctx['away_kit'] if team=='away' else ctx['home_kit']
        g._crowd_textures[team]=scene_cache(g).get('supporters.png',(kit[0],kit[3]))
    for spectator in spectators:
        if len(spectator)==6:x,y,z,code,team,tier=spectator
        elif len(spectator)==4:x,y,z,code=spectator;team='home';tier=0
        else:continue
        foot=g.project(x,y,z+.03);scale=g.pixels_per_meter(x,y,z+.2)
        height=max(4.,min(31.,scale*.72));width=height*2/3
        if not(g.x-width<=foot[0]<=g.right+width and g.y-height<=foot[1]<=g.top+height):continue
        visible+=1;team_counts[team]+=1;noise=seat_noise(x,y,z,code,ctx['crowd_seed']);column=noise%18
        body=((foot[0]-width/2,foot[1]),(foot[0]+width/2,foot[1]),(foot[0]+width/2,foot[1]+height),(foot[0]-width/2,foot[1]+height))
        vertices,indices=batches.setdefault(team,([],[]));start=len(vertices);g._append_mesh_quad(vertices,indices,body)
        texture=g._crowd_textures[team];frame=(noise>>8)&1;coords=uv(texture,column,frame,18,6)
        for j in range(4):vertices[start+j*4+2:start+j*4+4]=coords[j*2:j*2+2]
        baseline=tuple(p[1] for p in body)
        # Preserve the motion contract, with head and body now one sprite quad.
        g._crowd_motions.append((team,crowd_profile(noise),vertices,start,baseline,vertices,start,baseline))
        g._crowd_motion_scales.append(scale/30.);g._crowd_cells.append((column,frame,noise))
    g.crowd_total=len(spectators);g.crowd_visible=visible;g.crowd_team_counts=team_counts
    g._crowd_mesh_cache=[((1,1,1,1),v,i,0,team) for team,(v,i) in batches.items() if i]
    g._crowd_motion_offsets=[0.]*len(g._crowd_motions);g._crowd_motion_active=False

def cheering(g):
    return getattr(g,'_celebrating_side',None) if g.elapsed<getattr(g,'_crowd_celebrate_until',0) and g.shot_context!='training' else None

def build_stewards(g):
    vertices=[];indices=[];g.steward_visible=0
    g._steward_texture=scene_cache(g).get('supporters.png',((.46,1.,.015,1),(.9,1.,.65,1)))
    for index,(x,y,z,flank,file) in enumerate(g.steward_positions):
        foot=g.project(x,y,z+.03);height=max(4.,min(25.,g.pixels_per_meter(x,y,z+.2)*.58));width=height*2/3
        if not(g.x-width<=foot[0]<=g.right+width and g.y-height<=foot[1]<=g.top+height):continue
        g.steward_visible+=1;start=len(vertices)
        g._append_mesh_quad(vertices,indices,((foot[0]-width/2,foot[1]),(foot[0]+width/2,foot[1]),(foot[0]+width/2,foot[1]+height),(foot[0]-width/2,foot[1]+height)))
        coords=uv(g._steward_texture,(index%3)*3,0,18,6)
        for j in range(4):vertices[start+j*4+2:start+j*4+4]=coords[j*2:j*2+2]
    g._steward_mesh_cache=[((1,1,1,1),vertices,indices)] if indices else []

def jump(g,team,group):
    if cheering(g)!=team:return 0.
    age=max(0,g.elapsed-getattr(g,'_crowd_celebration_started',g.elapsed))
    from celebrations import crowd_jump
    return dp(crowd_jump(age,group))

def animate_crowd(g):
    side=cheering(g)
    if side is None and not getattr(g,'_crowd_motion_active',False):return
    age=max(0,g.elapsed-getattr(g,'_crowd_celebration_started',g.elapsed))
    remaining=max(0,getattr(g,'_crowd_celebrate_until',0)-g.elapsed)
    from celebrations import jump_displacement
    for index,(team,profile,bv,bs,by,hv,hs,hy) in enumerate(getattr(g,'_crowd_motions',())):
        fade=1. if remaining>=.65 else min(1.,remaining/(.2+profile[3]))
        amount=jump_displacement(age,profile)*g._crowd_motion_scales[index]*fade if side==team else 0.
        column,previous,noise=g._crowd_cells[index]
        frame=2+int(max(0.,age-profile[3])*profile[0]*.6+profile[1])%4 if side==team and age>profile[3] else (noise>>8)&1
        if frame!=previous:
            coords=uv(g._crowd_textures[team],column,frame,18,6)
            for j in range(4):bv[bs+j*4+2:bs+j*4+4]=coords[j*2:j*2+2]
            g._crowd_cells[index]=(column,frame,noise)
        if amount==g._crowd_motion_offsets[index]:continue
        for j in range(4):
            bv[bs+j*4+1]=by[j]+amount
            hv[hs+j*4+1]=hy[j]+amount
        g._crowd_motion_offsets[index]=amount
    g._crowd_motion_active=side is not None

def draw_crowd(g):
    animate_crowd(g)
    for color,vertices,indices,group,team in g._crowd_mesh_cache:
        Color(*color);Mesh(vertices=vertices,indices=indices,texture=g._crowd_textures[team],mode='triangles')
    # Stewards never join a team's goal celebration.
    for colour,vertices,indices in getattr(g,'_steward_mesh_cache',()):
        Color(*colour);Mesh(vertices=vertices,indices=indices,texture=g._steward_texture,mode='triangles')
