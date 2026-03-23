from game.ball import update_ball_position


def test_ball_moves_correctly():
    x, y = update_ball_position(10, 20, 5, -2, 2)
    assert x == 20
    assert y == 16