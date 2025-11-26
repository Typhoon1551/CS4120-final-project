from typing import Any

import pygame

from ui import Text


class TextBox:
    position: tuple[int, int]
    size: tuple[int, int]
    text: Text
    color: tuple[int, int, int]
    padding: int

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        text: str,
        text_color: tuple[int, int, int] = (0, 0, 0),
        text_font: tuple[str, bool] = ("Arial", True),
        color: tuple[int, int, int] = (255, 255, 255),
        padding: int = 0,
    ):
        self.position = position
        self.size = size
        self.color = color
        self.padding = padding
        self.text = Text(
            text,
            size[1] - 2 * padding,
            text_color,
            text_font[1],
            text_font[0],
        )

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.position + self.size)
        surface.blit(
            self.text.render(),
            (self.position[0] + self.padding, self.position[1] + self.padding),
        )
