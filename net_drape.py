"""Post-goal presentation sphere and draped net; never writes authoritative game state."""
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
 'reference':Material('REDE DRAPEADA · REFERÊNCIA',NetConfig(net_slack=.45,net_stiffness=8,net_damping=6.5,net_max_stretch=1.65,net_wave_propagation=95),.85,.015,.035),
 'sagged':Material('REDE COM MAIS FOLGA',NetConfig(net_slack=.45,net_stiffness=8,net_damping=10.5,net_max_stretch=2.5,net_wave_propagation=8),.75,.025),
 'slack':Material('REDE SOLTA',NetConfig(net_slack=.38,net_stiffness=10,net_damping=11.5,net_max_stretch=2.0,net_wave_propagation=18),.75,.025),
}

class TetheredCloth(NetCloth):
    """Lab-only soft rear ties; turf and front goal frame remain hard pins."""
    TIE_YIELD=.12

    def _rest_point(self,surface,u,v):
        point=list(super()._rest_point(surface,u,v))
        # More hanging fabric between supports, with zero offset at boundaries.
        envelope=math.sin(math.pi*u)*math.sin(math.pi*v)
        point[2]=max(0.,point[2]-.16*envelope)
        if surface=='back':point[1]-=.16*envelope
        else:point[0]+=(-1 if surface=='left' else 1)*.16*envelope
        return tuple(point)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        g=self.geometry;self.tethers=[];self.tie_peak=0.
        support_depth=g.depth if g.structure=='box' else g.top_depth
        for x in (-g.width/2,0.,g.width/2):
            index=min(range(len(self.rest)),key=lambda i:math.dist(self.rest[i],(x,-support_depth,g.height)))
            self.pinned[index]=False
            endpoint=(x+(-.35 if x<0 else .35 if x>0 else 0),-support_depth-1,g.height+.6)
            self.tethers.append((index,endpoint,math.dist(self.rest[index],endpoint)))

    def constrain_tethers(self):
        for index,endpoint,length in self.tethers:
            point=self.positions[index];rest=self.rest[index]
            offset=math.dist(point,rest)
            if offset>self.TIE_YIELD:
                for axis in range(3):
                    correction=(rest[axis]+(point[axis]-rest[axis])*self.TIE_YIELD/offset)-point[axis]
                    point[axis]+=correction;self.previous[index][axis]+=correction
            self.tie_peak=max(self.tie_peak,math.dist(point,rest))

    def _step(self):
        super()._step()
        # Stiff elastic ties give slightly at the net end. Their pole ends are
        # immutable world coordinates, independent of the moving net particles.
        for index,endpoint,length in self.tethers:
            for axis in range(3):
                self.previous[index][axis]+=(self.positions[index][axis]-self.rest[index][axis])*140*self.STEP**2
        self.constrain_tethers()

class ReferenceCloth(TetheredCloth):
    """Broad load transfer through hanging fabric, including the welded seam."""
    def _rest_point(self,surface,u,v):
        g=self.geometry
        x,y,z=g.point(surface,u,v)
        # Unloaded fabric hangs DOWN between supports. The previous sum of
        # three outward offsets made a permanent ~61 cm impact-shaped bulge.
        # Use one world-space rest field so shared roof/side seams agree.
        support_depth=g.depth if g.structure=='box' else g.top_depth
        depth=max(0.,min(1.,-y/support_depth))
        across=(x+g.width/2)/g.width
        sag=(self.config.net_slack*.5*math.sin(math.pi*depth)
             +.20*math.sin(2*math.pi*across)**2*depth)
        return (x,y,max(0.,z-sag*z/g.height))

