from typing import Any, Callable

import pygame

import maths
from character import Character


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
        player.current_health = maths.clamp(
            player.current_health, 0, player.max_health
        )
        player.inventory.remove(this)
        player.inventory.append(empty_bottle())

    return Item(
        True,
        "Health Potion",
        f"A potion that heals you for {healing} hp",
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
        "Break on enemy's head to deal 10 damage",
        None,
        effect,
    )
