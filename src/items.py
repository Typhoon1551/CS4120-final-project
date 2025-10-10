class Item:
    active = None

    def apply_effect():
        pass


class ActiveItem(Item):
    active = True

    def apply_effect():
        pass


class PassiveItem(Item):
    active = False

    def apply_effect():
        pass
