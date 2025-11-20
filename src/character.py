from typing import Any


class Character:
    current_health: int
    max_health: int
    inventory: list[Any] = []
    name: str
    description: str
    character_design = {
        "color": (0, 120, 120),
        "left": 50,
        "top": 100,
        "width": 25,
        "height": 25,
    }

    def __init__(self, _health, _starting_inven, _name, _description):
        self.current_health = _health
        self.max_health = _health
        self.inventory = _starting_inven
        self.name = _name
        self.description = _description
