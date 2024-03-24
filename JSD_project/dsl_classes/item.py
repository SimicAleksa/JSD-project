class Item:
    def __init__(self, name, portrayal, is_static):
        self.name = name
        self.portrayal = portrayal
        self.contains = []
        self.activations = []
        self.isStatic = is_static

    def print_self(self):
        return f'{self.portrayal}'

    def restores_health(self):
        return 'HealAction' in [action.__class__.__name__ for action in self.activations]

    def restores_mana(self):
        return 'RestoreManaAction' in [action.__class__.__name__ for action in self.activations]

    def print_self_with_activations(self):
        restores_health = self.restores_health()
        restores_mana = self.restores_mana()
        if restores_health and restores_mana:
            return f'{self.portrayal} Restores health and mana.'
        if restores_health:
            return f'{self.portrayal} Restores health.'
        if restores_mana:
            return f'{self.portrayal} Restores mana.'
        return f'{self.portrayal}'

    def print_self_contains(self):
        items = ""
        for item in self.contains:
            items += item + ", "
        items = items[:-2]
        return f'{self.portrayal}. Inside you see {items}'
