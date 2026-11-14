"""Scorer 1 cloth: gravity-loaded rest geometry and fixed-step Verlet springs.

This is presentation physics. It has no game, score, career, random or Kivy
imports. The existing ball/net collision and goal-line decision stay authoritative.
"""
from bisect import bisect_right
from dataclasses import asdict,dataclass
import math

@dataclass(frozen=True)
class NetConfig:
    net_slack: float = .20
    net_stiffness: float = 24.
    net_damping: float = 3.4
    net_gravity: float = 9.81
    net_impact_scale: float = .48
    net_max_stretch: float = 1.90
    net_wave_propagation: float = 48.
    net_settle_threshold: float = .0025

    def __post_init__(self):
        limits=((0,1.0),(8,80),(.8,12),(0,20),(.05,.9),(1.15,2.5),(5,120),(.0005,.015))
        for (name,value),(lo,hi) in zip(asdict(self).items(),limits):
            if type(value) not in (int,float) or not math.isfinite(value) or not lo<=value<=hi:
                raise ValueError('Invalid net parameter: '+name)

@dataclass(frozen=True)
class NetGeometry:
    structure: str = 'box'
    width: float = 7.32
    height: float = 2.44
    depth: float = 2.65
    top_depth: float = None
    ground_slack: float = .50
    veil_sag: float = .28

    def __post_init__(self):
        if self.top_depth is None:object.__setattr__(self,'top_depth',1.15 if self.structure=='rounded' else .55)
        if self.structure not in ('box','veil','rounded'):raise ValueError('Unknown net structure')
        if not all(math.isfinite(v) and v>0 for v in (self.width,self.height,self.depth)):raise ValueError('Invalid goal dimensions')
        if self.structure=='rounded' and not 0<self.top_depth<self.touch:raise ValueError('Invalid rounded net depth')

    @property
    def touch(self):return self.depth-self.ground_slack
    @property
    def slope(self):
        a,b=self.touch-self.top_depth,self.height
        if self.structure=='rounded':return math.pi*.25*(3*(a+b)-math.sqrt((3*a+b)*(a+3*b)))
        return math.hypot(a,b)
    @property
    def path(self):return self.depth+self.height if self.structure=='box' else self.top_depth+self.slope+self.ground_slack
    @property
    def hinge(self):return (self.depth if self.structure=='box' else self.top_depth)/self.path

    def profile(self,v):
        d=max(0,min(1,v))*self.path
        if self.structure=='box':return (-d,self.height) if d<=self.depth else (-self.depth,max(0,self.height-d+self.depth))
        if d<=self.top_depth:return -d,self.height
        t=(d-self.top_depth)/self.slope
        if self.structure=='rounded' and t<=1:
            angle=t*math.pi/2
            return -self.top_depth-(self.touch-self.top_depth)*(1-math.cos(angle)),self.height*(1-math.sin(angle))
        if t<=1:return -self.top_depth-(self.touch-self.top_depth)*t,max(0,self.height*(1-t)-self.veil_sag*math.sin(math.pi*t))
        return -self.touch-(d-self.top_depth-self.slope),0.

    def rounded_radius(self,z):
        return min(.65,self.width*.12)*math.sqrt(max(0.,1.-z/self.height))

    def rear_depth(self,z):
        ratio=max(0.,min(1.,1.-z/self.height))
        return self.top_depth+(self.touch-self.top_depth)*(1.-math.sqrt(max(0.,1.-ratio*ratio)))

    def point(self,surface,u,v):
        if surface=='back':
            y,z=self.profile(v)
            half=self.width/2-(self.rounded_radius(z) if self.structure=='rounded' else 0.)
            return (-half+2*half*u,y,z)
        y,top=(-self.depth*u,self.height) if self.structure=='box' else self.profile(u)
        z=top*v;half=self.width/2
        if self.structure=='rounded':
            radius=self.rounded_radius(z)
            if radius>1e-8:
                start=self.rear_depth(z)-radius
                along=max(0.,min(radius,-y-start))
                half-=radius-math.sqrt(max(0.,radius*radius-along*along))
        return ((-1 if surface=='left' else 1)*half,y,z)

    def uv_at(self,surface,position):
        x,y,z=position
        if self.structure=='box':
            if surface=='back':v=(-y if z>=self.height-.12 else self.depth+self.height-z)/self.path;u=(x+self.width/2)/self.width
            else:u=-y/self.depth;v=z/self.height
        else:
            lo,hi=0.,1.
            for _ in range(28):
                mid=(lo+hi)/2
                if self.profile(mid)[0]>y:lo=mid
                else:hi=mid
            amount=(lo+hi)/2
            if surface=='back':
                half=self.width/2-(self.rounded_radius(self.profile(amount)[1]) if self.structure=='rounded' else 0.)
                u=(x+half)/(2*half);v=amount
            else:
                u=amount;top=self.profile(u)[1];v=z/max(.001,top)
        return max(0,min(1,u)),max(0,min(1,v))

    def normal(self,surface,u,v):
        if surface!='back':
            if self.structure=='rounded':
                a,b=self.point(surface,max(0,u-.001),v),self.point(surface,min(1,u+.001),v)
                c,d=self.point(surface,u,max(0,v-.001)),self.point(surface,u,min(1,v+.001))
                du,dv=tuple(y-x for x,y in zip(a,b)),tuple(y-x for x,y in zip(c,d))
                n=(du[1]*dv[2]-du[2]*dv[1],du[2]*dv[0]-du[0]*dv[2],du[0]*dv[1]-du[1]*dv[0])
                sign=-1 if surface=='left' else 1
                if n[0]*sign<0:n=tuple(-x for x in n)
                length=math.sqrt(sum(x*x for x in n))
                if length>1e-10:return tuple(x/length for x in n)
            return (-1.,0.,0.) if surface=='left' else (1.,0.,0.)
        if self.structure=='box':return (0.,0.,1.) if v<self.hinge else (0.,-1.,0.)
        a,b=self.profile(max(0,v-.001)),self.profile(min(1,v+.001));dy,dz=b[0]-a[0],b[1]-a[1];length=math.hypot(dy,dz)
        return (0.,dz/max(1e-9,length),-dy/max(1e-9,length))

