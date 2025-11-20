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


class Button:
    position: tuple[int, int]
    size: tuple[int, int]
    icon: None
    text: Text
    id: Any | None
    color: tuple[int, int, int]
    hold: bool
    padding: int

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        text: str,
        text_color: tuple[int, int, int] = (0, 0, 0),
        text_font: tuple[str, bool] = ("Arial", True),
        id: Any | None = None,
        color: tuple[int, int, int] = (255, 255, 255),
        hold: bool = False,
        padding: int = 0,
    ):
        self.position = position
        self.size = size
        self.id = id
        self.color = color
        self.hold = hold
        self.padding = padding
        self.text = Text(
            text,
            size[1] - 2 * padding,
            text_color,
            text_font[1],
            text_font[0],
        )

    def is_pressed(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()

        check_x = (
            mouse_pos[0] >= self.position[0]
            and mouse_pos[0] <= self.position[0] + self.size[0]
        )

        check_y = (
            mouse_pos[1] >= self.position[1]
            and mouse_pos[1] <= self.position[1] + self.size[1]
        )

        if not self.hold:
            mouse_pressed = pygame.mouse.get_just_pressed()[0]
        else:
            mouse_pressed = pygame.mouse.get_pressed()[0]

        return check_x and check_y and mouse_pressed

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.position + self.size)
        surface.blit(
            self.text.render(),
            (self.position[0] + self.padding, self.position[1] + self.padding),
        )
