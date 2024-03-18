import numpy as np

class Weapon:
    def __init__(self, name, portrayal, weaponType, health_damage, mana_damage, health_cost, mana_cost, required_level):
        self.name = name
        self.portrayal = portrayal
        self.type = weaponType
        self.health_damage = health_damage
        self.mana_damage = mana_damage
        self.health_cost = health_cost
        self.mana_cost = mana_cost
        self.required_level = required_level
        self.modifiers = {}

    def add_modifier(self, attr_name, coefficients):
        self.modifiers[attr_name] = coefficients

    def print_with_modifiers(self, player):
        text = f'{self.portrayal}'
        for stat, coefficients in self.modifiers.items():
            text += f'\nModifies {stat}: {player.__getattribute__(stat)} -> {np.polyval(coefficients, player.__getattribute__(stat))}'
        return text
