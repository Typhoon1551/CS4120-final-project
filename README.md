# CS4120-final-project

## Description
This is a simple adventure that uses an LLM to generate a unique experience every time

## Running
This project uses [UV](https://docs.astral.sh/uv/) for dependency management. In order to run the project:
1. [Install UV.](https://docs.astral.sh/uv/getting-started/installation/)
2. Clone the repository with `git clone` or your favorite git client.
3. Run `uv run src/main.py` in the project root. UV will handle venvs and dependencies for you.

## Feature Chart

### General
- [ ] Learn PyGame
- [ ] Design Player

### Story
- [x] Player Movement
- [ ] Background
- [ ] Interactive Map
- [ ] Obstacles
- [ ] Combat Encounters

### Combat
- [ ] Custom UI Framework
  - [x] Buttons
  - [x] Text Boxes
  - [ ] Health Bars
  - [ ] Icons
  - [ ] Tooltips
- [x] Run passive item effects at start of battle
- [x] Item Selection
- [x] Run active item effect when used
- [ ] Initialize combat data
- [ ] Turn Cycle
- [ ] Enemy AI
- [ ] Return win/lose state
