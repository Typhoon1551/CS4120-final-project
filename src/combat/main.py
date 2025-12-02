import pygame

import common
import ui
from character import Character

BG_COLOR = (135, 206, 235)


def combat_main(display: pygame.Surface, player: Character, enemy: Character):
	### pygame stuff ###
	window_width = display.get_size()[0]
	window_height = display.get_size()[1]

	background = pygame.Surface((window_width, window_height))
	background.fill(BG_COLOR)

	running = True
	clock = pygame.time.Clock()

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
		(20, window_height - 70),
		(100, 50),
		'EXIT',
		color=(255, 255, 255),
		hovered_color=(255, 0, 0),
		padding=10,
	)

	inventory_title = ui.TextBox(
		(window_width // 2, 20),
		(window_width // 2 - 20, 80),
		'Which item to use?',
		color=(230, 230, 230),
		padding=15,
	)

	### Combatant Profiles ###

	### Player Profile ###
	player_title = ui.TextBox(
		(20, 20),
		(window_width // 2 - 40, 80),
		player.name,
		padding=15,
		color=BG_COLOR,
	)
	player_hp_bar = ui.ProgressBar(
		(20, 120),
		(window_width // 2 - 40, 40),
		player.max_health,
		player.current_health,
		(255, 0, 0),
		(0, 255, 0),
	)

	### Enemy Profile

	enemy_title = ui.TextBox(
		(20, window_height // 2),
		(window_width // 2 - 40, 80),
		enemy.name,
		padding=15,
		color=BG_COLOR,
	)
	enemy_hp_bar = ui.ProgressBar(
		(20, window_height // 2 + 100),
		(window_width // 2 - 40, 40),
		enemy.max_health,
		enemy.current_health,
		(255, 0, 0),
		(0, 255, 0),
	)

	### main loop ###
	while running:
		display.blit(background, (0, 0))

		### Exit Button ###
		if exit_button.pressed() == True:
			running = False
			return running
			break
			continue

		### Inventory ###
		inventory_buttons = []
		for i in range(len(player.inventory)):
			inventory_buttons.append(
				ui.Button(
					(window_width // 2, 120 + 100 * i),
					(window_width // 2 - 20, 80),
					player.inventory[i].name,
					color=(200, 200, 200),
					hovered_color=(150, 150, 150),
					padding=15,
					id=i,
				).tooltip(
					player.inventory[i].description,
					(168, 123, 71),
					1.0,
					(0, 0, 0),
					18,
					10,
				)
			)

		for i in inventory_buttons:
			if i.pressed():
				player.inventory[i.id].effect(
					player, enemy, player.inventory[i.id]
				)

		### Update Profiles ###
		player_hp_bar.value = player.current_health
		enemy_hp_bar.value = enemy.current_health

		### Render Elements ###
		exit_button.render(display)

		if player_turn:
			inventory_title.render(display)
			for i in range(len(inventory_buttons) - 1, -1, -1):
				inventory_buttons[i].render(display)

		player_title.render(display)
		player_hp_bar.render(display)

		enemy_title.render(display)
		enemy_hp_bar.render(display)

		### Event Handling ###
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				result = 'quit'
				running = False

		clock.tick(common.FPS)

		pygame.display.update()
