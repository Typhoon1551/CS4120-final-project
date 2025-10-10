# external imports
import pygame
import pygame.locals
import sys

# internal imports
import items
import character


def main():
    pygame.init()

    display = pygame.display.set_mode((400, 600))

    while True:
        display.fill((255, 0, 255))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
