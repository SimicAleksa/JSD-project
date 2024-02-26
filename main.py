from enums_consts import DIRECTIONS, display_help
from interpreter import parse_dsl

global game_world


def process_command(command):
    commands_mapping = {
        "move": game_world.player.move,
        "take": game_world.player.take,
        "drop": game_world.player.drop,
        "use": game_world.player.use,
        "open": game_world.player.open,
    }
    try:
        action, arg = command.split(" ", 1)
        if action in commands_mapping:
            if "move" in command:
                if command in DIRECTIONS:
                    text, moved = commands_mapping[action](arg, game_world)
                    if moved:
                        game_world.prev_direction = arg
            else:
                text = commands_mapping[action](arg, game_world)
            print(text)
            print(game_world.player.print_self())
            if game_world.current_enemy is not None:
                game_world.do_combat()
        else:
            print("Invalid command")
    except Exception as e:
        print(e)
        if command == "help":
            display_help()
        elif command == "inventory":
            print(game_world.player.print_inventory())
        elif command == "health":
            print(game_world.player.print_health())
        else:
            print("Invalid command")


def initial_setup():
    global game_world
    game_world = parse_dsl()
    print("Enter 'help' for help")
    print(game_world.player.print_self())


if __name__ == "__main__":
    initial_setup()

    while game_world.player.position != game_world.final_position:
        user_input = input(">>").strip()
        process_command(user_input)
