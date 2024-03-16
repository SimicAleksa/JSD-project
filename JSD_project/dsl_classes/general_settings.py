class GeneralSettings:
    def __init__(self):
        self.drop_old_weapon = False
        self.drop_old_armor = False
        self.additional_turn_after_use = False

    def set_drop_old_weapon(self, value):
        self.drop_old_weapon = value

    def set_drop_old_armor(self, value):
        self.drop_old_armor = value

    def set_additional_turn_after_use(self, value):
        self.additional_turn_after_use = value
