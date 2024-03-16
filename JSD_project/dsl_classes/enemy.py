import numpy as np


class Enemy:
    def __init__(self):
        self.name = ""
        self.position = ""  # Region object
        self.initial_health = 0
        self.damage = 0
        self.mana_damage = 0
        self.properties = {}
        self.items_to_drop = {}
        self.weapons_to_drop = {}
        self.attacks = []
        self.healing_chance = 0
        self.healing_amount = 0
        self.healing_amount_variance = 0

    def get_xp_value(self):
        return self.properties['Experience']

    def get_position(self):
        return self.properties['PositionProperties']

    def set_position_none(self):
        self.properties['PositionProperties'] = None

    def get_description(self):
        return self.properties['PortrayalProperties']

    def get_health(self):
        return self.properties['HealthProperties']

    def get_mana(self):
        if 'ManaProperties' not in self.properties:
            return 0
        return self.properties['ManaProperties']

    def set_health(self, value):
        self.properties['HealthProperties'] = value

    def set_mana(self, value):
        self.properties['ManaProperties'] = value

    def reduce_health(self, value):
        self.properties['HealthProperties'] -= value

    def reduce_mana(self, value):
        self.properties['ManaProperties'] -= value

    def heal(self, value):
        self.properties['HealthProperties'] = min(self.initial_health, self.properties['HealthProperties'] + value)

    def reset_health(self):
        self.set_health(self.initial_health)

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value
        if prop_name == 'HealthProperties':
            self.initial_health = self.get_health()

    def get_droppable(self):
        result = []
        for i in self.properties['ItemsToDrop']:
            result.append(self.properties['ItemsToDrop'][i])
        for w in self.properties['WeaponsToDrop']:
            result.append(self.properties['WeaponsToDrop'][w])
        for a in self.properties['ArmorsToDrop']:
            result.append(self.properties['ArmorsToDrop'][a])
        return result

    def choose_attack(self):
        feasible_attacks = [attack for attack in self.attacks if attack.health_cost < self.get_health() and attack.mana_cost <= self.get_mana()]
        # TODO: handle case when no feasible attacks
        if len(feasible_attacks) == 1:
            return feasible_attacks[0]
        attack_probabilities = [attack['frequency'] for attack in feasible_attacks]
        normalized_probabilities = np.array(attack_probabilities) / sum(attack_probabilities)
        return np.random.choice(feasible_attacks, p=normalized_probabilities)

    def print_self(self):
        return f'There is an enemy: {self.name}.'
