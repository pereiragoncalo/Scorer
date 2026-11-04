"""Competitive keeper/marking ability. No scoring quotas or altered ball physics."""
from dataclasses import dataclass
from functools import lru_cache

@dataclass(frozen=True)
class DefensiveProfile:
    level:float
    reaction_low:float
    reaction_high:float
    reading_error:float
    step_speed:float
    acceleration:float
    commitment_time:float
    dive_speed:float
    jump_boost:float
    lane_jitter:float
    defenders:int

@lru_cache(maxsize=16)
def defensive_profile(tier=4,international=False):
    tier=1 if international else max(1,min(5,int(tier)))
    level=(5-tier)/4
    return DefensiveProfile(level,.17-.05*level,.32-.07*level,.24-.12*level,
        2.5+1.0*level,11+5*level,.28+.05*level,4.0+.9*level,
        .36+.16*level,.50-.28*level,5 if tier<=2 else 4)
