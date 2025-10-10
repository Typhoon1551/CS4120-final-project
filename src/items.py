class Item:
    active = None
    name = ""
    description = ""
    icon = None
    effect = None

    def __init__(self, _active, _name, _description, _icon, _effect):
        self.active = _active
        self.name = _name
        self.description = _description
        self.icon = _icon
        self.effect = _effect


def health_potion(healing):
    def e(player, enemy):
        player.current_health += healing

    return Item(
        True,
        "Health Potion",
        "",
        None,
        e,
    )
