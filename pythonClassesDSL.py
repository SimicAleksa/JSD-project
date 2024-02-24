class GameWorld:
    def __init__(self):
        self.regions = []
        self.items = []
        self.enemies = []
        self.player = None
        self.current_enemy = None
        self.start_position = None
        self.final_position = None

    def check_combat(self, region):
        for enemy in self.enemies:
            if enemy.get_position() == region.name:
                self.current_enemy = enemy
                return True
        return False
    
    def set_start_position(self, region):
        self.start_position = region

    def set_final_position(self, region):
        self.final_position = region


class Region:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.connections = {}
        self.properties = {}

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def remove_item(self, item):
        for region_item in self.items:
            if item == region_item.name:
                self.items.remove(region_item)

    def is_item_contained(self, item):
        for region_item in self.items:
            if item == region_item.name:
                return True
        return False

    def add_connection(self, direction, target_region):
        self.connections[direction] = target_region

    def print_self(self):
        items = ""
        for item in self.items:
            items += item.name + ", "
        items = items[:-2]
        text = f"You are in {self.properties['PortrayalProperties']}. "
        if items:
            text += f"Inside you see {items}."
        return text


class Item:
    def __init__(self, name, is_static):
        self.name = name
        self.properties = {}
        self.isStatic = is_static

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def print_self(self):
        return f'{self.properties["PortrayalProperties"]}'

    def print_self_contains(self):
        items = ""
        for item in self.properties["ContainsProperties"]:
            items += item + ", "
        items = items[:-2]
        return f'{self.properties["PortrayalProperties"]}. Inside you see {items}'


class Player:
    def __init__(self, name, start_position):
        self.name = name
        self.position = start_position
        self.inventory = []
        self.health = 100
        self.properties = {}

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def remove_item(self, item):
        for region_item in self.position.items:
            if item == region_item.name:
                self.position.items.remove(region_item)
                break

    def attack(self, target):
        target.health -= 10
        return f"You hit you for {target.name} damage"
    
    def heal(self, amount):
        self.health += amount
        if amount > 0:
            return "You healed " + amount
        else:
            return "You took " + amount + " damage"

    def move(self, direction, game_world):
        if direction in self.position.connections:
            target_room = self.position.connections[direction]
            for region in game_world.regions:
                if region.name == target_room:
                    self.position = region
                    text = f"{self.name} moved to {self.position.name}."
                    if game_world.check_combat(region):
                        text += f"\nYou are in combat with {game_world.current_enemy.name}"
                    return text, True
        else:
            return "You can't go that way", False

    def take(self, item, game_world):
        if self.position.is_item_contained(item):
            for game_world_item in game_world.items:
                if item == game_world_item.name:
                    if not game_world_item.isStatic:
                        self.inventory.append(item)
                        self.remove_item(item)
                        return "You picked up " + game_world_item.name
                    else:
                        return "You cant do that"
        else:
            return "That item is not present in this room"

    def drop(self, item, game_world):
        if item in self.inventory:
            self.inventory.remove(item)
            for game_world_item in game_world.items:
                if item == game_world_item.name:
                    self.position.items.append(game_world_item)
                    return "You dropped " + item + " in " + self.position.name
        return "You dont have that item"

    def use(self, item, game_world):
        if item in self.inventory:
            for game_world_item in game_world.items:
                if game_world_item.name == item:
                    if "ActivationProperties" in game_world_item.properties:
                        action = game_world_item.properties["ActivationProperties"]
                        if action.name == "HealAction":
                            self.inventory.remove(item)
                            self.health += action.amount
                            return "You used " + item + ". Your health is now " + str(self.health)
                    else:
                        return "That item cant be used"
        return "You dont have that item"

    def open(self, item, game_world):
        if self.position.is_item_contained(item):
            for game_world_item in game_world.items:
                if item == game_world_item.name:
                    if "ContainsProperties" in game_world_item.properties:
                        for containItem in game_world_item.properties["ContainsProperties"]:
                            for temp_game_world_item in game_world.items:
                                if temp_game_world_item.name == containItem:
                                    self.position.items.append(temp_game_world_item)
                        self.remove_item(item)
                        return "You opened " + game_world_item.name+""
                    else:
                        return "You cant do that"
        else:
            return "You cant do that"

    def print_self(self):
        inventory = ""
        for item in self.inventory:
            inventory += item + ", "
        inventory = inventory[:-2]
        return f'{self.position.print_self()}Your backpack has {inventory}.'

    def print_inventory(self):
        inventory = ""
        for item in self.inventory:
            inventory += item + ", "
        inventory = inventory[:-2]
        return f'Your backpack has {inventory}.'

    def print_health(self):
        return f'You have {self.health} health.'

class Enemy:
    def __init__(self):
        self.name = ""
        self.position = ""  # Region object
        self.health = 60
        self.damage = 0
        self.reward_items = []
        self.properties = {}

    def get_position(self):
        return self.properties['PositionProperties']
    
    def get_description(self):
        return self.properties['PortrayalProperties']

    def get_health(self):
        return self.properties['HealthProperties']

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value
    
    def attack(self, target):
        target.health -= self.damage
        return f"{self.name} hits you for {self.damage} damage"
    
    def heal(self, amount):
        self.health += amount
        return "{self} healed " + amount

    def drop(self, item, game_world):
        if item in self.reward_items:
            self.reward_items.remove(item)
            for game_world_item in game_world.items:
                if item == game_world_item.name:
                    self.position.items.append(game_world_item)
                    return f"${self.name} dropped ${item}"
        return f"${self.name} does not have that item"

    def print_self(self):
        return f'There is an enemy: {self.name}.'

    def print_health(self):
        return f'{self.name} has {self.health} health.'


class HealAction:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class AttackAction:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount