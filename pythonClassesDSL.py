from random import uniform


class GameWorld:
    def __init__(self):
        self.regions = []
        self.items = []
        self.enemies = []
        self.weapons = {}
        self.player = None
        self.current_enemy = None
        self.start_position = None
        self.final_position = None
        self.prev_direction = None
        self.opposite_dirs = {"N": "S", "S": "N", "E": "W", "W": "E"}
        self.settings = None

    def check_combat(self, region):
        for enemy in self.enemies:
            if enemy.get_position() == region.name:
                self.current_enemy = enemy
                return True
        return False

    def set_start_position(self, region):
        self.start_position = region

    def set_final_position(self, region):
        self.final_position = region

    def flee(self):
        print("You fled!")
        self.current_enemy = None
        self.player.move(self.opposite_dirs[self.prev_direction], self)
        print(self.player.print_self())

    def attack_enemy(self):
        damage = int(self.player.strike_damage() * uniform(0.7, 1.3))
        enemy_health = self.current_enemy.get_health() - damage
        if enemy_health < 0:
            enemy_health = 0
        self.current_enemy.set_health(enemy_health)
        print(f"You dealt {damage} damage. Enemy has {self.current_enemy.get_health()} health.")
        if enemy_health == 0:
            print(f"You beat {self.current_enemy.name}!")
            self.current_enemy.set_position_none()
            self.player.monster_slain(self.current_enemy)
            dropped_items = self.current_enemy.get_droppable()
            for item in dropped_items:
                self.player.position.items.append(item)
            if len(dropped_items) > 0:
                print(f"{self.current_enemy.name} dropped {', '.join([item.name for item in dropped_items])}")
            self.current_enemy = None
        else:
            print(self.attack_player())

    def attack_player(self):
        damage = int(self.current_enemy.get_damage() * uniform(0.7, 1.3))
        player_health = self.player.get_health() - damage
        if player_health < 0:
            player_health = 0
        self.player.set_health(player_health)
        text = f"{self.current_enemy.name}'s turn.\n{self.current_enemy.name} dealt {damage} damage. You have {self.player.get_health()} health."
        if player_health == 0:
            text += "\nYou died"
            text_val, _ = self.player.move_to_start_position(self)
            text += f"\n{text_val}"
            self.current_enemy = None
        return text


