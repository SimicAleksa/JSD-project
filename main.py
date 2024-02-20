from interpreter import parse_dsl
if __name__ == "__main__":
    gameWorld = parse_dsl()
    print(gameWorld.player)