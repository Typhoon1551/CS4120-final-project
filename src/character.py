class Character:
    current_health = 0
    items = []
    name = ""
    description = ""
    character_design = {
        "color": (0, 0, 0),
        "left": 50,
        "top": 100,
        "width": 101,
        "height": 101,
    }

    def __init__(self, _health, _starting_inven, _name, _description):
        self.current_health = _health
        self.items = _starting_inven
        self.name = _name
        self.description = _description
