"""Development-only rolling sphere / net contact experiment. Not imported by game."""
from dataclasses import dataclass
import math
from net_cloth import NetCloth,NetConfig,NetGeometry

@dataclass(frozen=True)
class Material:
    label:str
    config:NetConfig
    friction:float
    restitution:float
    node_mass:float=.055

MATERIALS={
 'tight':Material('REDE ESTICADA',NetConfig(net_slack=.015,net_stiffness=78,net_damping=2.,net_max_stretch=1.16,net_wave_propagation=115),.08,.25,.35),
 'slack':Material('REDE SOLTA',NetConfig(net_slack=.38,net_stiffness=10,net_damping=11.5,net_max_stretch=2.0,net_wave_propagation=18),.75,.025),
}

class RollingReplay:
    STEP=1/120
    def __init__(self,variant='slack',speed=6.8):
        self.material=MATERIALS[variant];self.geometry=NetGeometry('box')
        self.cloth=NetCloth(self.geometry,self.material.config,coarse=False)
        # Every point touching the turf is an anchor, for both materials.
        # Slack belongs to the suspended mesh, never a sliding ground hem.
        self.ground_anchors=tuple(i for i,p in enumerate(self.cloth.rest) if abs(p[2])<1e-6)
        for i in self.ground_anchors:self.cloth.pinned[i]=True
        self.tick=0;self.accumulator=0.;self.hit=False;self.preset=self.material.label;self.peak=0.;self.peak_time=0.;self.peak_ball=None;self.first_contacts={}
        self.radius=.115;self.mass=.43
        # A glancing ground shot, already through the mouth. It reaches the
        # side first and keeps its longitudinal momentum towards the rear seam.
        self.position=[-self.geometry.width/2+.27,.65,self.radius]
        self.velocity=[-.75,-speed,0.];self.ball=tuple(self.position)
        self.roll=0.;self.distance=0.;self.contacts=[];self.history=[];self.stop_time=None

    def _contact(self,surface):
        g=self.geometry;c=self.cloth;b=self.position
        if b[1]>.02:return None
        u,v=g.uv_at(surface,b);weights=c.weights(surface,u,v)
        point=c.sample_weights(weights);normal=g.normal(surface,u,v)
        # Don't let a sheet beyond its parameter boundary act as an infinite wall.
        if surface!='back' and not -g.depth-1.0<b[1]<0:return None
        gap=sum((b[i]-point[i])*normal[i] for i in range(3))+self.radius
        if gap<=0:return None
        free={}
        for index,weight in weights:
            if not c.pinned[index] and weight>0:free[index]=free.get(index,0)+weight
        inv_ball=1/self.mass;inv_node=1/self.material.node_mass
        denom=inv_ball+inv_node*sum(w*w for w in free.values())
        impulse=gap/denom
        for axis in range(3):b[axis]-=normal[axis]*impulse*inv_ball
        for index,weight in free.items():
            for axis in range(3):
                correction=normal[axis]*impulse*inv_node*weight
                c.positions[index][axis]+=correction;c.previous[index][axis]+=correction
        return (surface,normal,weights,gap,impulse/self.STEP)

    def one_step(self):
        dt=self.STEP;c=self.cloth;b=self.position;old=b[:];v=self.velocity
        horizontal=math.hypot(v[0],v[1])
        # Rolling resistance, not an exponential animation to a target point.
        resistance=.55
        if horizontal:
            scale=max(0.,1-resistance*dt/horizontal);v[0]*=scale;v[1]*=scale
        for axis in range(2):b[axis]+=v[axis]*dt
        b[2]=self.radius
        c.advance(dt)
        contacts=[]
        for _ in range(4):
            for surface in ('left','right','back'):
                item=self._contact(surface)
                if item is not None:contacts.append(item)
        corrected=v[:]
        handled=set()
        for surface,normal,weights,gap,_ in contacts:
            if surface in handled:continue
            handled.add(surface)
            free={}
            for index,weight in weights:
                if not c.pinned[index] and weight>0:free[index]=free.get(index,0)+weight
            denominator=1/self.mass+sum(w*w/self.material.node_mass for w in free.values())
            sheet_velocity=[sum((c.positions[idx][axis]-c.previous[idx][axis])*weight/dt for idx,weight in weights) for axis in range(3)]
            relative=[corrected[i]-sheet_velocity[i] for i in range(3)]
            closing=sum(relative[i]*normal[i] for i in range(3))
            if closing<=0:continue
            impulse=(1+self.material.restitution)*closing/denominator
            for axis in range(2):corrected[axis]-=normal[axis]*impulse/self.mass
            for index,weight in free.items():
                for axis in range(2):c.previous[index][axis]-=normal[axis]*impulse*weight/self.material.node_mass*dt
            tangent=[relative[i]-normal[i]*closing for i in range(3)]
            length=math.sqrt(sum(x*x for x in tangent))
            if length:
                friction=min(length/denominator,self.material.friction*impulse)
                for axis in range(2):corrected[axis]-=tangent[axis]/length*friction/self.mass
                for index,weight in free.items():
                    for axis in range(2):c.previous[index][axis]+=tangent[axis]/length*friction*weight/self.material.node_mass*dt
        self.velocity=[corrected[0],corrected[1],0.]
        if contacts:
            self.hit=True;c.active=True;c.quiet=0.
            item=next((x for x in contacts if x[0]=='left'),contacts[-1])
            surface,normal,weights,gap,_=item;u,w=self.geometry.uv_at(surface,b)
            c.contact={'surface':surface,'u':u,'v':w,'normal':normal,'point':tuple(b),'time':c.time,'radius':self.radius,'speed':horizontal}
            c.generation+=1
        self.tick+=1;self.ball=tuple(b);self.contacts=sorted(set(x[0] for x in contacts))
        travel=math.dist(old,b);self.distance+=travel;self.roll+=-(b[1]-old[1])/self.radius
        displacement=c.displacement
        if displacement>self.peak:self.peak=displacement;self.peak_time=self.tick*dt;self.peak_ball=self.ball
        for surface in self.contacts:self.first_contacts.setdefault(surface,self.tick*dt)
        if math.hypot(*self.velocity[:2])<.03 and self.stop_time is None and self.tick*dt>1:self.stop_time=self.tick*dt
        if self.tick%12==0:self.history.append({'t':self.tick*dt,'position':self.ball,'speed':math.hypot(*self.velocity[:2]),'contacts':self.contacts,'deformation':displacement})

    def advance(self,dt):
        self.accumulator+=dt
        while self.accumulator+1e-12>=self.STEP:
            self.one_step();self.accumulator-=self.STEP
