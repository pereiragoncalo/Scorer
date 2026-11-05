"""Capacity-based ground geometry and separate home/away supporter batches."""
import math
from kivy.graphics import Color,Line,Mesh,PushMatrix,PopMatrix,Translate
from kivy.metrics import dp
from club_profiles import stadium_capacity,profile,ground

def context(g):
    training=g.shot_context=='training'
    home=g.career.club if training or g.match_home is None else g.match_home
    away=None if training else g.match_away
    def kit(club):
        if club is None:return g.career.kit_for_club(g.career.club) if g.career.club else ((.2,.4,.7,1),)*4
        return g.career.kit_for_club(club)
    home_kit=kit(home);away_kit=kit(away)
    capacity=stadium_capacity(home)
    away_name=g.career.display_club(away) if away else ''
    banner=(profile(away)['supporters'] or away_name) if away else ''
    key=(getattr(home,'uid',''),getattr(away,'uid',''),capacity,home_kit,away_kit,banner,training)
    return dict(home=home,away=away,home_kit=home_kit,away_kit=away_kit,ground=ground(capacity),banner=banner,key=key)

def away_seat(x,y,tier=0,section='goal'):
    # Positive world x is left of the goal in the fixed broadcast camera.
    return tier==0 and section=='goal' and 10<=x<=29

def build(g,ctx):
    spec=ctx['ground'];g.stadium_tiers=spec.tiers;g.stadium_capacity=spec.capacity
    g._crowd_specs=[];g._stand_mesh_builders={}
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
                if code%29 in (0,1):continue
                x,y,_=corner(radius+.4,(col+.5)*math.pi/(2*columns),z)
                g._crowd_specs.append((x,y,z,code,'home',tier))
            for col in range(164):
                x=-35.5+col*71/163;code=col*17+row*31+tier*137
                if col%27 in (0,1) or code%37 in (0,1):continue
                team='away' if ctx['away'] and away_seat(x,near,tier) else 'home'
                g._crowd_specs.append((x,near-.4,z,code,team,tier))
            for col in range(80):
                code=col*19+row*31+tier*137
                if col%20 in (0,1) or code%37 in (0,1):continue
                g._crowd_specs.append((sx+.4,-3.5+col*35/79,z,code,'home',tier))
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
    build_crowd(g,g._crowd_specs,ctx)
    g._crowd_specs=None

def build_crowd(g,spectators,ctx=None):
    ctx=ctx or context(g);batches={};skins=((.94,.72,.52,.96),(.72,.46,.29,.96),(.45,.27,.18,.96))
    visible=0;team_counts={'home':0,'away':0}
    def add(team,group,color,points):
        vertices,indices=batches.setdefault((team,group,color),([],[]));g._append_mesh_quad(vertices,indices,points)
    for spectator in spectators:
        if len(spectator)==6:
            x,y,z,code,team,tier=spectator
        elif len(spectator)==4:x,y,z,code=spectator;team='home';tier=0
        else:continue
        foot=g.project(x,y,z+.05);top=g.project(x,y,z+.29);head=g.project(x,y,z+.38)
        if not(g.x-8<=head[0]<=g.right+8 and g.y-8<=head[1]<=g.top+8):continue
        visible+=1;team_counts[team]+=1;scale=g.pixels_per_meter(x,y,z+.2)
        width=max(.82,min(1.95,scale*.041));radius=max(1.15,min(2.75,scale*.062));dx=top[0]-foot[0];dy=top[1]-foot[1];length=max(1e-6,math.hypot(dx,dy));nx=-dy/length*width;ny=dx/length*width
        kit=ctx['away_kit'] if team=='away' else ctx['home_kit'];base=kit[0 if (code//4)%3 else 3];shade=.90+((code//13)%2)*.08;color=tuple(min(1,v*shade) for v in base[:3])+(.98,)
        group=code%4
        add(team,group,color,((foot[0]-nx,foot[1]-ny),(foot[0]+nx,foot[1]+ny),(top[0]+nx,top[1]+ny),(top[0]-nx,top[1]-ny)))
        add(team,group,skins[(code//2)%3],((head[0]-radius,head[1]-radius),(head[0]+radius,head[1]-radius),(head[0]+radius,head[1]+radius),(head[0]-radius,head[1]+radius)))
    g.crowd_total=len(spectators);g.crowd_visible=visible;g.crowd_team_counts=team_counts
    g._crowd_mesh_cache=[(color,v,i,group,team) for (team,group,color),(v,i) in batches.items() if i]

def cheering(g):
    return getattr(g,'_celebrating_side',None) if g.elapsed<getattr(g,'_crowd_celebrate_until',0) and g.shot_context!='training' else None

def jump(g,team,group):
    if cheering(g)!=team:return 0.
    age=max(0,g.elapsed-getattr(g,'_crowd_celebration_started',g.elapsed))
    return max(0,math.sin(age*11.5+group*1.25))*dp(4+group*.6)

def draw_crowd(g):
    for color,vertices,indices,group,team in g._crowd_mesh_cache:
        Color(*color);amount=jump(g,team,group)
        if amount:
            PushMatrix();Translate(0,amount,0);Mesh(vertices=vertices,indices=indices,mode='triangles');PopMatrix()
        else:Mesh(vertices=vertices,indices=indices,mode='triangles')

def draw_banner(g,ctx):
    if not ctx['away'] or not g._show_stadium_crowd():return
    kit=ctx['away_kit'];corners=[g.project(*p) for p in ((10,-4.1,.55),(29,-4.1,.55),(29,-4.1,1.6),(10,-4.1,1.6))]
    Color(*(tuple(v*.3 for v in kit[0][:3])+(1,)));vertices=[];indices=[];g._append_mesh_quad(vertices,indices,tuple(corners));Mesh(vertices=vertices,indices=indices,mode='triangles')
    Color(*kit[3]);Line(points=[coordinate for p in corners+[corners[0]] for coordinate in p],width=1.2)
    center=g.project(19.5,-4.1,1.13);width=abs(corners[1][0]-corners[0][0])-dp(4)
    g.away_banner_text=ctx['banner'];g.away_banner_bounds=(min(p[0] for p in corners),min(p[1] for p in corners),max(p[0] for p in corners),max(p[1] for p in corners))
    g._draw_text(ctx['banner'],*center,dp(8),(.98,.98,.94,1),'center',max_width=max(1,width),localize=False)
