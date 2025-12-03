# CS4120-final-project

## Description
This is a simple adventure game about a fish navigating sewers, featuring a complex environment and turn-based combat.

## Running
This project uses [UV](https://docs.astral.sh/uv/) for dependency management. In order to run the project:
1. [Install UV.](https://docs.astral.sh/uv/getting-started/installation/)
2. Clone the repository with `git clone` or your favorite git client.
3. Run `uv run src/main.py` in the project root. UV will handle venvs and dependencies for you.

## Feature Chart

### General
- [x] Learn PyGame
- [x] Design Player

### Story
- [x] Player Movement
  - [x] Character rotation
  - [x] Interaction with walls, enemies, upgrades
- [x] Background
- [x] Interactive Map
- [x] Combat Encounters
- [x] Current flows (semi-operational)
- [x] Walls
  - [x] Wall-player collisions
- [x] Portals
- [x] Camera
  - [x] Camera movement when approaching edge of map
- [x] Messages
  - [x] Hit points from bouncing off of walls
  - [x] Instructions
  - [x] health + time
- [x] Health Bar
- [x] Debris
  - [x] Spawning debris
  - [x] Debris interaction
  - [x] Debris bouncing off of walls
- [x] Building Enemies and interaction
- [x] Building Items
- [x] Activiating upgrades
- [x] End screens
- [x] Correccting errors + Bug checking
- [x] Activating combat

### Combat
- [x] Custom UI Framework
  - [x] Buttons
  - [x] Text Boxes
  - [x] Progress Bars
  - [ ] Icons (no)
  - [x] Tooltips
- [x] Run passive item effects at start of battle
- [x] Item Selection
- [x] Run active item effect when used
- [x] Initialize combat data
- [x] Turn Cycle
  - [ ] fix turn cycle timing
- [x] Enemy AI
  - [ ] More advanced AI?
- [x] Return win/lose state
