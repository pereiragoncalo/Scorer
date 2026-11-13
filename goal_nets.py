"""Stable per-stadium net dressings; box collisions share the visible geometry.

Goal mouth, posts and goal-line scoring never depend on the dressing. The default
legacy veil remains authoritative for its two variants. All assignments use the
home club UID, including training, without consuming gameplay RNG.
"""
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import math
from career import GOAL_DEPTH, VEIL_TOP_DEPTH, clamp

@dataclass(frozen=True)
class NetStyle:
    structure:str
    mesh:str
    depth:float=GOAL_DEPTH

BASE_STYLES=tuple(NetStyle(s,m) for s in ('veil','box') for m in ('square','hexagon'))
STYLES=BASE_STYLES+tuple(NetStyle(s,m,d) for s,d in (('box',1.80),('veil',3.50)) for m in ('square','hexagon'))

@lru_cache(maxsize=4096)
def for_stadium(uid):
    digest=hashlib.sha256(('scorer-net-v1:'+str(uid)).encode()).digest()
    base=BASE_STYLES[int.from_bytes(digest[:4],'big')%len(BASE_STYLES)]
    # Independent selector preserves most original stadium dressings.
    return NetStyle(base.structure,base.mesh,1.80 if base.structure=='box' else 3.50) if digest[4]%3==0 else base

def stadium_style(g):
    override=getattr(g,'_goal_net_style_override',None)
    if override is not None:return override
    home=g.career.club if g.shot_context=='training' or g.match_home is None else g.match_home
    return for_stadium(home.uid) if home is not None else STYLES[0]

def box_profile(amount,height,depth=GOAL_DEPTH):
    distance=clamp(amount,0.,1.)*(depth+height)
    return (-distance,height) if distance<=depth else (-depth,max(0.,height-(distance-depth)))

def box_point(g,surface,u,v):
    hw,h=g.goal_half_width,g.goal_height
    if surface=='back':
        y,z=box_profile(v,h,g.goal_net_depth);x=-hw+g.goal_width*u
    else:
        x=-hw if surface=='left' else hw;y=-g.goal_net_depth*u;z=h*v
    # One world-space deformation field for all three sheets. Shared seams
    # remain identical even when roof, rear and side ripples overlap.
    across=(x+hw)/g.goal_width;depth=-y/g.goal_net_depth;vertical=z/h
    back_v=(g.goal_net_depth+h-z)/(g.goal_net_depth+h);roof_v=-y/(g.goal_net_depth+h)
    rear=g._net_displacement('back',across,back_v)*depth**3
    roof=g._net_displacement('back',across,roof_v)*vertical**3*depth
    left=g._net_displacement('left',depth,vertical)*(1-across)**3*depth
    right=g._net_displacement('right',depth,vertical)*across**3*depth
    return g.project(x-left+right,y-rear,z+roof)

@lru_cache(maxsize=32)
def lattice(width,height,mesh,cell=.24):
    """Unique physical line segments, clipped to a rectangular unrolled sheet."""
    edges={}
    def add(a,b):
        # Liang-Barsky segment clip retains partial boundary cells.
        dx,dy=b[0]-a[0],b[1]-a[1];lo,hi=0.,1.
        for p,q in ((-dx,a[0]),(dx,width-a[0]),(-dy,a[1]),(dy,height-a[1])):
            if abs(p)<1e-10:
                if q<0:return
            elif p<0:lo=max(lo,q/p)
            else:hi=min(hi,q/p)
        if lo>=hi:return
        aa=(round(a[0]+dx*lo,7),round(a[1]+dy*lo,7));bb=(round(a[0]+dx*hi,7),round(a[1]+dy*hi,7))
        if aa!=bb:edges[tuple(sorted((aa,bb)))]=(aa,bb)
    size=cell*.625
    if mesh=='hexagon':
        step=math.sqrt(3)*size
        for column in range(-1,math.ceil(width/(1.5*size))+2):
            for row in range(-1,math.ceil(height/step)+2):
                cx=column*1.5*size;cy=(row+.5*(column%2))*step
                points=tuple((cx+size*math.cos(i*math.pi/3),cy+size*math.sin(i*math.pi/3)) for i in range(6))
                for i in range(6):add(points[i],points[(i+1)%6])
    else:
        for i in range(math.ceil(width/cell)+1):
            x=width*i/math.ceil(width/cell);add((x,0),(x,height))
        for i in range(math.ceil(height/cell)+1):
            y=height*i/math.ceil(height/cell);add((0,y),(width,y))
    return tuple(edges.values())

