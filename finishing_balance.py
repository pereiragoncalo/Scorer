"""Chance-specific control/keeper tuning; never changes targets or save geometry."""
from dataclasses import dataclass
@dataclass(frozen=True)
class FinishingBalance:
    aim_speed:float=1.
    decision_time:float=1.
    reaction_delay:float=0.
    reading_error:float=1.
NEUTRAL=FinishingBalance()
PENALTY=FinishingBalance(.60,2.2,.18,2.5)
ONE_ON_ONE=FinishingBalance(.80,1.5,.09,1.6)
def finishing_balance(shot_type,one_on_one,distance):
    if shot_type=='penalty':return PENALTY
    if shot_type=='header':
        close=max(0.,min(1.,(10.-distance)/3.))
        if not close:return NEUTRAL
        return FinishingBalance(1.-.05*close,1.+.12*close,.015*close,1.+.08*close)
    if one_on_one:return ONE_ON_ONE
    return NEUTRAL
