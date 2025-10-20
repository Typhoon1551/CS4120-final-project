# external imports
import pygame
import pygame.locals
import sys

# internal imports
import items
import character
import combat_main


def main():
    pygame.init()
    display_size = pygame.display.Info()
    display = pygame.display.set_mode(
        (display_size.current_w, display_size.current_h)
    )

    while True:
        display.fill((225, 225, 225))

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            combat_main.combat_main(display, None, None)

        if key[pygame.K_UP] or key[pygame.K_w]:
            character.Character.character_design["top"] -= 10
        elif key[pygame.K_DOWN] or key[pygame.K_s]:
            character.Character.character_design["top"] += 10
        elif key[pygame.K_LEFT] or key[pygame.K_a]:
            character.Character.character_design["left"] -= 10
        elif key[pygame.K_RIGHT] or key[pygame.K_d]:
            character.Character.character_design["left"] += 10

        characterbuild = character.Character.character_design

        pygame.draw.rect(
            display,
            characterbuild["color"],
            pygame.Rect(
                characterbuild["left"],
                characterbuild["top"],
                int(characterbuild["width"]),
                int(characterbuild["height"]),
            ),
        )

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    main()
