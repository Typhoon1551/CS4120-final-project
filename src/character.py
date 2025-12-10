from typing import Any
import pygame

class Character:
	current_health: int
	max_health: int
	inventory: list[Any] = []
	name: str
	description: str
	character_design = {
		"color": (255, 150, 38),
		"left": 50,
		"top": 100,
		"width": 25,
		"height": 25,
	}
	last: pygame.Rect

	def __init__(self, _health, _max, _starting_inven, _name, _description, _last = pygame.Rect(0,0,0,0)):
		self.current_health = _health
		self.max_health = _max
		self.inventory = _starting_inven
		self.name = _name
		self.description = _description
		self.last = _last
