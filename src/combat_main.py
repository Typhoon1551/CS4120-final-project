import pygame
import pygame_gui


def combat_main(display: pygame.Surface, player, enemy):
    background = pygame.Surface(display.get_size())
    background.fill((150, 150, 150))

    manager = pygame_gui.UIManager(display.get_size())

    running = True
    clock = pygame.time.Clock()

    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(100, 100, 200, 100),
        text="Exit",
        manager=manager,
    )

    while running:
        for event in pygame.event.get():
            manager.process_events(event)

        delta_time = clock.tick(60) / 1000
        manager.update(delta_time)

        display.blit(background, (0, 0))
        manager.draw_ui(display)

        pygame.display.update()
