from textx import metamodel_from_file
from os.path import join, dirname

from pythonClassesDSL import GameWorld, Region, Player


def parse_dsl():
    # Load the metamodel from the DSL grammar
    this_folder = dirname(__file__)
    dsl_mm = metamodel_from_file(join(this_folder, "gameDSL.tx"))

    # Parse the DSL file and create the GameWorld
    model = dsl_mm.model_from_file("games/testGame.game/testGame.game")

    game_world = GameWorld()

    # Create regions
    for region_def in model.regions:
        region = Region(region_def.name)
        properties(region, region_def)
        for connection in region_def.connections:
            region.add_connection(connection.direction, connection.target)
        game_world.regions.append(region)

    # Create player
    player_def = model.player
    starting_position = None
    for prop in player_def.properties:
        prop_name = prop.__class__.__name__
        if prop_name == "PositionProperties":
            for player_region in game_world.regions:
                if prop.position.name == player_region.name:
                    starting_position = player_region
    player = Player(player_def.name, starting_position)
    properties(player, player_def)
    game_world.player = player

    # Set start and final positions
    for player_region in game_world.regions:
        if player_region.name == model.start_position.name:
            game_world.set_start_position(player_region)
        elif player_region.name == model.final_position.name:
            game_world.set_final_position(player_region)
    return game_world


def properties(obj, obj_def):
    for prop in obj_def.properties:
        prop_name = prop.__class__.__name__
        prop_value = None
        if prop_name == "PortrayalProperties":
            prop_value = prop.portrayal
        elif prop_name == "PositionProperties":
            prop_value = prop.position.name

        obj.add_property(prop_name, prop_value)
