class GameWorld:
    def __init__(self):
        self.regions = []
        self.items = []
        self.player = None
        self.start_position = None
        self.final_position = None

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

    def add_connection(self, direction, target_region):
        self.connections[direction] = target_region

    def print_self(self):
        items = ""
        for item in self.items:
            items += item.name + ", "
        items = items[:-2]
        return f'You are in {self.properties["PortrayalProperties"]}. Inside you see {items}. '


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
        self.properties = {}

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def move(self, direction, game_world):
        if direction in self.position.connections:
            target_room = self.position.connections[direction]
            for region in game_world.regions:
                if region.name == target_room:
                    self.position = region
            return self.name + " moved to " + self.position.name, True
        else:
            return "You can't go that way", False

    # TODO - add other commands like take, use, drop ...

    def print_self(self):
        return f'{self.position.print_self()}'


class HealAction:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
