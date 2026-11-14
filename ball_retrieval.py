"""A player follows the stopped presentation ball before picking it up."""
from dataclasses import dataclass
import math

@dataclass
class Retrieval:
    position:tuple
    target:tuple
    phase:str='approach'
    age:float=0.
    settled:float=0.
    secured:bool=False
    done:bool=False
    moving:bool=False
    previous_ball:object=None

    def advance(self,dt,ball,speed,radius=.115):
        self.moving=False
        if self.done:return
        self.age+=dt
        if self.phase=='return':
            self.target=(0.,52.5);self._move(dt)
            if self.age>=3.4:self.done=True
            return
        if self.previous_ball is not None and dt>0:speed=max(speed,math.dist(ball,self.previous_ball)/dt)
        self.previous_ball=tuple(ball);self.target=tuple(ball[:2])
        stationary=speed<.15 and ball[2]<=radius+.08
        self.settled=self.settled+dt if stationary else 0.
        if self.phase=='pickup':
            if not stationary or math.dist(self.position,self.target)>.3:
                self.phase='approach';self.age=0.;return
            if self.age>=.6:self.secured=True;self.phase='return';self.age=0.
            return
        self._move(dt)
        if math.dist(self.position,self.target)<.18 and self.settled>=.2:
            self.position=self.target;self.phase='pickup';self.age=0.

    def _move(self,dt):
        distance=math.dist(self.position,self.target);travel=min(distance,7.*max(0.,dt))
        if travel>1e-7:
            self.position=tuple(a+(b-a)*travel/distance for a,b in zip(self.position,self.target));self.moving=True

    def actor(self):
        return self.position,('BALL_RUN' if self.secured else 'TACKLE' if self.phase=='pickup' else 'RUN' if self.moving else 'IDLE'),self.age
