def should_goalkeeper_dive(ball_y, trigger_y):
    return ball_y <= trigger_y


def dive_direction(ball_x, keeper_center_x):
    if ball_x < keeper_center_x:
        return "left"
    if ball_x > keeper_center_x:
        return "right"
    return "center"