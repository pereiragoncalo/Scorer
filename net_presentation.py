"""Draped-net presentation after a legal goal; authoritative ball is read-only."""
from net_cloth import NetGeometry
from net_drape import MATERIALS,ReferenceCloth,RollingReplay


def ensure(game):
    config=getattr(game,'_net_config',MATERIALS['reference'].config)
    geometry=NetGeometry(game.goal_net_style.structure,game.goal_width,game.goal_height)
    coarse=not game.desktop_windows
    key=(geometry,config,coarse)
    if getattr(game,'_net_cloth_key',None)!=key:
        game._net_cloth=ReferenceCloth(geometry,config,coarse)
        game._net_cloth_key=key;game._net_renderer=None;game._net_replay=None
    return game._net_cloth


def impact(game,surface,position,velocity):
    if game.result_text!='GOAL!':return False
    cloth=ensure(game)
    # Original post-goal collisions can report several impacts. One independent
    # presentation trajectory owns the cloth until reset, never restart it from
    # the separately bouncing authoritative ball.
    if getattr(game,'_net_replay',None) is not None and (cloth.active or cloth.time>0):return False
    replay=RollingReplay('reference',height=max(game.ball.radius,position[2]),
                         geometry=cloth.geometry,coarse=not game.desktop_windows)
    replay.cloth=cloth;replay.radius=game.ball.radius
    replay.position=list(position);replay.velocity=list(velocity);replay.ball=tuple(position)
    replay.hit=True
    game._net_replay=replay
    cloth.active=True;cloth.quiet=0.
    return True


def advance(game,dt):
    cloth=getattr(game,'_net_cloth',None)
    replay=getattr(game,'_net_replay',None)
    if replay is not None:
        # A settled display ball must not keep waking the cloth on microscopic
        # ground/net overlaps. Let the unloaded fabric recover and sleep.
        resting=(replay.stop_time is not None
                 and replay.ball[2]<=replay.radius+.0001
                 and sum(v*v for v in replay.velocity)<.05**2)
        if resting:
            replay.position[2]=replay.radius;replay.ball=tuple(replay.position)
            cloth.advance(dt)
        elif cloth.active or replay.stop_time is None:replay.advance(dt)
    elif cloth is not None:cloth.advance(dt)


def reset(game):
    cloth=getattr(game,'_net_cloth',None)
    if cloth is not None:cloth.reset()
    game._net_replay=None


def ball_position(game):
    replay=getattr(game,'_net_replay',None)
    if replay is not None and game.result_text=='GOAL!':return replay.ball
    return (game.ball.x,game.ball.y,game.ball.z)
