"""Shared real-time clock; shot speed is controlled at ball launch."""
GAME_SPEED=1.0

def simulation_dt(seconds,view):
    return max(0.,min(seconds,.12))
