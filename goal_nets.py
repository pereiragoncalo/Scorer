"""Stable per-stadium net dressings; box collisions share the visible geometry.

Goal mouth, posts and goal-line scoring never depend on the dressing. The default
legacy veil remains authoritative for its two variants. All assignments use the
home club UID, including training, without consuming gameplay RNG.
"""
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import math
from career import GOAL_DEPTH, clamp

@dataclass(frozen=True)
class NetStyle:
    structure:str
    mesh:str

STYLES=tuple(NetStyle(s,m) for s in ('veil','box') for m in ('square','hexagon'))

@lru_cache(maxsize=4096)
def for_stadium(uid):
    digest=hashlib.sha256(('scorer-net-v1:'+str(uid)).encode()).digest()
    return STYLES[int.from_bytes(digest[:4],'big')%len(STYLES)]

def stadium_style(g):
    override=getattr(g,'_goal_net_style_override',None)
    if override is not None:return override
    home=g.career.club if g.shot_context=='training' or g.match_home is None else g.match_home
    return for_stadium(home.uid) if home is not None else STYLES[0]

def box_profile(amount,height):
    distance=clamp(amount,0.,1.)*(GOAL_DEPTH+height)
    return (-distance,height) if distance<=GOAL_DEPTH else (-GOAL_DEPTH,max(0.,height-(distance-GOAL_DEPTH)))

def box_point(g,surface,u,v):
    hw,h=g.goal_half_width,g.goal_height
    if surface=='back':
        y,z=box_profile(v,h);x=-hw+g.goal_width*u
    else:
        x=-hw if surface=='left' else hw;y=-GOAL_DEPTH*u;z=h*v
    # One world-space deformation field for all three sheets. Shared seams
    # remain identical even when roof, rear and side ripples overlap.
    across=(x+hw)/g.goal_width;depth=-y/GOAL_DEPTH;vertical=z/h
    back_v=(GOAL_DEPTH+h-z)/(GOAL_DEPTH+h);roof_v=-y/(GOAL_DEPTH+h)
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
        width=g.goal_width if surface=='back' else GOAL_DEPTH
        height=(GOAL_DEPTH+g.goal_height if box else g.goal_geometry.veil_path_length) if surface=='back' else g.goal_height
        vertices=[];indices=[]
        def point(a):
            x,z=a
            if surface=='back':return x/width,z/height
            top=g.goal_height if box else g._veil_height_at_y(-x)
            if z>top+1e-7:return None
            return (x/GOAL_DEPTH if box else g._veil_amount_at_y(-x)),z/top if top>1e-7 else 0.
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

def draw_box_frame(g):
    from kivy.graphics import Color,Line
    hw,h=g.goal_half_width,g.goal_height
    tube=max(1.4,g.pixels_per_meter(0,0,h*.5)*.055)
    def line(points,width):Line(points=[n for p in points for n in g.project(*p)],width=width)
    # Exactly three separate poles, set behind the vertical back panel. Thin
    # cords tension the upper edge. No iron stanchions extend from the goal.
    for x in (-hw-.35,0.,hw+.35):
        Color(.43,.48,.49,1);line(((x,-GOAL_DEPTH-1.,0),(x,-GOAL_DEPTH-1.,h+.65)),tube*.55)
        Color(.85,.88,.82,.9);line(((x,-GOAL_DEPTH-1.,h+.60),(clamp(x,-hw,hw),-GOAL_DEPTH,h)),max(.6,tube*.22))
    Color(.94,.97,.98,1)
    line(((-hw,0,0),(-hw,0,h),(hw,0,h),(hw,0,0)),tube)
    Color(.89,.92,.86,.85)
    line(((-hw,0,h),(-hw,-GOAL_DEPTH,h),(hw,-GOAL_DEPTH,h),(hw,0,h)),max(.6,tube*.22))
    line(((-hw,0,0),(-hw,-GOAL_DEPTH,0),(hw,-GOAL_DEPTH,0),(hw,0,0)),max(.6,tube*.22))

def collide_box(g,old_x=None,old_y=None,old_z=None):
    b=g.ball;hw,h,r=g.goal_half_width,g.goal_height,g.ball.radius
    speed=max(1.,b.speed)
    # Swept planes: high-speed balls stop at their FIRST roof/back/side contact.
    if old_x is not None:
        old=(old_x,old_y,old_z);end=(b.x,b.y,b.z);hits=[]
        for axis,plane,direction,surface in ((1,-GOAL_DEPTH+r,-1,'back'),(2,h-r,1,'roof'),(0,-hw+r,-1,'left'),(0,hw-r,1,'right')):
            delta=end[axis]-old[axis]
            if delta*direction<=0:continue
            t=(plane-old[axis])/delta
            if not 0<=t<=1:continue
            p=tuple(old[i]+(end[i]-old[i])*t for i in range(3))
            if -GOAL_DEPTH-r<=p[1]<=0 and abs(p[0])<=hw+r and 0<=p[2]<=h+r:hits.append((t,p,surface))
        if hits:
            _,p,_=min(hits);b.x,b.y,b.z=p
    within=abs(b.x)<=hw+r and 0<=b.z<=h+r
    if b.y<=-GOAL_DEPTH+r+.0001 and within and b.vy<0:
        b.y=-GOAL_DEPTH+r;b.vy=abs(b.vy)*.18;b.vx*=.62;b.vz*=.58
        g._add_ripple('back',(b.x+hw)/g.goal_width,(GOAL_DEPTH+h-b.z)/(GOAL_DEPTH+h),speed)
    if -GOAL_DEPTH<=b.y<=0 and abs(b.x)<=hw+r and b.z>=h-r-.0001 and b.vz>0:
        b.z=h-r;b.vz=-abs(b.vz)*.20;b.vx*=.64;b.vy*=.64
        g._add_ripple('back',(b.x+hw)/g.goal_width,-b.y/(GOAL_DEPTH+h),speed)
    if -GOAL_DEPTH<=b.y<=0 and 0<=b.z<=h+r:
        for sign,surface in ((-1,'left'),(1,'right')):
            if b.x*sign>=hw-r-.0001 and b.vx*sign>0:
                b.x=sign*(hw-r);b.vx=-sign*clamp(abs(b.vx)*.11,.38,1.45)
                b.vy=min(b.vy*.30,-.42);b.vz=min(b.vz*.16,-.58)
                g._add_ripple(surface,-b.y/GOAL_DEPTH,b.z/h,speed)

