import pygame
import random
from typing import List, Tuple

TILE_SIZE: int = 64
T_EMPTY: int = 0
T_WALL: int = 1

COLOR_WATER_BG = (18, 28, 38)        
COLOR_PIPE_WALL = (180, 190, 200)    
COLOR_PIPE_OUTLINE = (130, 140, 150) 


DRAIN_CHAMBER_ROWS = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,1],  
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1],  
    [1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,0,1,1,0,1,1,1,1],  
    [1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1],  
    [1,0,1,1,1,0,1,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0],  
    [1,0,1,1,1,0,1,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0],  
    [1,0,1,0,0,0,1,0,1,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1],  
    [1,0,1,1,1,0,1,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,1],  
    [1,0,1,0,0,0,1,1,0,1,0,1,0,1,1,1,0,0,0,1,0,0,0,1], 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

MAP_H_TILES = len(DRAIN_CHAMBER_ROWS)
MAP_W_TILES = len(DRAIN_CHAMBER_ROWS[0])
MAP_W_PX = MAP_W_TILES * TILE_SIZE

MAP_H_PX = MAP_H_TILES * TILE_SIZE

PORTAL_TILES: List[Tuple[int, int]] = []
for r in range(MAP_H_TILES):
    for c in range(MAP_W_TILES):
        if DRAIN_CHAMBER_ROWS[r][c] == T_EMPTY and (
            r == 0 or r == MAP_H_TILES - 1 or c == 0 or c == MAP_W_TILES - 1
        ):
            PORTAL_TILES.append((r, c))


def random_portal(exclude_idx: int | None = None) -> tuple[int, tuple[int, int]]:
    idxs = list(range(len(PORTAL_TILES)))
    if exclude_idx is not None and exclude_idx in idxs and len(idxs) > 1:
        idxs.remove(exclude_idx)
    idx = random.choice(idxs)
    pr, pc = PORTAL_TILES[idx]
    cx = pc * TILE_SIZE + TILE_SIZE // 2
    cy = pr * TILE_SIZE + TILE_SIZE // 2
    return idx, (cx, cy)


