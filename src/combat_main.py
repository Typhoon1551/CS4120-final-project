import pygame
import pygame_gui

import common
from character import Character


def combat_main(display: pygame.Surface, player: Character, enemy: Character):

    ### pygame stuff ###
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

    ### Combat initialization ###
    for item in player.inventory:
        if not item.active:
            item.effect(player, enemy, item)

    for item in enemy.inventory:
        if not item.active:
            item.effect(enemy, player, item)

    player_turn = True

    ### UI Elements ###

    ### main loop ###
    while running:

        if player_turn:
            player_item_buttons = []
            for i in range(len(player.inventory)):
                item = player.inventory[i]
                if item.active:
                    player_item_buttons.append(
                        pygame_gui.elements.UIButton(
                            pygame.Rect(
                                window_width / 2,
                                (window_height / 12 * (i + 1)),
                                window_width * (2 / 5),
                                window_height / 13,
                            ),
                            item.name,
                            manager,
                            command=lambda: item.effect(player, enemy, item),
                        )
                    )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                result = "quit"
                running = False
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exit_button:
                    result = "quit"
                    running = "false"

            manager.process_events(event)

        delta_time = clock.tick(common.FPS) / 1000

        ### UI Updates ###
        manager.update(delta_time)

        display.blit(background, (0, 0))
        manager.draw_ui(display)

        pygame.display.update()

    return result
