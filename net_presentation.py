"""Draped-net presentation after a legal goal; authoritative ball is read-only."""
from net_cloth import NetGeometry
from net_drape import MATERIALS,ReferenceCloth,RollingReplay


def ensure(game):
    variant='rounded' if game.goal_net_style.structure=='rounded' else 'reference'
    config=getattr(game,'_net_config',MATERIALS[variant].config)
    from goal_nets import geometry_for
    geometry=geometry_for(game)
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
    if getattr(game,'_net_replay',None) is not None:return False
    replay=RollingReplay('rounded' if cloth.geometry.structure=='rounded' else 'reference',height=max(game.ball.radius,position[2]),
                         geometry=cloth.geometry,coarse=not game.desktop_windows,cloth=cloth)
    replay.radius=game.ball.radius
    replay.position=list(position);replay.velocity=list(velocity);replay.ball=tuple(position)
    replay.hit=True
    game._net_replay=replay
    cloth.active=True;cloth.quiet=0.
    return True


def start(game,entry=None,remaining=0.):
    """Continuous post-goal flight starts before any authoritative net correction."""
    cloth=ensure(game)
    replay=RollingReplay('rounded' if cloth.geometry.structure=='rounded' else 'reference',height=game.ball.z,geometry=cloth.geometry,coarse=not game.desktop_windows,cloth=cloth)
    replay.radius=game.ball.radius
    replay.position=list(entry) if entry is not None else [game.ball.x,game.ball.y,game.ball.z]
    replay.velocity=[game.ball.vx,game.ball.vy,game.ball.vz];replay.ball=tuple(replay.position)
    if remaining>0:replay.advance(remaining)
    game._net_replay=replay;game._net_replay_just_started=True


def advance(game,dt):
    cloth=getattr(game,'_net_cloth',None)
    replay=getattr(game,'_net_replay',None)
    if replay is not None:
        if getattr(replay,'collected',False):
            cloth.retain_pocket=False;cloth.advance(dt);return
        if getattr(game,'_net_replay_just_started',False):game._net_replay_just_started=False;return
        replay.advance(dt)
    elif cloth is not None:cloth.advance(dt)


def reset(game):
    cloth=getattr(game,'_net_cloth',None)
    if cloth is not None:cloth.reset()
    game._net_replay=None;game._net_replay_just_started=False


def ball_position(game):
    replay=getattr(game,'_net_replay',None)
    if replay is not None and game.result_text=='GOAL!':return replay.ball
    return (game.ball.x,game.ball.y,game.ball.z)
