from game.goalkeeper import should_goalkeeper_dive, dive_direction


def test_keeper_dives_when_ball_is_close():
    assert should_goalkeeper_dive(ball_y=8, trigger_y=10) is True


def test_keeper_waits_when_ball_is_far():
    assert should_goalkeeper_dive(ball_y=30, trigger_y=10) is False


def test_dive_left():
    assert dive_direction(ball_x=30, keeper_center_x=50) == "left"


def test_dive_right():
    assert dive_direction(ball_x=70, keeper_center_x=50) == "right"


def test_dive_center():
    assert dive_direction(ball_x=50, keeper_center_x=50) == "center"