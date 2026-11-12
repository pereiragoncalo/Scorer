"""Chance-specific control/keeper tuning; never changes targets or save geometry."""
from dataclasses import dataclass
@dataclass(frozen=True)
class FinishingBalance:
    aim_speed:float=1.
    decision_time:float=1.
    reaction_delay:float=0.
    reading_error:float=1.
NEUTRAL=FinishingBalance()
PENALTY=FinishingBalance(.50,2.6,.24,2.9)
ONE_ON_ONE=FinishingBalance(.65,2.0,.18,2.2)
OPEN_PLAY=FinishingBalance(.75,1.6,.09,1.45)
HEADER=FinishingBalance(.78,1.6,.08,1.4)
def finishing_balance(shot_type,one_on_one,distance):
    if shot_type=='penalty':return PENALTY
    if shot_type=='header':
        close=max(0.,min(1.,(10.-distance)/3.))
        if not close:return HEADER
        return FinishingBalance(HEADER.aim_speed*(1.-.05*close),HEADER.decision_time*(1.+.12*close),HEADER.reaction_delay+.015*close,HEADER.reading_error*(1.+.08*close))
    if one_on_one:return ONE_ON_ONE
    return OPEN_PLAY if shot_type in ('kick','free_kick') else NEUTRAL

PENALTY_PROBABILITY=.08

def placed_keeper_balance(shot_type,target_x,goal_half_width):
    """Slightly later, less precise reads of clean shots towards either corner."""
    if shot_type not in ('kick','free_kick') or goal_half_width<=0 or abs(target_x)>goal_half_width-.12:
        return 0.,1.,0.
    strength=max(0.,min(1.,(abs(target_x)/goal_half_width-.45)/.40))
    bias=(-1. if target_x>0 else 1.)*.16*strength
    return .06*strength,1.+.35*strength,bias