def maybe_trigger_portal(player_rect: pygame.Rect, move_vec: tuple[int, int]) -> tuple[int, int] | None:
    dx, dy = move_vec
    if dx == 0 and dy == 0:
        return None

    r = max(0, min(MAP_H_TILES - 1, player_rect.centery // TILE_SIZE))
    c = max(0, min(MAP_W_TILES - 1, player_rect.centerx // TILE_SIZE))

    if (r, c) not in PORTAL_TILES:
        return None

    pushing_out = (
        (c == 0 and dx < 0) or
        (c == MAP_W_TILES - 1 and dx > 0) or
        (r == 0 and dy < 0) or
        (r == MAP_H_TILES - 1 and dy > 0)
    )
    if not pushing_out:
        return None

    try:
        idx = PORTAL_TILES.index((r, c))
    except ValueError:
        idx = None

    _idx, dest = random_portal(exclude_idx=idx)
    return dest

Rect = pygame.Rect

def rect_collides_walls(rect: Rect) -> bool:
    left_tile   = max(0, rect.left  // TILE_SIZE)
    right_tile  = min(MAP_W_TILES - 1, max(0, (rect.right  - 1) // TILE_SIZE))
    top_tile    = max(0, rect.top   // TILE_SIZE)
    bottom_tile = min(MAP_H_TILES - 1, max(0, (rect.bottom - 1) // TILE_SIZE))
    for r in range(top_tile, bottom_tile + 1):
        for c in range(left_tile, right_tile + 1):
            if DRAIN_CHAMBER_ROWS[r][c] == T_WALL:
                tile_rect = Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if rect.colliderect(tile_rect):
                    return True
    return False

def try_move(rect: Rect, dx: int, dy: int) -> Rect:
    r = rect.move(dx, 0)
    if not rect_collides_walls(r):
        rect = r
    r = rect.move(0, dy)
    if not rect_collides_walls(r):
        rect = r
    rect.left = max(0, min(rect.left, MAP_W_PX - rect.width))
    rect.top  = max(0, min(rect.top,  MAP_H_PX - rect.height))
    return rect

def get_camera_offset(player_rect: Rect, screen_w: int, screen_h: int) -> Tuple[int, int]:
    cam_x = player_rect.centerx - screen_w // 2
    cam_y = player_rect.centery - screen_h // 2
    cam_x = max(0, min(cam_x, max(0, MAP_W_PX - screen_w)))
    cam_y = max(0, min(cam_y, max(0, MAP_H_PX - screen_h)))
    return cam_x, cam_y

def draw_drain_chamber(surface: pygame.Surface, cam_off: Tuple[int, int]) -> None:
    cam_x, cam_y = cam_off
    sw, sh = surface.get_size()

    surface.fill(COLOR_WATER_BG)

    first_col = max(0, cam_x // TILE_SIZE)
    last_col  = min(MAP_W_TILES, (cam_x + sw) // TILE_SIZE + 1)
    first_row = max(0, cam_y // TILE_SIZE)
    last_row  = min(MAP_H_TILES, (cam_y + sh) // TILE_SIZE + 1)

    for r in range(first_row, last_row):
        for c in range(first_col, last_col):
            if DRAIN_CHAMBER_ROWS[r][c] == T_WALL:
                rx = c * TILE_SIZE - cam_x
                ry = r * TILE_SIZE - cam_y
                rect = Rect(rx, ry, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(surface, COLOR_PIPE_WALL, rect)
                pygame.draw.rect(surface, COLOR_PIPE_OUTLINE, rect, width=2)

def get_safe_start_rect(width: int = 40, height: int = 24) -> Rect:
    spawn_r, spawn_c = 5, 2  
    if DRAIN_CHAMBER_ROWS[spawn_r][spawn_c] != T_EMPTY:
        for rr in range(1, MAP_H_TILES - 1):
            for cc in range(1, MAP_W_TILES - 1):
                if DRAIN_CHAMBER_ROWS[rr][cc] == T_EMPTY:
                    spawn_r, spawn_c = rr, cc
                    break
            else:
                continue
            break
    x = spawn_c * TILE_SIZE + (TILE_SIZE - width) // 2
    y = spawn_r * TILE_SIZE + (TILE_SIZE - height) // 2
    return Rect(x, y, width, height)



def get_world_size_px() -> Tuple[int, int]:
    return MAP_W_PX, MAP_H_PX


class Debris:
    def __init__(self, x, y, w, h, vx, vy):
        self.rect = pygame.Rect(x, y, w, h)
        self.vx, self.vy = vx, vy

    def step(self):
        nxt = self.rect.move(self.vx, 0)
        if not rect_collides_walls(nxt): self.rect = nxt
        else: self.vx = -self.vx
        nxt = self.rect.move(0, self.vy)
        if not rect_collides_walls(nxt): self.rect = nxt
        else: self.vy = -self.vy

    def draw(self, surf, cam_off):
        r = self.rect.move(-cam_off[0], -cam_off[1])
        pygame.draw.rect(surf, (210,220,230), r)

DEBRIS = []

def tile_center(r: int, c: int) -> tuple[int, int]:
    return (c * TILE_SIZE + TILE_SIZE // 2, r * TILE_SIZE + TILE_SIZE // 2)

def init_debris(n=8):
    import random
    DEBRIS.clear()
    for _ in range(n):
        for _attempt in range(80):
            r = random.randrange(1, MAP_H_TILES-1)
            c = random.randrange(1, MAP_W_TILES-1)
            if DRAIN_CHAMBER_ROWS[r][c] == T_EMPTY:
                cx, cy = tile_center(r, c)
                w, h = 20, 12
                vx = random.choice([-2, -1, 1, 2])
                vy = random.choice([-2, -1, 1, 2])
                rect = pygame.Rect(cx - w//2, cy - h//2, w, h)
                if not rect_collides_walls(rect):
                    DEBRIS.append(Debris(rect.left, rect.top, w, h, vx, vy))
                    break

def update_and_draw_debris(surf, cam_off):
    for d in DEBRIS:
        d.step()
        d.draw(surf, cam_off)
def spawn_debris_near(cx: int, cy: int, count: int = 3):
    for _ in range(count):
        w, h = 18, 10
        rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
        if not rect_collides_walls(rect):
            vx = random.choice([-2, -1, 1, 2])
            vy = random.choice([-2, -1, 1, 2])
            DEBRIS.append(Debris(rect.left, rect.top, w, h, vx, vy))


FLOW: dict[tuple[int, int], tuple[float, float]] = {}


def set_flow_tile(r: int, c: int, fx: float, fy: float) -> None:
    if 0 <= r < MAP_H_TILES and 0 <= c < MAP_W_TILES and DRAIN_CHAMBER_ROWS[r][c] == T_EMPTY:
        FLOW[(r, c)] = (fx, fy)


def set_flow_rect(r0: int, c0: int, r1: int, c1: int, fx: float, fy: float) -> None:
    r0, r1 = sorted((max(0, r0), min(MAP_H_TILES - 1, r1)))
    c0, c1 = sorted((max(0, c0), min(MAP_W_TILES - 1, c1)))
    for rr in range(r0, r1 + 1):
        for cc in range(c0, c1 + 1):
            if DRAIN_CHAMBER_ROWS[rr][cc] == T_EMPTY:
                FLOW[(rr, cc)] = (fx, fy)


def clear_flow() -> None:
    FLOW.clear()


def flow_at(x: int, y: int) -> tuple[float, float]:
    r = max(0, min(MAP_H_TILES - 1, y // TILE_SIZE))
    c = max(0, min(MAP_W_TILES - 1, x // TILE_SIZE))
    return FLOW.get((r, c), (0.0, 0.0))
