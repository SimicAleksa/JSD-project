class Armor:
    def __init__(self, name, portrayal, armorType, defense, mana_defense, required_level):
        self.name = name
        self.portrayal = portrayal
        self.type = armorType
        self.defense = defense
        self.mana_defense = mana_defense
        self.required_level = required_level
        self.modifiers = {}

    def add_modifier(self, attr_name, coefficients):
        self.modifiers[attr_name] = coefficients

    def print_with_modifiers(self, player):
        text = f'{self.portrayal}'
        for stat, coefficients in self.modifiers.items():
            text += f'\nModifies {stat}: {player.__getattribute__(stat)} -> {np.polyval(coefficients, player.__getattribute__(stat))}'
        return text
