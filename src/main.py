# external imports
import pygame
import pygame.locals
import sys

# internal imports
import items
import character
def draw_player(characterbuild,display):
    pygame.draw.rect(
            display,
            characterbuild["color"],
            pygame.Rect(characterbuild["left"],characterbuild["top"],int(characterbuild["width"]),int(characterbuild["height"])),
            border_radius=5
            )
    pygame.draw.polygon(
        display,
        characterbuild["color"],
        ((characterbuild["left"]+characterbuild["width"]-5,characterbuild["top"]),(characterbuild["left"]+characterbuild["width"]-5,characterbuild["top"]+characterbuild["height"]),(characterbuild["left"]+(characterbuild["width"]*2-5),characterbuild["top"]+(characterbuild["height"]/2)))
    )
    pygame.draw.polygon(
        display,
        characterbuild["color"],
        ((characterbuild["left"]-characterbuild["width"]+10,characterbuild["top"]),(characterbuild["left"]-characterbuild["width"]+10,characterbuild["top"]+characterbuild["height"]),(characterbuild["left"]+10,characterbuild["top"]+(characterbuild["height"]/2)))
    )
    pygame.draw.circle(
        display,
        (225,0,225),
        (characterbuild["left"]+(characterbuild["width"]*0.75),characterbuild["top"]+(characterbuild["height"]*0.25)),
        characterbuild["width"]*0.1
    )

def main():
    pygame.init()
    display_size=pygame.display.Info()
    display = pygame.display.set_mode((display_size.current_w, display_size.current_h))

    while True:
        display.fill((225, 225, 225))

        key = pygame.key.get_pressed()
        if key[pygame.K_UP]==True or key[pygame.K_w] == True:
            character.Character.character_design["top"]-=10
        if key[pygame.K_DOWN]==True or key[pygame.K_s] == True:
            character.Character.character_design["top"]+=10
        if key[pygame.K_LEFT]==True or key[pygame.K_a] == True:
            character.Character.character_design["left"]-=10
        if key[pygame.K_RIGHT]==True or key[pygame.K_d] == True:
            character.Character.character_design["left"]+=10
        
        characterbuild = character.Character.character_design
        draw_player(characterbuild,display)
        
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()



if __name__ == "__main__":
    main()
