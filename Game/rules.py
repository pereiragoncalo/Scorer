def shot_is_outside_small_box(x, y, small_box):
    x1, y1, x2, y2 = small_box
    return not (x1 <= x <= x2 and y1 <= y <= y2)


def is_goal(ball_x, ball_y, goal_left, goal_right, goal_line_y):
    return goal_left <= ball_x <= goal_right and ball_y <= goal_line_y