from typing import Any

import pygame
import pygame.font as f


class Text:
	text: str
	color: tuple[int, int, int]
	font: pygame.font.Font

	def __init__(
		self,
		text: str,
		size: int,
		color: tuple[int, int, int] = (0, 0, 0),
		sys_font: bool = True,
		font: str = 'Arial',
	):
		self.text = text
		self.color = color

		if not pygame.font.get_init():
			pygame.font.init()

		if sys_font:
			self.font = pygame.font.SysFont(font, size)
		else:
			self.font = pygame.font.Font(font, size)

	def render(self) -> pygame.Surface:
		return self.font.render(self.text, True, self.color)


def draw_text(
	text: str,
	width: int | None,
	font_size: int,
	font_family: tuple[str, bool] = ('Arial', True),
	color: tuple[int, int, int] = (255, 255, 255),
) -> pygame.Surface:
	if not f.get_init():
		f.init()

	font = None
	if font_family[1]:
		font = f.SysFont(font_family[0], font_size)
	else:
		font = f.Font(font_family[0], font_size)

	res = font.render(text, True, color)

	return res

	if width is None:
		return res
	else:
		return res.subsurface(0, 0, width, font_size)
