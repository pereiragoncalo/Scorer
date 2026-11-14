"""One gameplay clock: faster playback without changing shot physics ratios."""
GAME_SPEED=1.05

def simulation_dt(seconds,view):
    elapsed=max(0.,min(seconds,.12))
    return elapsed*(GAME_SPEED if view in ('shot','match') else 1.)
