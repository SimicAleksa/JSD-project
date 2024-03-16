class Armor:
    def __init__(self, name, armorType, defense, mana_defense, required_level):
        self.name = name
        self.type = armorType
        self.defense = defense
        self.mana_defense = mana_defense
        self.required_level = required_level
        self.modifiers = {}

    def add_modifier(self, attr_name, coefficients):
        self.modifiers[attr_name] = coefficients
