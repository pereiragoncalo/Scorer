"""Small Scorer adapter: the cloth never writes game state or ball physics."""
from net_cloth import NetCloth,NetConfig,NetGeometry


def ensure(game):
    config=getattr(game,'_net_config',NetConfig())
    geometry=NetGeometry(game.goal_net_style.structure,game.goal_width,game.goal_height)
    coarse=not game.desktop_windows
    key=(geometry,config,coarse)
    if getattr(game,'_net_cloth_key',None)!=key:
        game._net_cloth=NetCloth(geometry,config,coarse);game._net_cloth_key=key
        game._net_renderer=None
    return game._net_cloth


def impact(game,surface,position,velocity):
    # Impacts arrive only from the original post-goal net collision path.
    if game.result_text!='GOAL!':return False
    return ensure(game).impact(surface,position,velocity,game.ball.radius)


def advance(game,dt):
    cloth=getattr(game,'_net_cloth',None)
    if cloth is not None:cloth.advance(dt)


def reset(game):
    cloth=getattr(game,'_net_cloth',None)
    if cloth is not None:cloth.reset()


def ball_position(game):
    actual=(game.ball.x,game.ball.y,game.ball.z)
    cloth=getattr(game,'_net_cloth',None)
    if cloth is None or game.result_text!='GOAL!':return actual
    return cloth.visual_position(actual)
