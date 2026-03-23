from game.rules import shot_is_outside_small_box
from game.goalkeeper import dive_direction
from game.ball import update_ball_position


def main():
    small_box = (40, 0, 60, 20)
    print("Scorer iniciado")
    print("Remate válido:", shot_is_outside_small_box(30, 25, small_box))
    print("Direção do GR:", dive_direction(35, 50))
    print("Nova posição da bola:", update_ball_position(10, 20, 5, -2, 2))


if __name__ == "__main__":
    main()