from enums_consts import DIRECTIONS
from interpreter import parse_dsl

if __name__ == "__main__":
    gameWorld = parse_dsl()

    while True:
        user_input = input(">>")

        if user_input in DIRECTIONS:
            text,moved = gameWorld.player.move(user_input[-1:],gameWorld)
            print(text)