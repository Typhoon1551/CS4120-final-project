import pygame

import common
import ui
from character import Character
from .character_profile import CharacterProfile

import random
import time


BG_COLOR = (135, 206, 235)


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
			y += 32
		display.blit(overlay, (0, 0))
		_help_ticks -= 1
	return _help_ticks


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
		"EXIT",
		color=(255, 255, 255),
		hovered_color=(255, 0, 0),
		padding=10,
	)

	inventory_title = ui.TextBox(
		(window_width // 2, 20),
		(window_width // 2 - 20, 80),
		"Which item to use?",
		color=(230, 230, 230),
		padding=15,
	)

	### Combatant Profiles ###

	### Player Profile ###
	player_profile = CharacterProfile(
		player,
		(20, 20),
		(window_width // 2 - 40, window_height // 2 - 20),
		BG_COLOR,
	)

	### Enemy Profile

	enemy_profile = CharacterProfile(
		enemy,
		(20, window_height // 2),
		(window_width // 2 - 40, window_height // 2 - 20),
		BG_COLOR,
	)

	message_time = 0
	power = ""
	damage = 0

	### main loop ###
	while running:
		display.blit(background, (0, 0))

		### Exit Button ###
		if exit_button.pressed():
			running = False
			return running

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

		### Update Profiles ###
		player_profile.update_info(player)
		enemy_profile.update_info(enemy)

		### Render Elements ###
		if enemy.current_health <= 0:
			exit_button.render(display)
			player_turn = True
		elif player.current_health <= 0:
			return False
		x = 0
		if player_turn:
			inventory_title.render(display)
			for i in range(len(inventory_buttons) - 1, -1, -1):
				inventory_buttons[i].render(display)
		else:
			message_time = 500
			time.sleep(0.8)
			if len(enemy.inventory) > 0:
				x = random.randint(0, len(enemy.inventory) - 1)
				before = str(player.current_health)[:]
				# print(before)
				power = enemy.inventory[x].name
				enemy.inventory[x].effect(player, enemy, enemy.inventory[x])
				player_turn = True
				damage = int(before) - player.current_health
				# print(damage)
			else:
				damage = random.randint(10, 50)
				power = "itself being toxic"
				player.current_health -= damage
				player_turn = True
		for i in inventory_buttons:
			if i.pressed():
				player.inventory[i.id].effect(
					player, enemy, player.inventory[i.id]
				)
				player_turn = False

		player_profile.render(display)
		enemy_profile.render(display)

		message_time = message(
			message_time,
			[
				f'Enemy used {power}, which dealt you {damage} damage. \nYou are at {player.current_health} health'
			],
			display,
			(window_height - 80) // 2,
			40,
			40,
			(225, 0, 0),
		)

		### Event Handling ###
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				result = "quit"
				running = False

		clock.tick(common.FPS)

		pygame.display.update()
