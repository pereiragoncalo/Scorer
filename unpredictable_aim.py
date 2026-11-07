"""Continuous bounded stochastic aim. No periodic return or known safe dwell."""
import random,math
class Aim:
 def __init__(self,seed,x=0,z=1.2):
  self.rng=random.Random(seed);self.x=x;self.z=z;self.vx=self.rng.choice((-1,1))*3.;self.vz=self.rng.uniform(-2,2);self.next=0
 def advance(self,dt,speed,half,height,margin):
  left=max(0.,min(dt,.25));speed=max(.6,speed)
  while left>0:
   step=min(left,1/120);left-=step;self.next-=step
   if self.next<=0:
    self.next=self.rng.uniform(.08,.31)
    self.vx=.35*self.vx+self.rng.uniform(-4.8,4.8)*speed
    if abs(self.vx)<speed:self.vx=self.rng.choice((-1,1))*speed
    self.vz=.3*self.vz+self.rng.uniform(-2.,2.)*speed
   self.x+=self.vx*step;self.z+=self.vz*step
   if self.x>half+.35:self.x=half+.35;self.vx=-abs(self.vx)
   if self.x<-half-.35:self.x=-half-.35;self.vx=abs(self.vx)
   if self.z>height-margin:self.z=height-margin;self.vz=-abs(self.vz)
   if self.z<margin:self.z=margin;self.vz=abs(self.vz)
  return self.x,self.z
