"""Deterministic development shots. No career, settings or score writes."""
from dataclasses import asdict
import json,math
from pathlib import Path
from net_cloth import NetCloth,NetGeometry,NetConfig

PRESETS={
 'Near Post Strong':('left',.24,.48,34.,-18.,0.),
 'Near Post Medium':('left',.24,.48,23.,-18.,0.),
 'Near Post Weak':('left',.24,.48,10.,-18.,0.),
 'Far Post Strong':('right',.24,.48,34.,18.,0.),
 'Center Strong':('back',.5,.65,34.,0.,0.),
 'Top Corner':('back',.08,.22,29.,-12.,12.),
 'Low Shot':('back',.40,.94,27.,0.,-6.),
}

class Replay:
    def __init__(self,structure='box',config=NetConfig(),preset='Near Post Strong',coarse=True):
        self.geometry=NetGeometry(structure);self.coarse=coarse;self.cloth=NetCloth(self.geometry,config,coarse)
        self.preset=preset;self.surface,self.u,self.v,self.force,self.yaw,self.pitch=PRESETS[preset]
        if self.surface=='back':
            target=self.geometry.height*.5 if preset=='Center Strong' else self.geometry.height-.16 if preset=='Top Corner' else .22
            lo,hi=0.,1.
            for _ in range(30):
                mid=(lo+hi)/2
                if self.geometry.profile(mid)[1]>target:lo=mid
                else:hi=mid
            self.v=(lo+hi)/2
        self.playback=1.;self.paused=False;self.reset()

    def reset(self):
        self.cloth.reset();self.tick=0;self.accumulator=0.;self.hit=False;self.peak=0.;self.peak_time=0.
        self.contact=self.geometry.point(self.surface,self.u,self.v)
        n=self.geometry.normal(self.surface,self.u,self.v);yaw=math.radians(self.yaw);pitch=math.radians(self.pitch)
        # Rotation within the tangent plane gives distinct direction/angle while
        # preserving an outward approach to the chosen sheet.
        tangent=(0.,1.,0.) if self.surface=='left' else (0.,-1.,0.) if self.surface=='right' else (1.,0.,0.)
        incoming=n if self.surface!='back' else (0.,-1.,0.)
        self.velocity=tuple(self.force*(incoming[i]*math.cos(yaw)*math.cos(pitch)+tangent[i]*math.sin(yaw)*math.cos(pitch)+(1 if i==2 else 0)*math.sin(pitch)) for i in range(3))
        self.normal=n
        self.flight=min(.30,max(.015,(self.contact[2]-n[2]*.127-.115)/self.velocity[2])) if self.velocity[2]>0 else .30
        self.ball=tuple(self.contact[i]-n[i]*.127-self.velocity[i]*self.flight for i in range(3))

    def one_step(self):
        self.tick+=1;t=self.tick*self.cloth.STEP
        if self.tick>=36 and not self.hit:
            self.cloth.impact(self.surface,self.contact,self.velocity);self.hit=True
        self.cloth.advance(self.cloth.STEP)
        if not self.hit:self.ball=tuple(self.contact[i]-self.normal[i]*.127-self.velocity[i]*min(self.flight,.30-t) for i in range(3))
        else:
            age=t-.30
            actual=(self.contact[0]-self.normal[0]*.127,self.contact[1]-self.normal[1]*.127+.08*age,max(.115,self.contact[2]-.127*self.normal[2]-.5*9.81*age*age))
            self.ball=self.cloth.visual_position(actual)
        displacement=self.cloth.displacement
        if displacement>self.peak:self.peak=displacement;self.peak_time=t

    def advance(self,dt):
        if self.paused:return
        self.accumulator+=max(0,min(.15,dt))*self.playback
        while self.accumulator+1e-12>=self.cloth.STEP:
            self.one_step();self.accumulator-=self.cloth.STEP

    def configuration(self):
        return {'schema':1,'resolution':'mobile' if self.coarse else 'full','structure':self.geometry.structure,'preset':self.preset,'parameters':asdict(self.cloth.config),'shot':{'surface':self.surface,'u':self.u,'v':self.v,'force':self.force,'yaw':self.yaw,'pitch':self.pitch}}

    def save(self,path):Path(path).write_text(json.dumps(self.configuration(),indent=2)+'\n')

    @classmethod
    def load(cls,path):
        path=Path(path)
        if path.stat().st_size>16384:raise ValueError('Configuration exceeds16KiB')
        data=json.loads(path.read_text())
        if set(data)!={'schema','resolution','structure','preset','parameters','shot'} or data['schema']!=1:raise ValueError('Invalid net configuration')
        if data['resolution'] not in ('mobile','full'):raise ValueError('Invalid resolution')
        replay=cls(data['structure'],NetConfig(**data['parameters']),data['preset'],data['resolution']=='mobile')
        shot=data['shot']
        if set(shot)!={'surface','u','v','force','yaw','pitch'} or shot['surface'] not in ('back','left','right'):raise ValueError('Invalid shot')
        limits={'u':(0,1),'v':(0,1),'force':(3,50),'yaw':(-65,65),'pitch':(-45,45)}
        for key,(lo,hi) in limits.items():
            if type(shot[key]) not in (int,float) or not math.isfinite(shot[key]) or not lo<=shot[key]<=hi:raise ValueError('Invalid shot '+key)
        for key,value in shot.items():setattr(replay,key,value)
        replay.reset();return replay
