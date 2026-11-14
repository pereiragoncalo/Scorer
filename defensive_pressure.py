"""One nearest opponent closes the player; the remaining block keeps its shape."""
from dataclasses import dataclass
import math
from career import PLAYER_SCALE


def player_position(game):
    facing=0. if game.current_opportunity is not None and game.state in (game.STATE_BUILDUP,game.STATE_AIMING) else game.aim_x
    dx,dy=facing-game.shot_origin_x,-game.shot_origin_y
    length=max(.001,math.hypot(dx,dy));distance=(.18 if game.shot_type=='header' else .52)*PLAYER_SCALE
    return (game.shot_origin_x-dx/length*distance,
            game.shot_origin_y-dy/length*distance+(2.*(1.-game.buildup_progress) if game.state==game.STATE_BUILDUP else 0.))

@dataclass
class Pressure:
    actor:object
    position:tuple
    moving:bool=False
    origin:object=None

    def __post_init__(self):
        if self.origin is None:self.origin=tuple(self.position)


def assign(game):
    game._pressure=None
    if game.current_opportunity is None or game.current_opportunity.kind=='penalty':return
    opponents=[p for p in game.field_players if p.team=='defender']
    if not opponents:return
    target=player_position(game)
    actor=min(opponents,key=lambda p:math.dist(game._field_player_position(p),target))
    game._pressure=Pressure(actor,game._field_player_position(actor))


def advance(game,dt):
    pressure=getattr(game,'_pressure',None)
    if pressure is None:return
    pressure.moving=False
    if game.outcome_registered or game.state not in (game.STATE_BUILDUP,game.STATE_AIMING,game.STATE_SHOT):return
    if game.current_opportunity.kind=='free_kick' and game.state!=game.STATE_SHOT:return
    target=player_position(game);origin=pressure.origin
    distance_from_line=math.dist(origin,target)
    step=min(.9,max(0.,distance_from_line-3.))
    target=tuple(a+(b-a)*step/max(1e-9,distance_from_line) for a,b in zip(origin,target))
    distance=math.dist(pressure.position,target)
    travel=min(distance,max(0.,dt)*1.8)
    if travel<=1e-7:return
    pressure.position=tuple(a+(b-a)*travel/distance for a,b in zip(pressure.position,target));pressure.moving=True
