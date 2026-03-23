def update_ball_position(x, y, vx, vy, dt):
    new_x = x + vx * dt
    new_y = y + vy * dt
    return new_x, new_y