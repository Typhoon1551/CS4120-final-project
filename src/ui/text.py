import pygame
from typing import Any


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
        font: str = "Arial",
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