class RollingReplay:
    STEP=1/120
    def __init__(self,variant='slack',speed=6.8,height=None,geometry=None,coarse=False):
        self.airborne=height is not None
        self.material=MATERIALS[variant];self.geometry=geometry or NetGeometry('box')
        self.cloth=(ReferenceCloth if variant=='reference' else TetheredCloth if variant=='sagged' else NetCloth)(self.geometry,self.material.config,coarse=coarse)
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
        if self.airborne:
            flight=.9/speed
            self.position=[-3.,-self.geometry.depth+.9,height+4.905*flight*flight]
            self.velocity=[0.,-speed,0.];self.ball=tuple(self.position)
        self.roll=0.;self.distance=0.;self.contacts=[];self.history=[];self.stop_time=None

    @classmethod
    def strong_side_shot(cls):
        replay=cls('reference',18.,1.22)
        replay.position=[-3.35,.60,1.27]
        replay.velocity=[-6.,-18.,0.]
        replay.ball=tuple(replay.position)
        return replay

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
        # Position correction may separate an idle ball, but must not create
        # a new pocket without incoming ball motion. Only touched strands
        # receive the load; neighboring fabric follows through its springs.
        if sum(self.velocity[i]*normal[i] for i in range(3))<=.02:free={}
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
        if self.airborne:v[2]-=9.81*dt
        for axis in range(3 if self.airborne else 2):b[axis]+=v[axis]*dt
        if b[2]<=self.radius:
            b[2]=self.radius
            if self.airborne:v[2]=max(0.,-v[2]*.12)
        if not self.airborne:b[2]=self.radius
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
            sheet_velocity=[sum((c.positions[idx][axis]-c.previous[idx][axis])*weight/dt for idx,weight in (free.items() if isinstance(c,ReferenceCloth) else weights)) for axis in range(3)]
            relative=[corrected[i]-sheet_velocity[i] for i in range(3)]
            closing=sum(relative[i]*normal[i] for i in range(3))
            if closing<=0:continue
            impulse=(1+self.material.restitution)*closing/denominator
            for axis in range(3 if self.airborne else 2):corrected[axis]-=normal[axis]*impulse/self.mass
            for index,weight in free.items():
                for axis in range(3 if self.airborne else 2):c.previous[index][axis]-=normal[axis]*impulse*weight/self.material.node_mass*dt
            tangent=[relative[i]-normal[i]*closing for i in range(3)]
            length=math.sqrt(sum(x*x for x in tangent))
            if length:
                friction=min(length/denominator,self.material.friction*impulse)
                for axis in range(3 if self.airborne else 2):corrected[axis]-=tangent[axis]/length*friction/self.mass
                for index,weight in free.items():
                    for axis in range(3 if self.airborne else 2):c.previous[index][axis]+=tangent[axis]/length*friction*weight/self.material.node_mass*dt
        self.velocity=[corrected[0],corrected[1],corrected[2] if self.airborne else 0.]
        if contacts:
            self.hit=True;c.active=True;c.quiet=0.
            item=next((x for x in contacts if x[0]=='left'),contacts[-1])
            surface,normal,weights,gap,_=item;u,w=self.geometry.uv_at(surface,b)
            c.contact={'surface':surface,'u':u,'v':w,'normal':normal,'point':tuple(b),'time':c.time,'radius':self.radius,'speed':horizontal}
            c.generation+=1
        if isinstance(c,TetheredCloth):c.constrain_tethers()
        self.tick+=1;self.ball=tuple(b);self.contacts=sorted(set(x[0] for x in contacts))
        travel=math.dist(old,b);self.distance+=travel;self.roll+=-(b[1]-old[1])/self.radius
        displacement=c.displacement
        if displacement>self.peak:self.peak=displacement;self.peak_time=self.tick*dt;self.peak_ball=self.ball
        for surface in self.contacts:self.first_contacts.setdefault(surface,self.tick*dt)
        if b[2]<=self.radius+.0001 and math.sqrt(sum(v*v for v in self.velocity))<.03 and self.stop_time is None and self.tick*dt>1:self.stop_time=self.tick*dt
        if self.tick%12==0:self.history.append({'t':self.tick*dt,'position':self.ball,'speed':math.hypot(*self.velocity[:2]),'contacts':self.contacts,'deformation':displacement})

    def advance(self,dt):
        self.accumulator+=dt
        while self.accumulator+1e-12>=self.STEP:
            self.one_step();self.accumulator-=self.STEP
