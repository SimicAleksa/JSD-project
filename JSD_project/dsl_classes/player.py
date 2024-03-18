import numpy as np


class Player:
    def __init__(self, name, start_position, vigor, endurance, strength, intelligence, health, mana, damage, defence,
                 mana_damage, mana_defence):
        self.name = name
        self.position = start_position
        self.inventory = []

        # basic stats
        self.health = health
        self.initial_health = health

        self.current_max_health = health
        self.unmodified_current_max_health = health

        self.current_experience = 0
        self.needed_experience_for_level_up = 100
        self.levelScalingPercentage = 10
        self.level = 1
        self.level_points = 0

        self.base_health = health
        self.mana = mana
        self.current_max_mana = mana
        self.base_mana = mana
        self.unmodified_mana = mana

        self.damage = damage
        self.unmodified_damage = damage

        self.defence = defence
        self.unmodified_defence = defence

        self.mana_damage = mana_damage
        self.unmodified_mana_damage = mana_damage

        self.mana_defence = mana_defence
        self.unmodified_mana_defence = mana_defence

        self.weapon = None
        self.armor = None
        self.can_equip = []

        # attributes
        self.vigor = vigor
        self.endurance = endurance
        self.strength = strength
        self.intelligence = intelligence

    def remove_item(self, item):
        del self.position.items[item]

    def strike_damage(self):
        if self.weapon is None or self.weapon.mana_cost > self.mana or self.weapon.health_cost >= self.health:
            return self.damage
        else:
            return self.damage * (1 + self.weapon.health_damage / 100)

    def get_mana_damage(self):
        if self.weapon is None or self.weapon.mana_cost > self.mana or self.weapon.health_cost >= self.health:
            return self.mana_damage
        else:
            return self.mana_damage * (1 + self.weapon.mana_damage / 100)

    def get_defense(self):
        if self.armor is None:
            return self.defence
        else:
            return self.armor.defense * (1 + self.defence / 100)

    def get_mana_defense(self):
        if self.armor is None:
            return self.mana_defence
        else:
            return self.armor.mana_defense * (1 + self.mana_defence / 100)

    def print_stats(self):
        print(
            f"Current stats:\nVigor - {self.vigor}\nEndurance - {self.endurance}\nStrength - {self.strength}\nIntelligence - {self.intelligence}"
            f"\nHealth - {self.health}\nDefence - {self.defence}\nDamage - {self.damage}\nMana - {self.mana}"
            f"\nMana damage - {self.mana_damage} \nMana defence - {self.mana_defence}\nMax health - {self.current_max_health}\nMax mana - {self.current_max_mana}")

    def inc_stat(self, stat):
        if stat == "vigor":
            return self.inc_vigor()
        elif stat == "strength":
            return self.inc_strength()
        elif stat == "endurance":
            return self.inc_endurance()
        elif stat == "intelligence":
            return self.inc_intelligence()
        else:
            return "Invalid stat"

    def inc_vigor(self):
        if self.level_points >= 1:
            self.vigor += 1
            self.level_points -= 1
            self.scale_health_from_vigor()
            return "Vigor increased"
        else:
            return "You don't have enough level up points for this command!"

    def scale_health_from_vigor(self):
        stat_modified = self.current_max_health != self.unmodified_current_max_health
        self.current_max_health = int(self.base_health * (1 + self.vigor / 100))
        self.unmodified_current_max_health = self.current_max_health
        if stat_modified:
            self.reapply_modification_single_stat('current_max_health')

    def inc_strength(self):
        if self.level_points >= 1:
            self.strength += 1
            self.level_points -= 1
            self.scale_damage_from_strength()
            return "Strength increased"
        else:
            return "You don't have enough level up points for this command!"

    def scale_damage_from_strength(self):
        stat_modified = self.damage != self.unmodified_damage
        self.damage *= (1 + self.strength / 100)
        self.unmodified_damage = self.damage
        if stat_modified:
            self.reapply_modification_single_stat('damage')

    def inc_endurance(self):
        if self.level_points >= 1:
            self.endurance += 1
            self.level_points -= 1
            self.scale_defence_from_endurance()
            return "Endurance increased"
        else:
            return "You don't have enough level up points for this command!"

    def scale_defence_from_endurance(self):
        stat_modified = self.defence != self.unmodified_defence
        self.defence *= (1 + self.endurance / 100)
        self.unmodified_defence = self.defence
        if stat_modified:
            self.reapply_modification_single_stat('defence')

    def inc_intelligence(self):
        if self.level_points >= 1:
            self.intelligence += 1
            self.level_points -= 1
            self.scale_mana_from_intelligence()
            return "Intelligence increased"
        else:
            return "You don't have enough level up points for this command!"

    def scale_mana_from_intelligence(self):
        stat_modified = self.mana != self.unmodified_mana
        self.mana = self.base_mana * (1 + self.intelligence / 100)
        self.unmodified_mana = self.mana
        if stat_modified:
            self.reapply_modification_single_stat('mana')

    def monster_slain(self, current_enemy):
        self.current_experience += current_enemy.get_xp_value()
        if self.current_experience >= self.needed_experience_for_level_up:
            while self.current_experience >= self.needed_experience_for_level_up:
                self.current_experience -= self.needed_experience_for_level_up
                self.level += 1
                self.level_points += 1
                self.needed_experience_for_level_up *= (1 + (self.levelScalingPercentage / 100))
                print(f"You leveled up to: {self.level} level.")
            print(f"You have {self.level_points} points to use")

    def get_health(self):
        return self.health

    def set_health(self, value):
        self.health = value

    def heal(self, value):
        self.health = min(self.current_max_health, self.health + value)

    def restore_mana(self, value):
        self.mana = min(self.current_max_mana, self.mana + value)

    def get_mana(self):
        return self.mana

    def set_mana(self, value):
        self.mana = value
        self.unmodified_mana = value

    def move(self, direction, game_world):
        if game_world.current_enemy is not None:
            return "You shall not pass", False
        if direction in self.position.connections:
            target_room = self.position.connections[direction]
            for region in game_world.regions:
                if region.name == target_room:
                    if len(region.requirements) == 0:
                        return self._change_player_position(region, game_world)
                    elif _check_if_the_requirements_are_met(region.requirements, self.inventory):
                        self.inventory = _remove_met_region_requirements_from_player_inventory(region.requirements,
                                                                                               self.inventory)
                        region.requirements = []
                        return self._change_player_position(region, game_world)
                    else:
                        return "Requirements not matched. You need a " + region.print_requirements(), False
        else:
            return "You can't go that way", False

    def move_to_start_position(self, game_world):
        return self._change_player_position(game_world.start_position, game_world)

    def _change_player_position(self, region, game_world):
        self.position = region
        text = f"{self.name} moved to {self.position.name}."
        if region.environmental_dmg:
            environmental_dmg = region.environmental_dmg.amount - self.endurance
            environmental_dmg = 0 if environmental_dmg < 0 else environmental_dmg
            self.health -= environmental_dmg
            if region.environmental_dmg.amount != 0:
                text += f"\nYou took {environmental_dmg} environmental damage"
                text += f"\nYou now have {self.health} health"
        if game_world.check_combat(region):
            text += f"\nYou encounter a {game_world.current_enemy.name}!"
        return text, True

    def take(self, item, game_world):
        if self.position.is_item_contained(item):
            if item in game_world.items:
                game_world_item = game_world.items[item]
                if not game_world_item.isStatic:
                    self.inventory.append(item)
                    self.remove_item(item)
                    return "You picked up " + game_world_item.name
                else:
                    return "You cant do that"
            if item in game_world.weapons:
                self.take_weapon(item, game_world)
                return f"You picked up {item}. You might be able to equip it."
            if item in game_world.armors:
                self.take_armor(item, game_world)
                return f"You picked up {item}. You might be able to equip it."
        else:
            return "That item is not present in this room"

    def equip(self, item, game_world):
        if item in self.inventory:
            text = ""
            if item in game_world.weapons:
                if self.level >= game_world.weapons[item].required_level and game_world.weapons[item].type in self.can_equip:
                    if self.weapon is not None:
                        self.remove_stat_modifications(self.weapon)
                    self.weapon = game_world.weapons[item]
                    self.apply_stat_modifications(self.weapon)
                    text = f"You equipped {item}. It deals additional {self.weapon.health_damage} damage."
                else:
                    text = "You cannot equip this."
            elif item in game_world.armors:
                if self.level >= game_world.armors[item].required_level and game_world.armors[item].type in self.can_equip:
                    if self.armor is not None:
                        self.remove_stat_modifications(self.armor)
                    self.armor = game_world.armors[item]
                    self.apply_stat_modifications(self.armor)
                    text = f"You equipped {item}. It gives additional {self.armor.defense} defense."
                else:
                    text = "You cannot equip this."
            if game_world.current_enemy is not None and not game_world.settings.additional_turn_after_use:
                text += "\n" + game_world.attack_player()
            return text
        return f"You don't have that item {item}"

    def unequip(self, item, _game_world):
        if self.weapon is not None and item == self.weapon.name:
            self.remove_stat_modifications(self.weapon)
            self.weapon = None
            return f"You unequipped {item}"
        elif self.armor is not None and item == self.armor.name:
            self.remove_stat_modifications(self.armor)
            self.armor = None
            return f"You unequipped {item}"
        return f"{item} is not equipped"

    def take_weapon(self, weapon, game_world):
        self.inventory.append(weapon)
        self.remove_item(weapon)
        if self.weapon is not None and game_world.settings.drop_old_weapon:
            self._drop_old_weapon(self.weapon.name, game_world)
        if self.weapon is not None:
            self.remove_stat_modifications(self.weapon)

    def take_armor(self, armor, game_world):
        self.inventory.append(armor)
        self.remove_item(armor)
        if self.armor is not None and game_world.settings.drop_old_armor:
            self._drop_old_armor(self.armor.name, game_world)
        if self.armor is not None:
            self.remove_stat_modifications(self.armor)

    def apply_stat_modifications(self, item):
        for property_to_modify, coefficients in item.modifiers.items():
            modified_value = np.polyval(coefficients, getattr(self, property_to_modify))
            setattr(self, property_to_modify, modified_value)

    def reapply_modification_single_stat(self, property_to_modify):
        if self.weapon is not None and property_to_modify in self.weapon.modifiers:
            modified_value = np.polyval(self.weapon.modifiers[property_to_modify], getattr(self, property_to_modify))
            setattr(self, property_to_modify, modified_value)
        if self.armor is not None and property_to_modify in self.armor.modifiers:
            modified_value = np.polyval(self.armor.modifiers[property_to_modify], getattr(self, property_to_modify))
            setattr(self, property_to_modify, modified_value)

    def remove_stat_modifications(self, item):
        for property_to_modify, coefficients in item.modifiers.items():
            original_value = getattr(self, f'unmodified_{property_to_modify}')
            setattr(self, property_to_modify, original_value)

    def drop(self, item, game_world):
        if item in self.inventory:
            self.inventory.remove(item)
            if item in game_world.items:
                game_world_item = game_world.items[item]
                self.position.items[item] = game_world_item
                return "You dropped " + item + " in " + self.position.name
        return "You dont have that item"

    def drop_items_after_death(self, game_world):
        direction = game_world.opposite_dirs[game_world.prev_direction]
        target_room = self.position.connections[direction]
        for region in game_world.regions:
            if region.name == target_room:
                for item in self.inventory:
                    if item in game_world.items:
                        region.items[item] = game_world.items[item]
                    elif item in game_world.weapons:
                        region.items[item] = game_world.weapons[item]
                self.inventory = []
                self.weapon = None
                self.current_experience = 0
                self.health = self.initial_health
                return f"Your possessions are in {region.name}"
        return ""

    def _drop_old_weapon(self, item, game_world):
        if item in self.inventory and item in game_world.weapons:
            self.position.items[item] = game_world.weapons[item]
            self.inventory.remove(item)
            print("You dropped " + item + " in " + self.position.name)
        else:
            print("You don't have that item")

    def _drop_old_armor(self, item, game_world):
        if item in self.inventory and item in game_world.armors:
            self.position.items[item] = game_world.armors[item]
            self.inventory.remove(item)
            print("You dropped " + item + " in " + self.position.name)
        else:
            print("You don't have that item")

    def use(self, item, game_world):
        if item in self.inventory:
            text = ""
            if item in game_world.items:
                game_world_item = game_world.items[item]
                if len(game_world_item.activations) == 0:
                    return "That item can't be used"
                for action in game_world_item.activations:
                    action.activate(self)
                self.inventory.remove(item)
                text = "You used " + item + ". Your health is now " + str(self.health)
            if game_world.current_enemy is not None and not game_world.settings.additional_turn_after_use:
                text += "\n" + game_world.attack_player()
            return text
        return f"You don't have that item {item}"

    def open(self, item, game_world):
        if self.position.is_item_contained(item):
            if item in game_world.items:
                game_world_item = game_world.items[item]
                if len(game_world_item.contains) > 0:
                    for containItem in game_world_item.contains:
                        for temp_game_world_item in game_world.items:
                            if temp_game_world_item == containItem:
                                self.position.items[temp_game_world_item] = game_world.items[temp_game_world_item]
                    self.remove_item(item)
                    return "You opened " + game_world_item.name + ""
                else:
                    return "You can't do that"
        else:
            return "You can't do that"

    def print_self(self):
        inventory = ""
        for item in self.inventory:
            inventory += item + ", "
        inventory = inventory[:-2]
        if inventory == "":
            return f'{self.position.print_self()}Your backpack is empty.'
        return f'{self.position.print_self()}Your backpack has {inventory}.'

    def print_inventory(self):
        inventory = ""
        for item in self.inventory:
            inventory += item + ", "
        inventory = inventory[:-2]
        if inventory == "":
            return f'{self.position.print_self()}Your backpack is empty.'
        return f'Your backpack has {inventory}.'

    def print_health(self):
        return f'You have {self.health} health.'


def _check_if_the_requirements_are_met(region_requirements, player_inventory):
    for region_req in region_requirements:
        req_met = False
        for player_item in player_inventory:
            if player_item == region_req.item:
                req_met = True
                break
        if not req_met:
            return req_met
    return True


def _remove_met_region_requirements_from_player_inventory(region_requirements, player_inventory):
    ret_val = []
    for player_item in player_inventory:
        needed_req = False
        for region_req in region_requirements:
            if player_item == region_req.item:
                needed_req = True
                break
        if not needed_req:
            ret_val.append(player_item)
    return ret_val
