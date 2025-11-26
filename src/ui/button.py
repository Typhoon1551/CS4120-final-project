from typing import Any

import pygame
from pygame.typing import ColorLike

import ui


class Button:
    position: tuple[int, int]
    size: tuple[int, int]
    icon: None
    id: Any | None
    text: str
    padding: int
    font_color: tuple[int, int, int]
    font_family: tuple[str, bool]

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        text: str,
        text_color: tuple[int, int, int] = (0, 0, 0),
        text_font: tuple[str, bool] = ("Arial", True),
        id: Any | None = None,
        color: tuple[int, int, int] = (255, 255, 255),
        padding: int = 0,
    ):
        self.position = position
        self.size = size
        self.id = id
        self.color = color
        self.padding = padding
        self.font_color = text_color
        self.font_family = text_font
        self.text = text

    def pressed(self) -> bool:
        return self.hovered() and pygame.mouse.get_just_pressed()[0]

    def held(self) -> bool:
        return self.hovered() and pygame.mouse.get_pressed()[0]

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.position + self.size)
        surface.blit(
            ui.draw_text(
                self.text,
                self.size[0] - self.padding * 2,
                self.size[1] - self.padding * 2,
                color=(0, 0, 0),
            ),
            (self.position[0] + self.padding, self.position[1] + self.padding),
        )

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
