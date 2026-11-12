"""Deterministic opportunity plans and visual deliveries, separate from shot physics.

A delivery never scores or consumes a shot. The exact contact point is handed
back to the existing fixed-step shot solver only after the player receives it.
"""
from dataclasses import dataclass
import math
import random
from career import BALL_RADIUS, HEADER_BALL_HEIGHT

KINDS=('cross','long_cross','corner','cutback','first_time','rebound','free_kick','long_shot')
TEXT={
 'long_shot':('LONG SHOT','A pass outside the box. Shoot from distance.'),
 'cross':('CROSS','A high cross is coming. Meet it with a header.'),
 'long_cross':('DEEP CROSS','A cross from deep on the wing. Attack the ball with a header.'),
 'corner':('CORNER','A corner into the box. Lose your marker and head towards goal.'),
 'cutback':('CUTBACK','A teammate reaches the byline and pulls the ball back to you.'),
 'first_time':('FIRST-TIME SHOT','A quick diagonal pass. Finish first time before the defence closes.'),
 'rebound':('REBOUND','A blocked shot falls to you. React and find a gap.'),
 'free_kick':('FREE KICK','A direct free kick. Find a way around or over the wall.'),
 'through_ball':('THROUGH BALL','A through ball puts you one on one with the goalkeeper.'),
 'penalty':('PENALTY','You have been chosen to take the penalty.'),
}
TIMING={'cross':.95,'long_cross':1.0,'corner':1.0,'cutback':1.0,'first_time':.85,'rebound':.90,'free_kick':1.10,'through_ball':1.0,'penalty':1.0,'long_shot':1.0}

def plan_opportunities(count,clear_index,penalty_index,seed):
    rng=random.Random('scorer-opportunities-v1:'+str(seed))
    # Weighted variety without repeated ordinary situations in a three-shot match.
    weights={'cross':3,'long_cross':3,'corner':2,'free_kick':3,'long_shot':4}
    pool=sorted(KINDS,key=lambda kind:rng.random()**(1/weights.get(kind,1)),reverse=True)
    return tuple('penalty' if i==penalty_index else 'through_ball' if i==clear_index else pool[i%len(pool)] for i in range(max(0,count)))

@dataclass(frozen=True)
class Delivery:
    kind:str
    shot_type:str
    points:tuple
    duration:float
    arcs:tuple

    @property
    def contact(self):return self.points[-1]

    def position(self,progress):
        p=max(0.,min(1.,progress))
        if p>=1:return self.contact
        segment=min(len(self.points)-2,int(p*(len(self.points)-1)))
        t=p*(len(self.points)-1)-segment
        a,b=self.points[segment:segment+2]
        return tuple(a[i]+(b[i]-a[i])*t+(math.sin(math.pi*t)*self.arcs[segment] if i==2 else 0) for i in range(3))

    def chasing_defender(self,progress):
        """Goal is y=0: the last defender plays the receiver onside at release.

        The receiver runs from contact.y+2m towards contact; the beaten defender
        retreats behind him before reception, leaving only the keeper ahead.
        This is a real match actor after reception, never a blocker in the lane.
        """
        if self.kind!='through_ball':return None
        p=max(0.,min(1.,progress));x,y,_=self.contact
        side=1 if x>=0 else -1
        return (x+side*(2.4+.4*p),y-.75+3.75*p)

    def mirrored(self):
        return Delivery(self.kind,self.shot_type,tuple((-x,y,z) for x,y,z in self.points),self.duration,self.arcs)

def make_delivery(kind,seed):
    if kind not in TEXT:raise ValueError('Unknown opportunity')
    rng=random.Random('scorer-delivery-v1:'+str(seed));side=rng.choice((-1,1));radius=BALL_RADIUS
    if kind=='penalty':return Delivery(kind,'penalty',((0.,11.,radius),(0.,11.,radius)),0.,(0.,))
    x=side*rng.uniform(1.0,3.8)
    if kind=='cross':
        end=(x,rng.uniform(6.5,9.0),HEADER_BALL_HEIGHT)
        return Delivery(kind,'header',((side*8.5,5.,radius),end),2.25,(2.8,))
    if kind in ('long_cross','corner'):
        end=(x,rng.uniform(6.5,10.),HEADER_BALL_HEIGHT)
        start=(side*25.,rng.uniform(20.,26.),radius) if kind=='long_cross' else (side*33.7,.3,radius)
        return Delivery(kind,'header',(start,end),3.15 if kind=='long_cross' else 3.0,(4.2,))
    if kind=='cutback':
        end=(x,rng.uniform(12.,16.),radius)
        return Delivery(kind,'kick',((side*8.,7.,radius),(side*7.,2.8,radius),end),2.7,(0.,.08))
    if kind=='first_time':
        end=(x,rng.uniform(15.5,18.),radius)
        return Delivery(kind,'kick',((-side*7.,20.,radius),end),1.9,(.28,))
    if kind=='rebound':
        end=(x,rng.uniform(13.,16.),radius)
        return Delivery(kind,'kick',((-side*5.,17.,radius),(side*1.5,6.,.65),end),2.4,(.35,.65))
    if kind=='long_shot':
        end=(side*rng.uniform(2.,9.),rng.uniform(22.,29.),radius)
        return Delivery(kind,'kick',((side*15.,31.,radius),end),1.8,(.15,))
    if kind=='free_kick':
        end=(side*rng.uniform(1.,6.),rng.uniform(18.5,23.),radius)
        return Delivery(kind,'free_kick',(end,end),1.1,(0.,))
    end=(side*rng.uniform(.5,1.8),rng.uniform(8.,11.),radius)
    return Delivery(kind,'kick',((-side*5.,18.,radius),end),2.1,(.10,))
