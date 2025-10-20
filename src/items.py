class Item:
    active = None
    name = None
    description = None
    icon = None
    effect = None

    def __init__(self, _active, _name, _description, _icon, _effect):
        self.active = _active
        self.name = _name
        self.description = _description
        self.icon = _icon
        self.effect = _effect


# example item creation:
def health_potion(healing):
    def e(player, enemy, this):
        player.current_health += healing

    return Item(
        True,
        "Health Potion",
        "",
        None,
        e,
    )


def empty_bottle():
    def effect(player, enemy, this):
        enemy.current_health -= 10
        player.items.remove(this)

    return Item(
        True,
        "Empty Bottle",
        "",
        None,
        effect,
    )
