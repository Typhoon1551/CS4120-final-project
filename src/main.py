# external imports
import pygame
import pygame.locals
import sys

# internal imports
import items
import character
import combat_main
from adventure import story

def draw_player(characterbuild, display):
    left   = int(characterbuild["left"])
    top    = int(characterbuild["top"])
    width  = int(characterbuild["width"])
    height = int(characterbuild["height"])
    color  = characterbuild["color"]
    facing = characterbuild.get("facing", "R")

    body = pygame.Rect(left, top, width, height)
    pygame.draw.rect(display, color, body, border_radius=5)

    nose_R = ((left + width - 5, top),
              (left + width - 5, top + height),
              (left + (width * 2 - 5), top + (height // 2)))
    tail_R = ((left - width + 10, top),
              (left - width + 10, top + height),
              (left + 10, top + (height // 2)))

    cx = left + width // 2
    cy = top  + height // 2

    def mirror_x(poly):
        return tuple((2*cx - x, y) for (x, y) in poly)

    def rotate90(poly):
        return tuple((cx + (y - cy), cy - (x - cx)) for (x, y) in poly)

    if facing == "R":
        nose, tail = nose_R, tail_R
        eye = (left + int(width * 0.75), top + int(height * 0.25))
    elif facing == "L":
        nose, tail = mirror_x(nose_R), mirror_x(tail_R)
        eye = (left + int(width * 0.25), top + int(height * 0.25))
    elif facing == "U":
        nose, tail = rotate90(nose_R), rotate90(tail_R)
        eye = (left + int(width * 0.25), top + int(height * 0.25))
    else:  
        nose, tail = rotate90(rotate90(rotate90(nose_R))), rotate90(rotate90(rotate90(tail_R)))
        eye = (left + int(width * 0.25), top + int(height * 0.75))

    pygame.draw.polygon(display, color, nose)
    pygame.draw.polygon(display, color, tail)
    pygame.draw.circle(display, (225, 0, 225), (int(eye[0]), int(eye[1])), int(width * 0.1))

def main():
    pygame.init()
    display_size = pygame.display.Info()
    display = pygame.display.set_mode((display_size.current_w, display_size.current_h))
    story.clear_flow()

    story.set_flow_rect(2, 0, 3, 15, 2.0, 0.0)
    story.set_flow_rect(4, 15, 5, 16, 0.0, 1.8)
    story.set_flow_rect(6, 16, 7, 23, 2.2, 0.0)

    story.set_flow_rect(0, 7, 1, 7, 0.0, 1.6)
    story.set_flow_rect(8, 19, 10, 19, 0.0, -1.4)

    story.set_flow_rect(5, 1, 5, 5, 1.2, 0.0)
    story.set_flow_rect(6, 1, 7, 1, 0.0, -1.2)

    story.set_flow_rect(4, 10, 10, 10, 0.0, -1.3)
    story.set_flow_rect(6, 13, 7, 15, 1.0, 0.0)

    story.set_flow_rect(9, 15, 9, 16, 1.0, 0.0)
    story.set_flow_rect(7, 8, 7, 10, 1.0, 0.0)

    tilesw = 3
    tilesh = 3
    veiw_w = tilesw * story.TILE_SIZE
    veiwh = tilesh * story.TILE_SIZE

    render_surf = pygame.Surface((veiw_w, veiwh)).convert()
    spawn = story.get_safe_start_rect(
        width=int(character.Character.character_design["width"]),
        height=int(character.Character.character_design["height"])
    )
    cd = character.Character.character_design
    cd["left"], cd["top"] = spawn.left, spawn.top
    cd.setdefault("facing", "R")
    vis_rect = pygame.Rect(
        character.Character.character_design["left"],
        character.Character.character_design["top"],
        character.Character.character_design["width"],
        character.Character.character_design["height"]
    )
    story.init_debris(6)
    story.spawn_debris_near(vis_rect.centerx, vis_rect.centery, 3)
    pygame.font.init()
    _hud_font = pygame.font.SysFont(None, 22)
    _help_ticks = 500 
    _hit_cooldown = 0  
    while True:
        key = pygame.key.get_pressed()
        dx = dy = 0
        speed = 6
        if key[pygame.K_UP] or key[pygame.K_w]:
            dy -= speed
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            dy += speed
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            dx -= speed
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            dx += speed
        if _hit_cooldown > 0:
            _hit_cooldown -= 1

        cd = character.Character.character_design
        vis_rect = pygame.Rect(int(cd["left"]), int(cd["top"]),
                               int(cd["width"]), int(cd["height"]))
        phys_rect = vis_rect.inflate(-int(vis_rect.width * 0.30),
                                     -int(vis_rect.height * 0.20))
        phys_rect.center = vis_rect.center

        fx, fy = story.flow_at(phys_rect.centerx, phys_rect.centery)
        mdx = dx + int(round(fx))
        mdy = dy + int(round(fy))

        if mdx == 0 and mdy == 0 and (fx or fy):
            nudge_x = 1 if fx > 0 else -1 if fx < 0 else 0
            nudge_y = 1 if fy > 0 else -1 if fy < 0 else 0
            test = phys_rect.move(nudge_x, 0)
            if not story.rect_collides_walls(test):
                phys_rect = test
            test = phys_rect.move(0, nudge_y)
            if not story.rect_collides_walls(test):
                phys_rect = test
            vis_rect.center = phys_rect.center
            cd["left"], cd["top"] = vis_rect.left, vis_rect.top

        if mdx or mdy:
            phys_rect = story.try_move(phys_rect, mdx, mdy)
            vis_rect.center = phys_rect.center
            cd["left"], cd["top"] = vis_rect.left, vis_rect.top
        if mdx or mdy:
            if abs(mdx) >= abs(mdy):
                cd["facing"] = "R" if mdx > 0 else "L"
            else:
                cd["facing"] = "D" if mdy > 0 else "U"
        else:
            cd.setdefault("facing", "R")
        dest = story.maybe_trigger_portal(phys_rect, (mdx, mdy))
        if dest is not None:
            phys_rect.center = dest
            vis_rect.center  = dest
            cd["left"], cd["top"] = vis_rect.left, vis_rect.top
        cam_off = story.get_camera_offset(phys_rect, veiw_w, veiwh)

        story.draw_drain_chamber(render_surf, cam_off)
        story.update_and_draw_debris(render_surf, cam_off)

        screen_space_cd = dict(cd)
        screen_space_cd["left"] = cd["left"] - cam_off[0]
        screen_space_cd["top"]  = cd["top"]  - cam_off[1]
        draw_player(screen_space_cd, render_surf)  
        for d in story.DEBRIS:
            if phys_rect.colliderect(d.rect):
                if _hit_cooldown == 0:
                    if getattr(character.Character, "current_health", 0) <= 0:
                        character.Character.current_health = 10  
                    character.Character.current_health = max(0, character.Character.current_health - 1)
                    phys_rect = story.try_move(phys_rect, -4 if mdx >= 0 else 4, -4 if mdy >= 0 else 4)
                    vis_rect.center = phys_rect.center
                    cd["left"], cd["top"] = vis_rect.left, vis_rect.top
                    _hit_cooldown = 45  
                break

        pygame.transform.scale(render_surf, display.get_size(), display)

        if _help_ticks > 0:
            if any(key[i] for i in range(len(key))):
                _help_ticks = 0
            else:
                overlay = pygame.Surface(display.get_size(), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 90))
                font = pygame.font.SysFont(None, 28)
                lines = [
                    "WASD / Arrows to swim",
                    "Portals: push into a hole on the outer wall",
                    "Debris = small damage (has cooldown)"
                ]
                y = 20
                for ln in lines:
                    txt = font.render(ln, True, (235, 245, 255))
                    overlay.blit(txt, (20, y))
                    y += 32
                display.blit(overlay, (0, 0))
                _help_ticks -= 1

        if key[pygame.K_SPACE]:
            combat_main.combat_main(display, None, None)


        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()


if __name__ == "__main__":
    main()
