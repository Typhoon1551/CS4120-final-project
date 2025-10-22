import pygame
import pygame_gui
import common


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

    result = ""

    while running:
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

        pygame.display.update()

    return result
