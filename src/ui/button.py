from typing import Any

import pygame

import ui


class Button:
	position: tuple[int, int]
	size: tuple[int, int]
	id: Any | None
	text_box: Any
	tool_tip: Any | None
	color: tuple[int, int, int]
	hovered_color: tuple[int, int, int]

	def __init__(
		self,
		position: tuple[int, int],
		size: tuple[int, int],
		text: str,
		text_color: tuple[int, int, int] = (0, 0, 0),
		text_font: tuple[str, bool] = ('Arial', True),
		id: Any | None = None,
		color: tuple[int, int, int] = (255, 255, 255),
		hovered_color: tuple[int, int, int] = (200, 200, 200),
		padding: int = 0,
	):
		self.position = position
		self.size = size
		self.id = id
		self.text_box = ui.TextBox(
			self.position,
			self.size,
			text,
			text_color,
			text_font,
			color,
			padding,
		)
		self.color = color
		self.hovered_color = hovered_color
		self.tool_tip = None

	def tooltip(
		self,
		text: str,
		color: tuple[int, int, int],
		width: float,
		font_color: tuple[int, int, int],
		font_size: int,
		padding: int,
		font_family: tuple[str, bool] = ('Arial', True),
	):
		self.tool_tip = ui.TextBox(
			(self.position[0], self.position[1] + self.size[1]),
			(int(width * self.size[0]), padding * 2 + font_size),
			text,
			font_color,
			font_family,
			color,
			padding,
		)

		return self

	def pressed(self) -> bool:
		return self.hovered() and pygame.mouse.get_just_pressed()[0]

	def held(self) -> bool:
		return self.hovered() and pygame.mouse.get_pressed()[0]

	def render(self, surface: pygame.Surface):
		if self.hovered():
			self.text_box.color = self.hovered_color

			if self.tool_tip:
				self.tool_tip.render(surface)
		else:
			self.text_box.color = self.color

		self.text_box.render(surface)

	def hovered(self) -> bool:
		mouse_pos = pygame.mouse.get_pos()

		check_x = (
			mouse_pos[0] >= self.position[0]
			and mouse_pos[0] <= self.position[0] + self.size[0]
		)

		check_y = (
			mouse_pos[1] >= self.position[1]
			and mouse_pos[1] <= self.position[1] + self.size[1]
		)

		return check_x and check_y
