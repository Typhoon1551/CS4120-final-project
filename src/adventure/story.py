import pygame
import random
from typing import List, Tuple

TILE_SIZE: int = 64
T_EMPTY: int = 0
T_WALL: int = 1
T_ENEMY: int = 2

COLOR_WATER_BG = (18, 28, 38)
COLOR_PIPE_WALL = (180, 190, 200)
COLOR_PIPE_OUTLINE = (130, 140, 150)
COLOR_PORTAL_TILE = (68, 28, 38)


DRAIN_CHAMBER_ROWS = [
	# 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23
	[
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
	],  # 0
	[
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		0,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		1,
	],  # 1
	[
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		1,
		1,
		1,
		0,
		1,
		1,
		1,
		1,
	],  # 2
	[
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		1,
		1,
		0,
		1,
		1,
		1,
		1,
	],  # 3
	[
		1,
		1,
		1,
		1,
		1,
		0,
		1,
		1,
		1,
		1,
		0,
		1,
		1,
		1,
		1,
		0,
		0,
		1,
		1,
		2,
		1,
		1,
		1,
		1,
	],  # 4
	[
		1,
		0,
		0,
		0,
		0,
		0,
		1,
		1,
		1,
		1,
		0,
		1,
		1,
		1,
		1,
		0,
		0,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
	],  # 5
	[
		1,
		0,
		1,
		1,
		1,
		0,
		1,
		1,
		1,
		1,
		0,
		1,
		0,
		0,
		0,
		1,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
	],  # 6
	[
		1,
		0,
		1,
		1,
		1,
		0,
		1,
		0,
		0,
		0,
		0,
		1,
		0,
		1,
		0,
		1,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
		0,
	],  # 7
	[
		1,
		0,
		1,
		0,
		0,
		0,
		1,
		0,
		1,
		1,
		0,
		1,
		0,
		1,
		0,
		1,
		1,
		1,
		0,
		1,
		1,
		1,
		0,
		1,
	],  # 8
	[
		1,
		0,
		1,
		1,
		1,
		0,
		1,
		0,
		0,
		1,
		0,
		1,
		0,
		1,
		0,
		0,
		0,
		1,
		0,
		1,
		0,
		1,
		0,
		1,
	],  # 9
	[
		1,
		0,
		1,
		2,
		0,
		0,
		1,
		1,
		2,
		1,
		0,
		1,
		0,
		1,
		1,
		1,
		0,
		0,
		0,
		1,
		0,
		0,
		0,
		1,
	],  # 10
	[
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
		1,
	],  # 11
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
	for c in range(MAP_W_TILES):
		if DRAIN_CHAMBER_ROWS[r][c] == T_EMPTY and (
			r == 0 or r == MAP_H_TILES - 1 or c == 0 or c == MAP_W_TILES - 1
		):
			PORTAL_TILES.append((r, c))
# print(PORTAL_TILES)


def random_portal(
	exclude_idx: int | None = None,
) -> tuple[int, tuple[int, int]]:
	idxs = list(range(len(PORTAL_TILES)))
	if exclude_idx is not None and exclude_idx in idxs and len(idxs) > 1:
		idxs.remove(exclude_idx)
	idx = random.choice(idxs)
	pr, pc = PORTAL_TILES[idx]
	cx = pc * TILE_SIZE + TILE_SIZE // 2
	cy = pr * TILE_SIZE + TILE_SIZE // 2
	return idx, (cx, cy)


def maybe_trigger_portal(
	player_rect: pygame.Rect, move_vec: tuple[int, int]
) -> tuple[int, int] | None:
	dx, dy = move_vec
	if dx == 0 and dy == 0:
		return None

	r = max(0, min(MAP_H_TILES - 1, player_rect.centery // TILE_SIZE))
	c = max(0, min(MAP_W_TILES - 1, player_rect.centerx // TILE_SIZE))

	if (r, c) not in PORTAL_TILES:
		return None

	pushing_out = (
		(c == 0 and dx < 0)
		or (c == MAP_W_TILES - 1 and dx > 0)
		or (r == 0 and dy < 0)
		or (r == MAP_H_TILES - 1 and dy > 0)
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
	left_tile = max(0, rect.left // TILE_SIZE)
	right_tile = min(MAP_W_TILES - 1, max(0, (rect.right - 1) // TILE_SIZE))
	top_tile = max(0, rect.top // TILE_SIZE)
	bottom_tile = min(MAP_H_TILES - 1, max(0, (rect.bottom - 1) // TILE_SIZE))
	for r in range(top_tile, bottom_tile + 1):
		for c in range(left_tile, right_tile + 1):
			if DRAIN_CHAMBER_ROWS[r][c] == T_WALL:
				tile_rect = Rect(
					c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE
				)
				if rect.colliderect(tile_rect):
					return True
	return False


def is_enemey(rect: Rect) -> bool:
	left_tile = max(0, rect.left // TILE_SIZE)
	right_tile = min(MAP_W_TILES - 1, max(0, (rect.right - 1) // TILE_SIZE))
	top_tile = max(0, rect.top // TILE_SIZE)
	bottom_tile = min(MAP_H_TILES - 1, max(0, (rect.bottom - 1) // TILE_SIZE))
	for r in range(top_tile, bottom_tile + 1):
		for c in range(left_tile, right_tile + 1):
			if DRAIN_CHAMBER_ROWS[r][c] == T_ENEMY:
				tile_rect = Rect(
					c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE
				)
				if rect.colliderect(tile_rect):
					return True
	return False


def remove_enemy(rect: Rect) -> bool:
	left_tile = max(0, rect.left // TILE_SIZE)
	right_tile = min(MAP_W_TILES - 1, max(0, (rect.right - 1) // TILE_SIZE))
	top_tile = max(0, rect.top // TILE_SIZE)
	bottom_tile = min(MAP_H_TILES - 1, max(0, (rect.bottom - 1) // TILE_SIZE))
	for r in range(top_tile, bottom_tile + 1):
		for c in range(left_tile, right_tile + 1):
			if DRAIN_CHAMBER_ROWS[r][c] == T_ENEMY:
				tile_rect = Rect(
					c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE
				)
				if rect.colliderect(tile_rect):
					DRAIN_CHAMBER_ROWS[r][c] = T_EMPTY


R = 0


def try_move(rect: Rect, dx: int, dy: int):
	try:
		R += 1
	except:
		R = 0
	zero = random.randint(-1, 1)
	if abs(dx) < 30 or abs(dy) < 30 and R < 100:
		r = rect.move(dx, dy)
		if not rect_collides_walls(r):
			rect = r
		else:
			rect = try_move(rect, (dx + zero) * (-4), (dy + zero) * (-4))
		"""r1 = rect.move(0, )
		if not rect_collides_walls(r1):
			rect = r1
		else:
			rect = try_move(rect,(dx+zero)*(4),dy*(-5))"""

		rect.left = max(0, min(rect.left, MAP_W_PX - rect.width))
		rect.top = max(0, min(rect.top, MAP_H_PX - rect.height))
	R = 0
	return rect


def get_camera_offset(
	player_rect: Rect, screen_w: int, screen_h: int
) -> Tuple[int, int]:
	cam_x = player_rect.centerx - screen_w // 2
	cam_y = player_rect.centery - screen_h // 2
	cam_x = max(0, min(cam_x, max(0, MAP_W_PX - screen_w)))
	cam_y = max(0, min(cam_y, max(0, MAP_H_PX - screen_h)))
	return cam_x, cam_y


def draw_drain_chamber(
	surface: pygame.Surface, cam_off: Tuple[int, int]
) -> None:
	cam_x, cam_y = cam_off
	sw, sh = surface.get_size()

	surface.fill(COLOR_WATER_BG)

	first_col = max(0, cam_x // TILE_SIZE)
	last_col = min(MAP_W_TILES, (cam_x + sw) // TILE_SIZE + 1)
	first_row = max(0, cam_y // TILE_SIZE)
	last_row = min(MAP_H_TILES, (cam_y + sh) // TILE_SIZE + 1)
	y_n = random.randint(0, 1)
	for r in range(first_row, last_row):
		for c in range(first_col, last_col):
			if DRAIN_CHAMBER_ROWS[r][c] == T_WALL:
				rx = c * TILE_SIZE - cam_x
				ry = r * TILE_SIZE - cam_y
				rect = Rect(rx, ry, TILE_SIZE, TILE_SIZE)
				pygame.draw.rect(surface, COLOR_PIPE_WALL, rect)
				pygame.draw.rect(surface, COLOR_PIPE_OUTLINE, rect, width=2)
			if DRAIN_CHAMBER_ROWS[r][c] == T_ENEMY:
				rx = c * TILE_SIZE - cam_x
				ry = r * TILE_SIZE - cam_y
				rect = Rect(rx, ry, TILE_SIZE, TILE_SIZE)
				pygame.draw.rect(surface, (0, 0, 0), rect)
			if (r, c) in PORTAL_TILES:
				rx = c * TILE_SIZE - cam_x
				ry = r * TILE_SIZE - cam_y
				rect = Rect(rx, ry, TILE_SIZE, TILE_SIZE)
				if y_n == 1:
					pygame.draw.rect(surface, COLOR_PORTAL_TILE, rect)
				else:
					pygame.draw.rect(surface, COLOR_WATER_BG, rect)


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
		if not rect_collides_walls(nxt):
			self.rect = nxt
		else:
			self.vx = -self.vx
		nxt = self.rect.move(0, self.vy)
		if not rect_collides_walls(nxt):
			self.rect = nxt
		else:
			self.vy = -self.vy

	def draw(self, surf, cam_off):
		r = self.rect.move(-cam_off[0], -cam_off[1])
		pygame.draw.rect(surf, (210, 220, 230), r)


DEBRIS = []


def tile_center(r: int, c: int) -> tuple[int, int]:
	return (c * TILE_SIZE + TILE_SIZE // 2, r * TILE_SIZE + TILE_SIZE // 2)


def init_debris(n=8):
	import random

	DEBRIS.clear()
	for _ in range(n):
		for _attempt in range(80):
			r = random.randrange(1, MAP_H_TILES - 1)
			c = random.randrange(1, MAP_W_TILES - 1)
			if DRAIN_CHAMBER_ROWS[r][c] == T_EMPTY:
				cx, cy = tile_center(r, c)
				w, h = 20, 12
				vx = random.choice([-2, -1, 1, 2])
				vy = random.choice([-2, -1, 1, 2])
				rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
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


FLOW: dict[tuple[int, int], tuple[float, float]] = {
	(2, 0): (3.0, 0.0), (2, 1): (2.0, 0.0), (2, 2): (2.0, 0.0), (2, 3): (2.0, 0.0), 
	(2, 4): (2.0, 0.0), (2, 5): (2.0, 0.5), (2, 6): (2.0, 0.0), (2, 7): (2.0, 1.2), 
	(2, 8): (2.0, 0.0), (2, 9): (2.0, 0.0), (2, 10): (2.0, 0.0), (2, 11): (2.0, 0.0), 
	(2, 12): (2.0, 0.0), (2, 13): (2.0, 0.0), (2, 14): (2.0, 0.0), (2, 15): (0.5, 2.5),(2,19):(0.0,-1.0),(3,19):(0.0,-5.0), 
	(3, 0): (3.0, 0.0), (3, 1): (2.0, 0.0), (3, 2): (2.0, 0.0), (3, 3): (2.0, 0.0), 
	(3, 4): (2.0, 0.0), (3, 5): (2.0, -2.0), (3, 6): (2.0, 0.0), (3, 7): (2.0, 0.0), (3, 8): (2.0, 0.0), 
	(3, 9): (2.0, 0.0), (3, 10): (2.0, 0.0), (3, 11): (2.0, 0.0), (3, 12): (2.0, 0.0), (3, 13): 
	(2.0, 0.0), (3, 14): (2.0, 0.0), (3, 15): (2.0, 1.0), (3, 16): (1.0, 2.0), (4, 15):(2.0,0.0),(4, 16): (0.2, 3.4), 
	(5, 16): (1.0, 3.0), (6, 16): (3.3, 2.0), (6, 17): (2.3, 0.0), (6, 18): (2.3, 0.0), (6, 19): 
	(2.3, 0.0), (6, 20): (2.3, 0.0), (6, 21): (2.3, 0.0), (6, 22): (2.3, 0.0), (6, 23): (3.3, 0.0), 
	(7, 16): (2.3, 0.0), (7, 17): (2.3, 0.0), (7, 18): (2.3, 0.0), (7, 19): (2.3, 0.0), (7, 20): 
	(2.3, 0.0), (7, 21): (2.3, 0.0), (7, 22): (2.3, 0.0), (7, 23): (3.3, 0.0), (1, 16): (-1.5, 0.0), 
	(1, 17): (-1.5, 0.0), (1, 18): (-1.5, 0.0), (1, 19): (-1.5, -1.5), (1, 20): (-1.5, 0.0), 
	(1, 21): (-1.5, 0.0), (1, 22): (-1.5, 0.0), (1, 15): (-0.8, 2.5), (1, 7): (0.0, 1.2), 
	(5, 1): (1.8, 0.0), (5, 2): (1.8, 0.0), (5, 3): (1.8, 0.0), (5, 4): (1.8, 0.0), (5, 5): (1.8, -0.8), 
	(4, 5): (-0.2, -1.4), (6, 5): (0.0, -1.4), (7, 5): (0.0, -1.4), (8, 5): (0.0, -1.4), 
	(9, 5): (0.0, -1.4), (10, 5): (0.0, -1.4), (4, 10): (0.0, -1.2), (5, 10): (0.0, -1.2), 
	(6, 10): (0.0, -1.2), (7, 10): (0.0, -1.2), (8, 10): (0.0, -1.2), (9, 10): (0.0, -1.2), 
	(10, 10): (0.0, -1.2), (6, 12): (1.4, 0.0), (6, 13): (1.4, 0.0), (6, 14): (1.4, 0.0), 
	(7, 14): (0.0, 1.0), (9, 15): (1.0, 0.0), (9, 16): (1.0, 0.0), (9, 1): (0.0, -1.0), 
	(10, 1): (0.0, -1.0), (10, 3): (1.0, 0.0), (10, 4): (1.0, 0.0), (10,8):(-10.0,-10.0),(9,8):(-1.0,-1.0)}


def clear_flow():
	FLOW.clear()


def set_flow_tile(r, c, fx, fy):
	if 0 <= r < MAP_H_TILES and 0 <= c < MAP_W_TILES:
		if DRAIN_CHAMBER_ROWS[r][c] == T_EMPTY:
			if (r, c) in FLOW:
				old = FLOW[(r, c)]
				FLOW[(r, c)] = (old[0] + fx, old[1] + fy)
			else:
				FLOW[(r, c)] = (fx, fy)


def set_flow_rect(r0, c0, r1, c1, fx, fy):
	r0, r1 = sorted((max(0, r0), min(MAP_H_TILES - 1, r1)))
	c0, c1 = sorted((max(0, c0), min(MAP_W_TILES - 1, c1)))
	for rr in range(r0, r1 + 1):
		for cc in range(c0, c1 + 1):
			if DRAIN_CHAMBER_ROWS[rr][cc] == T_EMPTY:
				if (rr, cc) in FLOW:
					old = FLOW[(rr, cc)]
					FLOW[(rr, cc)] = (old[0] + fx, old[1] + fy)
				else:
					FLOW[(rr, cc)] = (fx, fy)


def flow_at(x, y):
	r = max(0, min(MAP_H_TILES - 1, y // TILE_SIZE))
	c = max(0, min(MAP_W_TILES - 1, x // TILE_SIZE))
	return FLOW.get((r, c), (0.0, 0.0))


def setup_flow():
	"""
	clear_flow()
	# MAIN TRUNK — TOP HORIZONTAL
	# rows 2–3, cols 0–15: strong rightward flow
	set_flow_rect(2, 0, 3, 15, 2.0, 0.0)

	# MAIN TRUNK — VERTICAL DROP
	# column 16, rows 3–6: down into lower trunk
	# (this intersects tiles near the bend; overlap = diagonal)
	set_flow_rect(2, 16, 6, 16, 1.0, 2.0)

	# MAIN TRUNK — BOTTOM HORIZONTAL
	# rows 6–7, cols 16–23: main flow to the outlet
	set_flow_rect(6, 16, 7, 23, 2.3, 0.0)

	# TOP RESERVOIR POOL (row 1, cols 15–22)
	# Water drifts left into the junction, then drops down.
	set_flow_rect(1, 16, 1, 22, -1.5, 0.0)   # leftward along the top
	set_flow_rect(1, 15, 1, 15, -1.5, 1.5)   # at 1,15: left + down
	set_flow_rect(1, 15, 2, 15, -1.5, 1.5)   # at 1,15: left + down
	set_flow_rect(2, 15, 2, 15, 0.0, 1.5)    # at 2,15: reinforce downward into trunk

	# LITTLE INLET ON (1,7)
	# Feeds down into the top main.
	set_flow_rect(1, 7, 2, 7, 0.0, 1.2)

	# MID-LEFT BRANCH — HORIZONTAL (row 5, cols 1–5)
	# Gentle flow toward the junction at (5,5).
	set_flow_rect(5, 1, 5, 5, 1.8, 0.0)

	# MID-LEFT BRANCH — VERTICAL (col 5, rows 4–10)
	# Sucks water upward into that mid-left branch.
	set_flow_rect(4, 5, 10, 5, 0.0, -1.4)

	# CENTRAL VERTICAL FEEDER — (col 10, rows 4–10)
	# Pulls up toward the middle of the map.
	set_flow_rect(4, 10, 10, 10, 0.0, -1.2)

	# LOWER SIDE CHANNEL — (row 6, cols 12–14)
	# Drifts right, then bends down at (7,14) toward the lower trunk area.
	set_flow_rect(6, 12, 6, 14, 1.4, 0.0)  # right
	set_flow_rect(7, 14, 7, 14, 0.0, 1.0)  # downward at the bend

	# BOTTOM POCKET NEAR RIGHT — (row 9, cols 15–16)
	# Small rightward eddy under the trunk.
	set_flow_rect(9, 15, 9, 16, 1.0, 0.0)

	# BOTTOM-LEFT VERTICAL — (col 1, rows 9–10)
	# Pulls up into the lower maze.
	set_flow_rect(9, 1, 10, 1, 0.0, -1.0)

	# BOTTOM-LEFT HORIZONTAL — (row 10, cols 3–4)
	# Short rightward drift.
	set_flow_rect(10, 3, 10, 4, 1.0, 0.0)
	print(FLOW)
	"""
