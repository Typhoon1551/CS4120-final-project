class Item:
    active = None
    name = ""
    description = ""
    icon = None

    def apply_effect(self, player, enemy):
        pass


class ActiveItem(Item):
    active = True


class PassiveItem(Item):
    active = False


######### Prefab Items ###########


class HealthPotion(ActiveItem):
    healing = 10

    def apply_effect(self, player, enemy):
        player.current_health += self.healing


class Weapon(ActiveItem):
    damage = 10

    def apply_effect(self, player, enemy):
        enemy.current_health -= self.damage


class Armor(PassiveItem):
    defense = 10

    def apply_effect(self, player, enemy):
        player.defense += self.defense
