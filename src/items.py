from typing import Callable, Any
from character import Character
import pygame


class Item:
    active: bool
    name: str
    description: str
    icon: pygame.Surface | None
    effect: Callable[[Character, Character, "Item"], Any]

    def __init__(self, _active, _name, _description, _icon, _effect):
        self.active = _active
        self.name = _name
        self.description = _description
        self.icon = _icon
        self.effect = _effect


# example item creation:
def health_potion(healing):
    def e(player: Character, enemy: Character, this: Item):
        player.current_health += healing
        player.inventory.remove(this)
        player.inventory.append(empty_bottle())

    return Item(
        True,
        "Health Potion",
        "",
        None,
        e,
    )


def empty_bottle():
    def effect(player: Character, enemy: Character, this: Item):
        enemy.current_health -= 10
        player.inventory.remove(this)

    return Item(
        True,
        "Empty Bottle",
        "",
        None,
        effect,
    )
