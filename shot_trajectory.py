"""Launch solver matching the game's fixed-step gravity/drag integrator."""
import math
from career import GRAVITY, PHYSICS_STEP


def launch_velocity(start, target, duration):
    steps=max(1,round(duration/PHYSICS_STEP))
    drag=math.pow(.996,PHYSICS_STEP*60)
    factor=0.;unit=1.;fall=0.;vertical=0.
    for _ in range(steps):
        factor+=unit*PHYSICS_STEP;unit*=drag
        vertical-=GRAVITY*PHYSICS_STEP
        fall+=vertical*PHYSICS_STEP;vertical*=drag
    return ((target[0]-start[0])/factor, -start[1]/factor,
            (target[1]-start[2]-fall)/factor)
