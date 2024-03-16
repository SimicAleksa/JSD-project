class Item:
    def __init__(self, name, portrayal, is_static):
        self.name = name
        self.portrayal = portrayal
        self.contains = []
        self.activations = []
        self.isStatic = is_static

    def print_self(self):
        return f'{self.portrayal}'

    def print_self_contains(self):
        items = ""
        for item in self.contains:
            items += item + ", "
        items = items[:-2]
        return f'{self.portrayal}. Inside you see {items}'