class Region:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.connections = {}
        self.properties = {}
        self.requirements = []
        self.environmental_dmg = None

    def add_requirements(self, requirement):
        self.requirements.append(requirement)

    def add_environmental_dmg(self, environmental_dmg):
        self.environmental_dmg = environmental_dmg

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def remove_item(self, item):
        for region_item in self.items:
            if item == region_item.name:
                self.items.remove(region_item)

    def is_item_contained(self, item):
        for region_item in self.items:
            if item == region_item.name:
                return True
        return False

    def add_connection(self, direction, target_region):
        self.connections[direction] = target_region

    def print_self(self):
        items = ""
        for item in self.items:
            items += item.name + ", "
        items = items[:-2]
        text = f"You are in {self.properties['PortrayalProperties']}. "
        if items:
            text += f"Inside you see {items}. "
        return text

    def print_requirements(self):
        reqs = ""
        for req in self.requirements:
            reqs += str(req.item) + ", "
        reqs = reqs[:-2]
        return reqs


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
        self.inventory = []
        self.health = 100
        self.current_experience = 0
        self.needed_experience_for_level_up = 100
        self.level = 1
        self.level_points = 0
        self.properties = {}
        self.weapon = None
        self.vigor = 10
        self.endurance = 10
        self.strength = 10

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def remove_item(self, item):
        for region_item in self.position.items:
            if item == region_item.name:
                self.position.items.remove(region_item)
                break

    def attack(self, target):
        target.health -= 10
        return f"You hit you for {target.name} damage"

    def strike_damage(self):
        if self.weapon is None:
            return 10 * (self.strength / 10)
        else:
            damage = self.weapon.get_damage()
            damage *= (1 + self.strength / 100)
            return damage

    def print_stats(self):
        print(f"Current stats:\nVigor - {self.vigor}\nEndurance - {self.endurance}\nStrength - {self.strength}")

    def inc_stat(self, stat):
        if stat == "vigor":
            return self.inc_vigor()
        elif stat == "strength":
            return self.inc_strength()
        elif stat == "endurance":
            return self.inc_endurance()
        else:
            return "Invalid stat"

    def inc_vigor(self):
        if self.level_points >= 1:
            self.vigor += 1
            self.level_points -= 1
            health = self.get_health()
            health *= (1 + self.vigor / 100)
            self.set_health(health)
            return "Vigor increased"
        else:
            return "You don't have enough level up points for this command!"

    def inc_strength(self):
        if self.level_points >= 1:
            self.strength += 1
            self.level_points -= 1
            return "Strength increased"
        else:
            return "You don't have enough level up points for this command!"

    def inc_endurance(self):
        if self.level_points >= 1:
            self.endurance += 1
            self.level_points -= 1
            return "Endurance increased"
        else:
            return "You don't have enough level up points for this command!"

    def monster_slain(self, current_enemy):
        self.current_experience += current_enemy.get_xp_value()
        if self.current_experience >= self.needed_experience_for_level_up:
            while self.current_experience >= self.needed_experience_for_level_up:
                self.current_experience -= self.needed_experience_for_level_up
                self.level += 1
                self.level_points += 1
                self.needed_experience_for_level_up *= 1.1
                print(f"You leveled up to: {self.level} level.")
            print(f"You have {self.level_points} points to use")

    def heal(self, amount):
        self.health += amount
        if amount > 0:
            return "You healed " + amount
        else:
            return "You took " + amount + " damage"

    def get_health(self):
        return self.health

    def set_health(self, value):
        self.health = value

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
            for game_world_item in game_world.items:
                if item == game_world_item.name:
                    if not game_world_item.isStatic:
                        self.inventory.append(item)
                        self.remove_item(item)
                        return "You picked up " + game_world_item.name
                    else:
                        return "You cant do that"
            if item in game_world.weapons:
                self.take_weapon(item, game_world)
                return f"You picked up {item}. You equipped {item}. It deals additional {game_world.weapons[item].get_damage()} damage."
        else:
            return "That item is not present in this room"

    def take_weapon(self, weapon, game_world):
        self.inventory.append(weapon)
        self.remove_item(weapon)
        if self.weapon is not None and game_world.settings.drop_old_weapon:
            self._drop_old_weapon(self.weapon.name, game_world)
        self.weapon = game_world.weapons[weapon]

    def drop(self, item, game_world):
        if item in self.inventory:
            self.inventory.remove(item)
            if item in [i.name for i in game_world.items]:
                self.position.items.append(item)
                return "You dropped " + item + " in " + self.position.name
        return "You dont have that item"

    def _drop_old_weapon(self, item, game_world):
        if item in self.inventory:
            self.inventory.remove(item)
            if item in [i.name for i in game_world.items]:
                self.position.items.append(item)
                print("You dropped " + item + " in " + self.position.name)
            elif item in game_world.weapons:
                self.position.items.append(game_world.weapons[item])
                print("You dropped " + item + " in " + self.position.name)
        else:
            print("You don't have that item")

    def use(self, item, game_world):
        if item in self.inventory:
            text = ""
            for game_world_item in game_world.items:
                if game_world_item.name == item:
                    if "ActivationProperties" in game_world_item.properties:
                        action = game_world_item.properties["ActivationProperties"]
                        if action.name == "HealAction":
                            self.inventory.remove(item)
                            self.health += action.amount
                            text = "You used " + item + ". Your health is now " + str(self.health)
                    else:
                        return "That item can't be used"
            if item in game_world.weapons:
                self.weapon = game_world.weapons[item]
                text = f"You equipped {item}. It deals additional {game_world.weapons[item].get_damage()} damage."
            if game_world.current_enemy is not None and not game_world.settings.additional_turn_after_use:
                text += "\n" + game_world.attack_player()
            return text
        return f"You don't have that item {item}"

    def open(self, item, game_world):
        if self.position.is_item_contained(item):
            for game_world_item in game_world.items:
                if item == game_world_item.name:
                    if "ContainsProperties" in game_world_item.properties:
                        for containItem in game_world_item.properties["ContainsProperties"]:
                            for temp_game_world_item in game_world.items:
                                if temp_game_world_item.name == containItem:
                                    self.position.items.append(temp_game_world_item)
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


class Enemy:
    def __init__(self):
        self.name = ""
        self.position = ""  # Region object
        self.health = 60
        self.damage = 0
        self.reward_items = []
        self.properties = {}
        self.items_to_drop = {}
        self.weapons_to_drop = {}

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

    def set_health(self, value):
        self.properties['HealthProperties'] = value

    def get_damage(self):
        return self.properties['WeaponProperties']

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value

    def get_droppable(self):
        result = []
        for i in self.properties['ItemsToDrop']:
            result.append(self.properties['ItemsToDrop'][i])
        for w in self.properties['WeaponsToDrop']:
            result.append(self.properties['WeaponsToDrop'][w])
        return result

    def attack(self, target):
        target.health -= self.damage
        return f"{self.name} hits you for {self.damage} damage"

    def heal(self, amount):
        self.health += amount
        return "{self} healed " + amount

    def drop(self, item, game_world):
        if item in self.reward_items:
            self.reward_items.remove(item)
            for game_world_item in game_world.items:
                if item == game_world_item.name:
                    self.position.items.append(game_world_item)
                    return f"${self.name} dropped ${item}"
        return f"${self.name} does not have that item"

    def print_self(self):
        return f'There is an enemy: {self.name}.'

    def print_health(self):
        return f'{self.name} has {self.health} health.'


class Weapon:
    def __init__(self, name):
        self.name = name
        self.properties = {}

    def get_damage(self):
        return self.properties["WeaponProperties"]

    def add_property(self, prop_name, prop_value):
        self.properties[prop_name] = prop_value


class HealAction:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class AttackAction:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class GeneralSettings:
    def __init__(self):
        self.drop_old_weapon = False
        self.additional_turn_after_use = False

    def set_drop_old_weapon(self, value):
        self.drop_old_weapon = value

    def set_additional_turn_after_use(self, value):
        self.additional_turn_after_use = value


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
