class GameWorld:
    def __init__(self):
        self.regions = []
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
        self.connections = {}
        self.properties = {}

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def add_connection(self, direction, target_region):
        self.connections[direction] = target_region

    def print_self(self):
        return f'You are in {self.properties["PortrayalProperties"]}. '


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
            return "You moved to " + self.position.name,True
        else:
            return "You can't go that way.", False

    # TODO - add other commands like take, use, drop ...

    def print_self(self):
        return f'{self.position.print_self()}.'
