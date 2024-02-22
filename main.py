from enums_consts import DIRECTIONS
from interpreter import parse_dsl

if __name__ == "__main__":
    gameWorld = parse_dsl()
    print(gameWorld.player.print_self())

    while True:
        if gameWorld.player.position == gameWorld.final_position:
            break

        user_input = input(">>").strip()

        if user_input in DIRECTIONS:
            text, moved = gameWorld.player.move(user_input[-1:], gameWorld)
            print(text)
            print(gameWorld.player.print_self())
