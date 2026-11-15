"""Short heading wind-up and a grounded-to-airborne presentation arc."""
WINDUP_SECONDS=.22

def reset(game):game._header_pending=None

def queue(game,x,z):
    if getattr(game,'_header_pending',None)is not None:return
    if x is not None and z is not None:
        from career import clamp
        game.aim_x=clamp(x,-game.goal_half_width+.16,game.goal_half_width-.16);game.aim_z=clamp(z,.18,game.goal_height-.10);game.auto_aim=False
    game._header_pending=dict(age=0.,x=x,z=z,aim=(game.aim_x,game.aim_z),auto=game.auto_aim)

def advance(game,seconds):
    pending=getattr(game,'_header_pending',None)
    if pending is None:return False
    if game.state!=game.STATE_AIMING:reset(game);return False
    pending['age']+=seconds
    if pending['age']+1e-9>=WINDUP_SECONDS:
        reset(game);game.aim_x,game.aim_z=pending['aim'];game.auto_aim=pending['auto']
        game._launch_shot(pending['x'],pending['z'])
    return True

def windup_frame(game):
    pending=getattr(game,'_header_pending',None)
    return min(2,int(pending['age']/WINDUP_SECONDS*3))if pending else 0

def root_target(game,renderer,pose,position,contact):
    """Use one contact-frame calibration; never pin every frame to the ball."""
    from retro_sprites import projected_scale,PLAYER_HEIGHT_METRES
    character=renderer.manifest['characters']['players'];clip=character['animations']['HEADER']
    scale=projected_scale(game,position,character,PLAYER_HEIGHT_METRES)
    ax,ay=character['anchor'];hx,hy=clip['joints'][pose.view][3]['forehead']
    dx=(hx+.5-ax)*scale*(-1 if pose.flipped else 1);dy=(ay-hy-.5)*scale
    apex=(contact[0]-dx,contact[1]-dy);ground=game.project(*position)
    pending=getattr(game,'_header_pending',None)
    if game.state==game.STATE_AIMING:
        fraction=max(0.,min(1.,(pending['age']/WINDUP_SECONDS-.33)/.67))if pending else 0.
    else:fraction=1.-max(0.,min(1.,game.player_kick_progress))
    fraction=fraction*fraction*(3.-2.*fraction)
    return tuple(a+(b-a)*fraction for a,b in zip(ground,apex))
