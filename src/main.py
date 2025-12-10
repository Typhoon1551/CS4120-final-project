# external imports
import pygame
import pygame.locals
import os, sys
import random
import time
import ui

# internal imports
import items
import character
from combat import combat_main
from adventure import story
import common


def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(base_path, relative_path)


def message(
	_help_ticks, message, display, y, x, size=28, color=(235, 245, 255)
):
	if _help_ticks > 0:
		overlay = pygame.Surface(display.get_size(), pygame.SRCALPHA)
		font = pygame.font.SysFont(None, size)
		lines = message
		for ln in lines:
			txt = font.render(ln, True, color)
			overlay.blit(txt, (x, y))
			y += size + 10
		display.blit(overlay, (0, 0))
		_help_ticks -= 1
	return _help_ticks


def draw_player(characterbuild, display):
	left = int(characterbuild["left"])
	top = int(characterbuild["top"])
	width = int(characterbuild["width"])
	height = int(characterbuild["height"])
	color = characterbuild["color"]
	facing = characterbuild.get("facing", "R")
	left = int(characterbuild["left"])
	top = int(characterbuild["top"])
	width = int(characterbuild["width"])
	height = int(characterbuild["height"])
	color = characterbuild["color"]
	facing = characterbuild.get("facing", "R")

	body = pygame.Rect(left, top, width, height)
	pygame.draw.rect(display, color, body, border_radius=5)

	nose_R = (
		(left + width - 5, top),
		(left + width - 5, top + height),
		(left + (width * 2 - 5), top + (height // 2)),
	)
	tail_R = (
		(left - width + 10, top),
		(left - width + 10, top + height),
		(left + 10, top + (height // 2)),
	)

	cx = left + width // 2
	cy = top + height // 2

	def mirror_x(poly):
		return tuple((2 * cx - x, y) for (x, y) in poly)

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
		nose, tail = (
			rotate90(rotate90(rotate90(nose_R))),
			rotate90(rotate90(rotate90(tail_R))),
		)
		eye = (left + int(width * 0.25), top + int(height * 0.75))
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
		nose, tail = (
			rotate90(rotate90(rotate90(nose_R))),
			rotate90(rotate90(rotate90(tail_R))),
		)
		eye = (left + int(width * 0.25), top + int(height * 0.75))

	pygame.draw.polygon(display, color, nose)
	pygame.draw.polygon(display, color, tail)
	pygame.draw.circle(
		display, (225, 0, 225), (int(eye[0]), int(eye[1])), int(width * 0.1)
	)


def hit1(current_health, health_message):
	current_health -= random.randint(1, 5)
	health_message = 60
	return [current_health, health_message]


def find_enemy(enemies):
	good = False
	while not good:
		enemy = random.choice(enemies)
		if enemy.current_health > 0:
			good = True
			return enemy


def main():
	pygame.init()

	icon = pygame.image.load(resource_path("/assets/fish_icon.png"))
	display_size = pygame.display.Info()
	display = pygame.display.set_mode(
		(display_size.current_w, display_size.current_h), pygame.RESIZABLE
	)
	icon1 = pygame.display.set_icon(icon)

	story.setup_flow()
	tilesw = 3
	tilesh = 3
	veiw_w = tilesw * story.TILE_SIZE
	veiwh = tilesh * story.TILE_SIZE

	render_surf = pygame.Surface((veiw_w, veiwh)).convert()
	spawn = story.get_safe_start_rect(
		width=int(character.Character.character_design["width"]),
		height=int(character.Character.character_design["height"]),
	)
	cd = character.Character.character_design
	cd["left"], cd["top"] = spawn.left, spawn.top
	cd.setdefault("facing", "R")
	vis_rect = pygame.Rect(
		character.Character.character_design["left"],
		character.Character.character_design["top"],
		character.Character.character_design["width"],
		character.Character.character_design["height"],
	)
	story.init_debris(6)
	story.spawn_debris_near(vis_rect.centerx, vis_rect.centery, 3)
	pygame.font.init()
	_hud_font = pygame.font.SysFont(None, 22)
	_help_ticks = 500
	_hit_cooldown = 0
	health_message = []

	clock = pygame.time.Clock()
	time1 = time.time()
	level = 1
	### Player/Enemy Initialization ###
	player = character.Character(
		50000,
		700,
		[
			items.basic_wand(level),
			items.health_potion(100),
			items.health_potion(100),
			items.health_potion(100),
		],
		"John Fish",
		"A cute little guppy",
		vis_rect,
	)

	enemy1 = character.Character(200, 200, [], "Pizza Box", "Death for you")
	enemy2 = character.Character(500, 500, [], "Netting", "Death for you")
	enemy3 = character.Character(50, 50, [], "Floss", "Death for you")
	enemy4 = character.Character(100, 100, [], "Hair clump", "Death for you")
	enemy5 = character.Character(40, 40, [], "Grease", "Death for you")
	enemy6 = character.Character(150, 150, [], "Mold Colony", "Death for you")
	print(player.max_health)
	player_hp_bar = ui.ProgressBar(
		(display_size.current_w // 2 - 10, 20),
		(display_size.current_w // 2 - 40, 20),
		player.max_health,
		player.current_health,
		(255, 0, 0),
		(0, 255, 0),
	)
	enemies = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6]
	for x in enemies:
		x.inventory.append(items.drain_o())

	### Main Loop ###
	while True:
		c = (225, 225, 225)
		if player.current_health <= 0:
			overlay = pygame.Surface(display.get_size(), pygame.SRCALPHA)
			font = pygame.font.SysFont(None, 500)
			lines = "YOU DIED"
			txt = font.render(lines, True, color=c)
			overlay.blit(txt, (20, display_size.current_h // 4))
			display.blit(overlay, (15, 0))
			exit_button = ui.Button(
				(40, display_size.current_h - 200),
				(100, 50),
				"EXIT",
				color=(255, 255, 255),
				hovered_color=(255, 0, 0),
				padding=10,
			)
			while True:
				if exit_button.pressed() == True:
					pygame.quit()
					sys.exit()
					break
				for event in pygame.event.get():
					if event.type == pygame.locals.QUIT:
						pygame.quit()
						sys.exit()

				exit_button.render(display)
				pygame.display.update()
			pygame.quit()
			sys.exit()
			break
		elif player.current_health == 50000:
			overlay = pygame.Surface(display.get_size(), pygame.SRCALPHA)
			lines = [
				"Welcome to FISH",
				"You are a young goldfish wizard who, after a duel, somehow ended up in this system of pipes",
				"You must learn about what obstacles lie in your path and eliminate them if you wish to ever get home",
				"Use the WASD / Arrows to swim",
				"Portals surround the pipes. They hurt a little",
				"Use the portals to get around. Beware, some lead to enemies, but some lead to upgrades.",
				"Pink squares are enemies, teal squares are upgades",
				"Debris = small damage",
				"Don't hit the walls, it will hurt.",
				"Find your enemies and destroy them",
				"Use your wizard powers to stay safe",
				"Look around for upgrades, they will matter a lot.",
				"You have these items:",
			]
			for x in list(player.inventory):
				lines.append(str(str(x.name) + ": " + str(x.description)))
			exit_button = ui.Button(
				(40, display_size.current_h - 200),
				(100, 50),
				"Play!",
				color=(255, 255, 255),
				hovered_color=(255, 0, 0),
				padding=10,
			)
			while True:
				_help_ticks = (
					message(_help_ticks, lines, display, 30, 30, 40) + 1
				)
				if exit_button.pressed() == True:
					player.current_health = 700
					break
				for event in pygame.event.get():
					if event.type == pygame.locals.QUIT:
						pygame.quit()
						sys.exit()

				exit_button.render(display)
				pygame.display.flip()

		elif all(e.current_health <= 0 for e in enemies):
			overlay = pygame.Surface(display.get_size(), pygame.SRCALPHA)
			font = pygame.font.SysFont(None, 500)
			lines = "YOU WON"
			txt = font.render(lines, True, color=c)
			overlay.blit(txt, (20, display_size.current_h // 4))
			display.blit(overlay, (15, 0))
			exit_button = ui.Button(
				(20, display_size.current_h - 200),
				(100, 50),
				"EXIT",
				color=(255, 255, 255),
				hovered_color=(255, 0, 0),
				padding=10,
			)
			while True:
				if exit_button.pressed() == True:
					pygame.quit()
					sys.exit()
					break
				for event in pygame.event.get():
					if event.type == pygame.locals.QUIT:
						pygame.quit()
						sys.exit()
				exit_button.render(display)

				pygame.display.update()
			pygame.quit()
			sys.exit()
			break

		else:
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

			cd = player.character_design
			vis_rect = pygame.Rect(
				int(cd["left"]),
				int(cd["top"]),
				int(cd["width"]),
				int(cd["height"]),
			)
			phys_rect = vis_rect.inflate(
				-int(vis_rect.width * 0.30), -int(vis_rect.height * 0.20)
			)
			phys_rect.center = vis_rect.center

			fx, fy = story.flow_at(phys_rect.centerx, phys_rect.centery)
			mdx = dx + (fx)
			mdy = dy + (fy)

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

			old = phys_rect

			if mdx or mdy:
				phys_rect = story.try_move(phys_rect, mdx, mdy, player)
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
				vis_rect.center = dest
				cd["left"], cd["top"] = vis_rect.left, vis_rect.top
			cam_off = story.get_camera_offset(phys_rect, veiw_w, veiwh)

			story.draw_drain_chamber(render_surf, cam_off)
			story.update_and_draw_debris(render_surf, cam_off)

			screen_space_cd = dict(cd)
			screen_space_cd["left"] = cd["left"] - cam_off[0]
			screen_space_cd["top"] = cd["top"] - cam_off[1]
			draw_player(screen_space_cd, render_surf)
			for d in story.DEBRIS:
				if phys_rect.colliderect(d.rect):
					if _hit_cooldown == 0:
						hit = hit1(player.current_health, 10)
						player.current_health = hit[0]
						health_message.append(hit[1])
						phys_rect = story.try_move(
							phys_rect,
							-4 if mdx >= 0 else 4,
							-4 if mdy >= 0 else 4,
							player,
						)
						vis_rect.center = phys_rect.center
						cd["left"], cd["top"] = vis_rect.left, vis_rect.top
						_hit_cooldown = 45
					break

			pygame.transform.scale(render_surf, display.get_size(), display)

			now = time.time()
			none = message(
				100,
				[
					f"Health: {player.current_health}",
					f"Time: {str(int(now - time1))}",
				],
				display,
				20,
				20,
			)

			if ((phys_rect.centerx - old.centerx) != int(mdx)) and (
				(phys_rect.centery - old.centery) != int(mdy)
			):
				hit = hit1(player.current_health, health_message)
				player.current_health = hit[0]
				health_message.append(hit[1])
			index = 0

			for x in health_message:
				health_message[index] = message(
					health_message[index],
					["-1"],
					display,
					20,
					100 * (index + 1),
					200,
					(225, 0, 0),
				)
				index += 1
				# health_message = message(health_message, ['-1'], display, 20, 100, 300, (225,0,0))

			message1 = [
				"WASD / Arrows to swim",
				"Portals surround the pipes. they hurt a little",
				"Use the portals to get around. Beware, some lead to enemies",
				"but some lead to friends.",
				"Debris = small damage",
				"Don't hit the walls, it will hurt.",
				"Find your enemies and destroy them",
				"Use your wizard powers to stay safe",
				"Look around for upgrades, they will matter a lot.",
				"You have these items:",
			]

			for x in list(player.inventory):
				message1.append(str(x.description))

			_help_ticks = message(
				_help_ticks,
				message1,
				display,
				40,
				display_size.current_w - 500,
				40,
			)
			if len(health_message) > 0:
				index = 0
				for x in health_message:
					health_message[index] -= 1
					if x <= 0:
						health_message.pop(index)
					index += 1
			if _help_ticks > 300:
				player.current_health = 700
			if story.is_upgrade(phys_rect):
				level += 1
				story.remove_upgrade(phys_rect)
				health_message.insert(0, 600)
				player.inventory[0] = items.basic_wand(level)

			try:
				if health_message[0] > 60:
					message(
						health_message[0],
						[f"You upgraded your items to level {level}"],
						display,
						50,
						display_size.current_w - 1000,
						60,
						(0, 0, 225),
					)
			except:
				none = 0

			if story.is_enemey(phys_rect):
				enemy = find_enemy(enemies)
				none = combat_main(display, player, enemy)
				story.remove_enemy(phys_rect)
				end = story.is_enemey(phys_rect)
				while end:
					mdx = (mdx + random.randint(-1, 1)) * -1
					mdy = (mdy + random.randint(-1, 1)) * -1
					phys_rect = story.try_move(phys_rect, (mdx), (mdy), player)
					end = story.is_enemey(phys_rect)
					if not end:
						mdx = dx + int(round(fx)) * 4
						mdy = dy + int(round(fy)) * 4
						phys_rect = story.try_move(
							phys_rect, (mdx), (mdy), player
						)
						end = story.is_enemey(phys_rect)

			player_hp_bar.value = player.current_health
			player_hp_bar.render(display)
			clock.tick(common.FPS)

		for event in pygame.event.get():
			if event.type == pygame.locals.QUIT:
				pygame.quit()
				sys.exit()
		time.sleep(0.0001)
		pygame.display.flip()


if __name__ == "__main__":
	main()

	"""
	story.clear_flow()
	#set_flow_rect(r0: int, c0: int, r1: int, c1: int, fx: float, fy: float)
	#main Tube
	story.set_flow_rect(2, 0, 3, 15, 2.0, 0.0)
	story.set_flow_rect(6, 16, 7, 23, 2.2, 0.0)

	story.set_flow_rect(1, 15, 8, 16, 1.0, 1.8)


	story.set_flow_rect(8, 19, 10, 19, 0.0, -1.4)
	story.set_flow_rect(5, 1, 5, 5, 1.2, 0.0)
	story.set_flow_rect(6, 1, 7, 1, 0.0, -1.2)
	#first hole, straight down.
	story.set_flow_rect(3, 5, 11, 5, 0.5, -2.6)

	story.set_flow_rect(3, 10, 10, 12, 0.0, -1.3)
	story.set_flow_rect(6, 13, 7, 15, 1.0, 0.0)

	story.set_flow_rect(9, 15, 9, 16, 1.0, 0.0)
	story.set_flow_rect(7, 7, 7, 10, 1.0, 0.0)
	"""