def draw_net(g):
    from kivy.graphics import Color,Mesh
    box=g.goal_net_style.structure=='box';hexagon=g.goal_net_style.mesh=='hexagon'
    # Segments are subdivided for ripples; every batch stays far below uint16.
    for surface in ('back','left','right'):
        width=g.goal_width if surface=='back' else g.goal_net_depth
        height=(g.goal_net_depth+g.goal_height if box else g.veil_path_length) if surface=='back' else g.goal_height
        vertices=[];indices=[]
        def point(a):
            x,z=a
            if surface=='back':return x/width,z/height
            top=g.goal_height if box else g._veil_height_at_y(-x)
            if z>top+1e-7:return None
            return (x/g.goal_net_depth if box else g._veil_amount_at_y(-x)),z/top if top>1e-7 else 0.
        for a,b in lattice(width,height,'hexagon' if hexagon else 'square'):
            steps=max(1,math.ceil(math.dist(a,b)/.18))
            for i in range(steps):
                aa=tuple(a[j]+(b[j]-a[j])*i/steps for j in (0,1));bb=tuple(a[j]+(b[j]-a[j])*(i+1)/steps for j in (0,1))
                pa,pb=point(aa),point(bb)
                if pa is None or pb is None:continue
                for uv in (pa,pb):
                    pos=g._net_point(surface,*uv);indices.append(len(vertices)//4);vertices.extend((*pos,0.,0.))
        Color(.95,.97,.94,.74 if hexagon else .84)
        # Single-pixel threads retain open cells on GLES2, no filled blue sheet.
        Mesh(vertices=vertices,indices=indices,mode='lines')

def draw_rear_supports(g):
    from kivy.graphics import Color,Line
    hw,h=g.goal_half_width,g.goal_height
    tube=max(1.4,g.pixels_per_meter(0,0,h*.5)*.055)
    def line(points,width):Line(points=[n for p in points for n in g.project(*p)],width=width)
    depth=g.goal_net_depth
    net_depth=depth if g.goal_net_style.structure=='box' else VEIL_TOP_DEPTH
    # Exactly three separate poles, set behind the upper net edge. Thin
    # cords tension the upper edge. No iron stanchions extend from the goal.
    for x in (-hw-.35,0.,hw+.35):
        Color(.43,.48,.49,1);line(((x,-depth-1.,0),(x,-depth-1.,h+.65)),tube*.55)
        Color(.85,.88,.82,.9)
        cloth=getattr(g,'_net_cloth',None)
        if cloth is not None and hasattr(cloth,'tethers'):
            index,endpoint,_=min(cloth.tethers,key=lambda tie:abs(tie[1][0]-x))
            end=tuple(cloth.positions[index]);mid=tuple((endpoint[i]+end[i])*.5-(.035 if i==2 else 0.) for i in range(3))
            line((endpoint,mid,end),max(.6,tube*.22))
        else:line(((x,-depth-1.,h+.60),(clamp(x,-hw,hw),-net_depth,h)),max(.6,tube*.22))

def draw_front_frame(g):
    from kivy.graphics import Color,Line
    hw,h=g.goal_half_width,g.goal_height
    tube=max(1.4,g.pixels_per_meter(0,0,h*.5)*.055)
    Color(.94,.97,.98,1)
    Line(points=[n for p in ((-hw,0,0),(-hw,0,h),(hw,0,h),(hw,0,0)) for n in g.project(*p)],width=tube)

def draw_box_frame(g):
    from kivy.graphics import Color,Line
    hw,h=g.goal_half_width,g.goal_height
    tube=max(1.4,g.pixels_per_meter(0,0,h*.5)*.055)
    def line(points,width):Line(points=[n for p in points for n in g.project(*p)],width=width)
    draw_rear_supports(g)
    draw_front_frame(g)
    Color(.89,.92,.86,.85)
    line(((-hw,0,h),(-hw,-g.goal_net_depth,h),(hw,-g.goal_net_depth,h),(hw,0,h)),max(.6,tube*.22))
    line(((-hw,0,0),(-hw,-g.goal_net_depth,0),(hw,-g.goal_net_depth,0),(hw,0,0)),max(.6,tube*.22))

def collide_box(g,old_x=None,old_y=None,old_z=None):
    b=g.ball;hw,h,r=g.goal_half_width,g.goal_height,g.ball.radius
    speed=max(1.,b.speed)
    # Swept planes: high-speed balls stop at their FIRST roof/back/side contact.
    if old_x is not None:
        old=(old_x,old_y,old_z);end=(b.x,b.y,b.z);hits=[]
        for axis,plane,direction,surface in ((1,-g.goal_net_depth+r,-1,'back'),(2,h-r,1,'roof'),(0,-hw+r,-1,'left'),(0,hw-r,1,'right')):
            delta=end[axis]-old[axis]
            if delta*direction<=0:continue
            t=(plane-old[axis])/delta
            if not 0<=t<=1:continue
            p=tuple(old[i]+(end[i]-old[i])*t for i in range(3))
            if -g.goal_net_depth-r<=p[1]<=0 and abs(p[0])<=hw+r and 0<=p[2]<=h+r:hits.append((t,p,surface))
        if hits:
            _,p,_=min(hits);b.x,b.y,b.z=p
    within=abs(b.x)<=hw+r and 0<=b.z<=h+r
    if b.y<=-g.goal_net_depth+r+.0001 and within and b.vy<0:
        b.y=-g.goal_net_depth+r;b.vy=abs(b.vy)*.18;b.vx*=.62;b.vz*=.58
        g._add_ripple('back',(b.x+hw)/g.goal_width,(g.goal_net_depth+h-b.z)/(g.goal_net_depth+h),speed)
    if -g.goal_net_depth<=b.y<=0 and abs(b.x)<=hw+r and b.z>=h-r-.0001 and b.vz>0:
        b.z=h-r;b.vz=-abs(b.vz)*.20;b.vx*=.64;b.vy*=.64
        g._add_ripple('back',(b.x+hw)/g.goal_width,-b.y/(g.goal_net_depth+h),speed)
    if -g.goal_net_depth<=b.y<=0 and 0<=b.z<=h+r:
        for sign,surface in ((-1,'left'),(1,'right')):
            if b.x*sign>=hw-r-.0001 and b.vx*sign>0:
                b.x=sign*(hw-r);b.vx=-sign*clamp(abs(b.vx)*.11,.38,1.45)
                b.vy=min(b.vy*.30,-.42);b.vz=min(b.vz*.16,-.58)
                g._add_ripple(surface,-b.y/g.goal_net_depth,b.z/h,speed)

