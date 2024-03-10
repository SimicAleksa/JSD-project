from textx import metamodel_from_file
from os.path import join, dirname

from pythonClassesDSL import GameWorld, Region, Player, Enemy, Item, HealAction, Weapon, GeneralSettings


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
        for requirement in region_def.requirements:
            region.add_requirements(requirement)
        if region_def.environmental_dmg:
            region.add_environmental_dmg(region_def.environmental_dmg)
        for prop in region_def.properties:
            prop_name = prop.__class__.__name__
            if prop_name == "ContainsProperties":
                for item in prop.contains:
                    region.items.append(item)
        game_world.regions.append(region)

    # Create items
    for item_def in model.items:
        item = Item(item_def.name, item_def.isStatic)
        properties(item, item_def)
        game_world.items.append(item)

    # Create weapons
    for weapon_def in model.weapons:
        weapon = Weapon(weapon_def.name)
        properties(weapon, weapon_def)
        game_world.weapons[weapon_def.name] = weapon

    # Create player
    player_def = model.player
    starting_position = None
    health = 0
    current_experiance = 0
    needed_experiance_for_level_up = 100
    level = 1
    inventory = []
    vigor = 10
    strength = 10
    endurance = 10
    for prop in player_def.properties:
        prop_name = prop.__class__.__name__
        if prop_name == "PositionProperties":
            for player_region in game_world.regions:
                if prop.position.name == player_region.name:
                    starting_position = player_region
        elif prop_name == "HealthProperties":
            health = prop.health
        elif prop_name == "InventoryProperties":
            for item in prop.inventory:
                inventory.append(item.name)
        elif prop_name == "VigorAttribute":
            vigor = prop.vigor
        elif prop_name == "StrengthAttribute":
            strength = prop.strength
        elif prop_name == "EnduranceAttribute":
            endurance = prop.endurance
        elif prop_name == "CurrentExpProperty":
            current_experiance = prop.currentExperiance
        elif prop_name == "NeededExpProperty":
            needed_experiance_for_level_up = prop.neededExperianceForLevelUp
        elif prop_name == "LevelProperty":
            level = prop.level
    player = Player(player_def.name, starting_position)
    player.health = health
    player.current_experiance = current_experiance
    player.needed_experiance_for_level_up = needed_experiance_for_level_up
    player.level = level
    player.inventory = inventory
    player.vigor = vigor
    player.strength = strength
    player.endurance = endurance

    properties(player, player_def)
    game_world.player = player

    #Create enemies
    for enemy_def in model.enemies:
        enemy = Enemy()
        # for item in enemy_def.itemsToDrop:
        #     print(item)
        enemy.name = enemy_def.name
        properties(enemy, enemy_def)
        game_world.enemies.append(enemy)

    # Set start and final positions
    for player_region in game_world.regions:
        if player_region.name == model.start_position.name:
            game_world.set_start_position(player_region)
        elif player_region.name == model.final_position.name:
            game_world.set_final_position(player_region)

    # Set settings
    for settings_def in model.settings:
        settings = GeneralSettings()
        if settings_def.additionalTurnAfterUse:
            settings.set_additional_turn_after_use(True)
        if settings_def.dropOldWeapon:
            settings.set_drop_old_weapon(True)
        game_world.settings = settings

    return game_world
        

def properties(obj, obj_def):
    for prop in obj_def.properties:
        prop_name = prop.__class__.__name__
        prop_value = None
        if prop_name == "PortrayalProperties":
            prop_value = prop.portrayal
        elif prop_name == "ContainsProperties":
            prop_value = []
            for item in prop.contains:
                prop_value.append(item.name)
        elif prop_name == "PositionProperties":
            prop_value = prop.position.name
        elif prop_name == "ActivationProperties":
            action_name = prop.action.__class__.__name__
            if action_name == "HealAction":
                prop_value = HealAction(action_name, prop.action.amount)
        elif prop_name == "InventoryProperties":
            prop_value = []
            for item in prop.inventory:
                prop_value.append(item.name)
        elif prop_name == "HealthProperties":
            prop_value = prop.health
        elif prop_name == "WeaponProperties":
            prop_value = prop.damage
        elif prop_name == "ItemsToDrop" or prop_name == "WeaponsToDrop":
            prop_value = {}
            for item in prop.inventory:
                prop_value[item.name] = item
        # elif prop_name == "AttributeProperties":
        #     pass
        elif prop_name == "VigorAttribute":
            prop_value = prop.vigor
        elif prop_name == "StrengthAttribute":
            prop_value = prop.strength
        elif prop_name == "EnduranceAttribute":
            prop_value = prop.endurance
        elif prop_name == "Experience":
            prop_value = prop.xp
        obj.add_property(prop_name, prop_value)
