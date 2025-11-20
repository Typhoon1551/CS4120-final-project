import pygame

import common
from character import Character
import combat.ui as ui


def combat_main(display: pygame.Surface, player: Character, enemy: Character):

    ### pygame stuff ###
    window_width = display.get_size()[0]
    window_height = display.get_size()[1]

    background = pygame.Surface((window_width, window_height))
    background.fill((150, 150, 150))

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

    ### main loop ###
    while running:
        display.blit(background, (0, 0))

        if exit_button.is_pressed():
            running = False
        exit_button.render(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                result = "quit"
                running = False

        delta_time = clock.tick(common.FPS) / 1000

        ### UI Updates ###
        pygame.display.update()

    return result
