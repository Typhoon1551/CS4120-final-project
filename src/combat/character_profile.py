import ui
from character import Character
from pygame import Surface


class CharacterProfile:
	name_card: ui.TextBox
	hp_card: ui.TextBox
	hp_bar: ui.ProgressBar

	def __init__(
		self,
		character: Character,
		position: tuple[int, int],
		size: tuple[int, int],
		bg_color: tuple[int, int, int],
	) -> None:
		self.name_card = ui.TextBox(
			position,
			(size[0] // 2, 80),
			character.name,
			padding=15,
			color=bg_color,
		)
		self.hp_card = ui.TextBox(
			(position[0] + size[0] // 2, position[1]),
			(size[0] // 2, 80),
			"",
			padding=15,
			color=bg_color,
		)
		self.hp_bar = ui.ProgressBar(
			(position[0], position[1] + 80),
			(size[0], 40),
			character.max_health,
			0,
			(255, 0, 0),
			(0, 255, 0),
		)
		self.update_info(character)

	def update_info(self, character: Character) -> None:
		self.hp_card.text = (
			f"{character.current_health} / {character.max_health}"
		)
		self.hp_bar.value = character.current_health

	def render(self, surface: Surface):
		self.hp_bar.render(surface)
		self.name_card.render(surface)
		self.hp_card.render(surface)
