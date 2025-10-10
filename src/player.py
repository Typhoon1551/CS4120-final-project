class Player:
    name = ""
    inventory = []

    def __init__(self, _name, _inv):
        self.name = _name
        self.inventory = _inv

    def hello(self):
        print(f"Hello {self.name}!")
