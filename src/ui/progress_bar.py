import pygame


class ProgressBar:
	position: tuple[int, int]
	size: tuple[int, int]
	max_value: int | float
	value: int | float
	bg: tuple[int, int, int]
	fg: tuple[int, int, int]

	def __init__(
		self,
		position: tuple[int, int],
		size: tuple[int, int],
		max_value: int | float,
		value: int | float,
		background_color: tuple[int, int, int],
		foreground_color: tuple[int, int, int],
	):
		self.position = position
		self.size = size
		self.max_value = max_value
		self.value = value
		self.bg = background_color
		self.fg = foreground_color

	def render(self, surface: pygame.Surface):
		pygame.draw.rect(surface, self.bg, self.position + self.size)
		pygame.draw.rect(
			surface,
			self.fg,
			self.position
			+ (int(self.value / self.max_value * self.size[0]), self.size[1]),
		)
