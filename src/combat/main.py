import pygame

import common
from character import Character
import ui


def combat_main(display: pygame.Surface, player: Character, enemy: Character):

    ### pygame stuff ###
    window_width = display.get_size()[0]
    window_height = display.get_size()[1]

    background = pygame.Surface((window_width, window_height))
    background.fill((135, 206, 235))

    running = True
    clock = pygame.time.Clock()

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
    exit_button = ui.Button(
        (20, 20),
        (100, 50),
        "EXIT",
        color=(255, 0, 0),
        padding=10,
    )

    inventory_title = ui.Button(
        (window_width // 2, 20),
        (window_width // 2 - 20, 80),
        "Which item to use?",
        color=(230, 230, 230),
        padding=15,
    )

    ### main loop ###
    while running:
        display.blit(background, (0, 0))

        ### Exit Button ###
        if exit_button.hovered():
            exit_button.color = (255, 0, 0)
        else:
            exit_button.color = (255, 255, 255)

        if exit_button.pressed():
            running = False

        ### Inventory ###
        inventory_buttons = []
        for i in range(len(player.inventory)):
            inventory_buttons.append(
                ui.Button(
                    (window_width // 2, 120 + 100 * i),
                    (window_width // 2 - 20, 80),
                    player.inventory[i].name,
                    color=(200, 200, 200),
                    padding=15,
                    id=i,
                )
            )

        for i in inventory_buttons:
            if i.hovered():
                i.color = (150, 150, 150)
            else:
                i.color = (200, 200, 200)

            if i.pressed():
                player.inventory[i.id].effect(
                    player, enemy, player.inventory[i.id]
                )

        ### Render Elements ###
        exit_button.render(display)
        if player_turn:
            inventory_title.render(display)
            for i in inventory_buttons:
                i.render(display)

        ### Event Handling ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                result = "quit"
                running = False

        clock.tick(common.FPS)

        pygame.display.update()

    return result
