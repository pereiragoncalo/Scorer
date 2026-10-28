"""Per-game goal dimensions. Android keeps the original physical profile."""
from dataclasses import dataclass,field
from math import hypot
from career import GOAL_WIDTH,GOAL_HEIGHT,VEIL_TOUCH_DEPTH,VEIL_TOP_DEPTH,VEIL_GROUND_SLACK

@dataclass(frozen=True)
class GoalGeometry:
    width: float=GOAL_WIDTH
    height: float=GOAL_HEIGHT
    veil_slope_length: float=field(init=False)
    veil_path_length: float=field(init=False)

    def __post_init__(self):
        slope=hypot(VEIL_TOUCH_DEPTH-VEIL_TOP_DEPTH,self.height)
        object.__setattr__(self,'veil_slope_length',slope)
        object.__setattr__(self,'veil_path_length',VEIL_TOP_DEPTH+slope+VEIL_GROUND_SLACK)

    @classmethod
    def for_profile(cls,windows=False):
        return cls(GOAL_WIDTH*1.12,GOAL_HEIGHT*1.10) if windows else cls()
