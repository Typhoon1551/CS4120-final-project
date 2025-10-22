import pygame
import pygame_gui

import common
from character import Character


def combat_main(display: pygame.Surface, player: Character, enemy: Character):

    # pygame stuff
    window_width = display.get_size()[0]
    window_height = display.get_size()[1]

    background = pygame.Surface((window_width, window_height))
    background.fill((150, 150, 150))

    manager = pygame_gui.UIManager((window_width, window_height))

    running = True
    clock = pygame.time.Clock()

    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(100, 100, 200, 100),
        text="Exit",
        manager=manager,
    )

    result = ""

    # Combat initialization
    for item in player.items:
        if not item.active:
            item.effect(player, enemy, item)

    for item in enemy.items:
        if not item.active:
            item.effect(enemy, player, item)

    player_turn = True

    # UI Elements
    player_item_select = pygame_gui.elements.UISelectionList(
        relative_rect=pygame.Rect(
            window_width * (1 / 10),
            window_height / 2,
            window_width * (8 / 10),
            window_height * (4 / 10),
        ),
        manager=manager,
        item_list=[],
    )

    # main loop
    while running:

        if player_turn:
            player_item_buttons = []
            for item in player.items:
                if not item.active:
                    continue
                player_item_buttons.append(
                    pygame_gui.elements.UIButton(
                        pygame.Rect(
                            0,
                            0,
                            window_width * (7 / 10),
                            window_height * (1 / 10),
                        ),
                        text=item.name,
                        manager=manager,
                    )
                )

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    result = "QUIT"
                    running = False
                case pygame_gui.UI_BUTTON_PRESSED:
                    match event.ui_element:
                        case exit_button:
                            result = "QUIT"
                            running = False

            manager.process_events(event)

        delta_time = clock.tick(common.FPS) / 1000
        manager.update(delta_time)

        display.blit(background, (0, 0))
        manager.draw_ui(display)

        pygame.display.update(common.FPS)

    return result
