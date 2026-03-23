from game.rules import shot_is_outside_small_box, is_goal


def test_shot_outside_small_box():
    small_box = (40, 0, 60, 20)
    assert shot_is_outside_small_box(30, 25, small_box) is True


def test_shot_inside_small_box():
    small_box = (40, 0, 60, 20)
    assert shot_is_outside_small_box(50, 10, small_box) is False


def test_goal_detected():
    assert is_goal(50, 0, 40, 60, 0) is True


def test_not_goal_outside_posts():
    assert is_goal(70, 0, 40, 60, 0) is False