class NetCloth:
    STEP=1/120

    def __init__(self,geometry=NetGeometry(),config=NetConfig(),coarse=False):
        self.geometry,self.config=geometry,config
        self.generation=0;self.active=False;self.accumulator=0.;self.time=0.;self.quiet=0.;self.contact=None
        self.rest=[];self.pinned=[];self.grids={};self.links=[];self._lookup={};self._edges=set()
        nu,nv,side_v=(12,8,5) if coarse else (18,12,7)
        # Include the roof/back hinge exactly, not a diagonal across a box corner.
        path=sorted(set([i/nv for i in range(nv+1)]+[geometry.hinge]))
        if geometry.structure in ('veil','rounded'):path=sorted(set(path+[(geometry.top_depth+geometry.slope)/geometry.path]))
        if geometry.structure=='box':
            # Conforming rear seam: side height rows must also be rows of the
            # unrolled roof/back sheet. No independent hanging edge particles.
            path=sorted(set(path+[(geometry.depth+geometry.height*(1-i/side_v))/geometry.path for i in range(side_v+1)]))
        across=[i/nu for i in range(nu+1)];side=[i/side_v for i in range(side_v+1)]
        self._grid('back',across,path)
        side_us=path
        if geometry.structure=='box':
            side_us=sorted(set(round(-geometry.profile(v)[0]/geometry.depth,8) for v in path))
            side=sorted(set([round(geometry.profile(v)[1]/geometry.height,8) for v in path]))
        self._grid('left',side_us,side);self._grid('right',side_us,side)
        self.reset()

    def _rest_point(self,surface,u,v):
        g,c=self.geometry,self.config;x,y,z=g.point(surface,u,v)
        # Sag is geometry, not a multiplier on a cosmetic oscillation. Its
        # gravity-loaded equilibrium is the origin of the perturbation solver.
        if surface=='back':
            envelope=math.sin(math.pi*u)*math.sin(math.pi*v)
            y-=c.net_slack*.5*envelope
            z=max(0,z-c.net_slack*.45*math.sqrt(c.net_gravity/9.81)*envelope)
        else:
            envelope=math.sin(math.pi*u)*math.sin(math.pi*v)
            x+=(-1 if surface=='left' else 1)*c.net_slack*.55*envelope
            z=max(0,z-c.net_slack*.35*math.sqrt(c.net_gravity/9.81)*envelope)
        return (x,y,z)

    def _grid(self,surface,us,vs):
        g=self.geometry;grid=[]
        for j,v in enumerate(vs):
            row=[]
            for i,u in enumerate(us):
                p=g.point(surface,u,v);key=tuple(round(n,7) for n in p)
                pinned=(surface=='back' and j in (0,len(vs)-1)) or (surface!='back' and (i==0 or j==0))
                if surface=='back' and abs(v-g.hinge)<1e-8:
                    pinned|=i in (0,len(us)-1) or (g.structure=='box' and i==len(us)//2)
                if surface!='back':
                    anchor=(i==len(us)-1 if g.structure=='box' else abs(u-g.hinge)<1e-8)
                    if anchor and j==len(vs)-1:pinned=True
                if key not in self._lookup and (i in (0,len(us)-1) or j in (0,len(vs)-1)):
                    # Algebraically identical Windows seam coordinates may
                    # straddle a decimal rounding boundary. Weld by tolerance,
                    # never leave a separate particle a few nanometres away.
                    match=next((index for position,index in self._lookup.items() if math.dist(position,p)<1e-6),None)
                    if match is not None:self._lookup[key]=match
                if key in self._lookup:
                    index=self._lookup[key];self.pinned[index]|=pinned
                else:
                    index=len(self.rest);self._lookup[key]=index
                    # Shared seams keep their exact base geometry; interior sag
                    # joins continuously at the same welded particle.
                    self.rest.append(list(self._rest_point(surface,u,v)));self.pinned.append(pinned)
                row.append(index)
            grid.append(row)
        self.grids[surface]=(us,vs,grid)
        for j,row in enumerate(grid):
            for i,a in enumerate(row):
                for di,dj,strength in ((1,0,1.),(0,1,1.),(1,1,.25),(-1,1,.25)):
                    ni,nj=i+di,j+dj
                    if 0<=ni<len(us) and nj<len(vs):
                        b=grid[nj][ni];edge=tuple(sorted((a,b)))
                        if a==b or edge in self._edges:continue
                        self._edges.add(edge);length=math.dist(self.rest[a],self.rest[b]);self.links.append((a,b,length,strength))

    def reset(self):
        self.positions=[p[:] for p in self.rest];self.previous=[p[:] for p in self.rest]
        self.forces=[[0.,0.,0.] for _ in self.rest]
        self.active=False;self.accumulator=0.;self.time=0.;self.quiet=0.;self.contact=None;self.generation+=1

    def weights(self,surface,u,v):
        us,vs,grid=self.grids[surface]
        i=max(0,min(len(us)-2,bisect_right(us,u)-1));j=max(0,min(len(vs)-2,bisect_right(vs,v)-1))
        a=max(0,min(1,(u-us[i])/(us[i+1]-us[i])));b=max(0,min(1,(v-vs[j])/(vs[j+1]-vs[j])))
        return ((grid[j][i],(1-a)*(1-b)),(grid[j][i+1],a*(1-b)),(grid[j+1][i],(1-a)*b),(grid[j+1][i+1],a*b))

    def sample_weights(self,weights):
        p=self.positions
        return tuple(sum(p[i][axis]*w for i,w in weights) for axis in range(3))

    def sample(self,surface,u,v):return self.sample_weights(self.weights(surface,u,v))

    def impact(self,surface,position,velocity,radius=.115):
        if surface not in self.grids:raise ValueError('Invalid net surface')
        if not all(math.isfinite(x) for x in (*position,*velocity)) or not .02<=radius<=.3:raise ValueError('Invalid impact')
        if self.contact and self.time-self.contact['time']<.20 and math.dist(position,self.contact['point'])<.6:return False
        u,v=self.geometry.uv_at(surface,position);normal=self.geometry.normal(surface,u,v)
        speed=math.sqrt(sum(x*x for x in velocity));normal_speed=sum(a*b for a,b in zip(normal,velocity))
        if speed<.01 or normal_speed<=0:return False
        direction=tuple(.85*normal[i]+.15*velocity[i]/speed for i in range(3))
        contact_point=self.geometry.point(surface,u,v)
        reach=.43+.09*min(1,speed/32)
        for i,p in enumerate(self.rest):
            if self.pinned[i]:continue
            distance=math.dist(p,contact_point)
            if distance>reach*3:continue
            influence=math.exp(-(distance/reach)**2*1.3)
            impulse=min(45,normal_speed)*self.config.net_impact_scale*influence
            for axis in range(3):self.previous[i][axis]-=direction[axis]*impulse*self.STEP
        self.contact={'surface':surface,'u':u,'v':v,'normal':normal,'point':tuple(position),'time':self.time,'radius':radius,'speed':speed}
        self.active=True;self.quiet=0.;self.generation+=1
        return True

    def advance(self,dt):
        if not math.isfinite(dt) or dt<0:raise ValueError('Invalid time delta')
        if not self.active:return 0
        self.accumulator+=min(dt,.15);steps=0
        while self.accumulator+1e-12>=self.STEP and steps<18 and self.active:
            self._step();self.accumulator-=self.STEP;steps+=1
        return steps

    def _step(self):
        c=self.config;p=self.positions;previous=self.previous;forces=self.forces;dt=self.STEP
        for i,point in enumerate(p):
            for axis in range(3):forces[i][axis]=-c.net_stiffness*(point[axis]-self.rest[i][axis])
        for a,b,length,strength in self.links:
            pa,pb=p[a],p[b];dx,dy,dz=pb[0]-pa[0],pb[1]-pa[1],pb[2]-pa[2]
            distance=math.sqrt(dx*dx+dy*dy+dz*dz)
            # The measured rest length includes sag; a small material reserve
            # goes slack before structural tension rises. Shear is softer.
            extension=max(0,distance-length*(1+c.net_slack*.12))
            spring=c.net_wave_propagation*strength*extension/max(.0001,distance)
            for axis,delta in enumerate((dx,dy,dz)):
                force=spring*delta;forces[a][axis]+=force;forces[b][axis]-=force
        damping=math.exp(-c.net_damping*dt);max_move=0.;max_speed=0.
        cap=(c.net_max_stretch-1)*1.8
        for i,point in enumerate(p):
            if self.pinned[i]:continue
            for axis in range(3):
                old=point[axis];point[axis]=old+(old-previous[i][axis])*damping+forces[i][axis]*dt*dt;previous[i][axis]=old
            point[2]=max(0.,point[2]);offset=math.dist(point,self.rest[i])
            if offset>cap:
                scale=cap/offset
                for axis in range(3):point[axis]=self.rest[i][axis]+(point[axis]-self.rest[i][axis])*scale
        # Stretch constraints bound impulsive near-post extension, including at
        # anchored nodes. Deterministic order/iterations independent of draw FPS.
        for _ in range(2):
            for a,b,length,_strength in self.links:
                pa,pb=p[a],p[b];dx,dy,dz=pb[0]-pa[0],pb[1]-pa[1],pb[2]-pa[2]
                distance2=dx*dx+dy*dy+dz*dz;limit=length*c.net_max_stretch
                if distance2<=limit*limit or self.pinned[a] and self.pinned[b]:continue
                distance=math.sqrt(distance2);factor=(distance-limit)/distance
                wa=0 if self.pinned[a] else 1;wb=0 if self.pinned[b] else 1;factor/=wa+wb
                for axis,delta in enumerate((dx,dy,dz)):
                    pa[axis]+=delta*factor*wa;pb[axis]-=delta*factor*wb
        for i,point in enumerate(p):
            if self.pinned[i]:continue
            max_move=max(max_move,math.dist(point,self.rest[i]));max_speed=max(max_speed,math.dist(point,previous[i])/dt)
        self.time+=dt;self.generation+=1
        if max_move<c.net_settle_threshold and max_speed<c.net_settle_threshold*6:self.quiet+=dt
        else:self.quiet=0.
        if self.quiet>.35:
            for i in range(len(p)):p[i][:]=self.rest[i];previous[i][:]=self.rest[i]
            self.active=False;self.contact=None;self.generation+=1

    def pocket_ball(self):
        """A short scored-ball presentation contact; never a second score model."""
        hit=self.contact
        if not hit:return None
        age=self.time-hit['time']
        if age>.72:return None
        point=self.sample(hit['surface'],hit['u'],hit['v'])
        # Ball sits inside the same sheet; the net touches its outer hemisphere.
        return tuple(point[i]-hit['normal'][i]*(hit['radius']+.012) for i in range(3))

    def visual_position(self,actual):
        target=self.pocket_ball();point=tuple(actual)
        if target is not None:
            age=self.time-self.contact['time']
            weight=min(1.,age/.035,max(0.,(.72-age)/.20))
            weight=weight*weight*(3-2*weight)
            point=tuple(actual[i]+(target[i]-actual[i])*weight for i in range(3))
        # Retain a scored ball on the inner side even during secondary inward
        # oscillations. This affects drawing only, not the original Ball object.
        if self.contact and point[1]<0:
            radius=self.contact['radius']+.008
            for surface in ('left','right','back'):
                u,v=self.geometry.uv_at(surface,point);sheet=self.sample(surface,u,v);normal=self.geometry.normal(surface,u,v)
                gap=sum((point[i]-sheet[i])*normal[i] for i in range(3))
                if gap>-radius:point=tuple(point[i]-normal[i]*(gap+radius) for i in range(3))
        return point

    @property
    def displacement(self):return max((math.dist(a,b) for a,b in zip(self.positions,self.rest)),default=0.)
