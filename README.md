# Undertale-like RPG Game

A 2D RPG game inspired by Undertale, built with Pygame. The game features multiple levels, NPCs, enemies, boss battles, and various game mechanics.

## Features

- 7 unique levels with increasing difficulty
- Multiple enemy types (regular enemies, mini-boss, and final boss)
- NPC interaction system with dialogue
- Combat system with sword attacks
- Boss projectile system
- Health and speed power-ups
- Player stats and health system
- Door progression system
- Smooth player movement with WASD/Arrow keys

## Prerequisites

- Python 3.x
- Pygame

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment (optional but recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install pygame
```

## How to Play

1. Run the game:
```bash
python main.py
```

2. Controls:
- Movement: WASD or Arrow keys
- Attack: ENTER key
- Interact/Proceed: SPACE key

## Game Mechanics

### Player
- The player starts with 10000 health and 1000 damage
- Movement speed can be increased by collecting speed potions
- Health can be restored by collecting health potions

### Levels
- Each level must be cleared of enemies before proceeding
- Levels progressively get harder with stronger enemies
- Special boss levels feature unique mechanics

### Combat
- Use ENTER to attack with your sword
- Attacks have a cooldown period
- Bosses can shoot projectiles that must be dodged
- Defeated enemies may drop power-ups

### NPCs
- NPCs provide helpful information and story elements
- Interact with NPCs using the SPACE key when near them

### Power-ups
- Health Potions: Restore player health
- Speed Potions: Permanently increase movement speed

## Asset Requirements

The game requires the following image assets in an `assets` folder:
- goodGuy.png (player sprite)
- badGuy1.png (regular enemy)
- badGuy2.png (mini-boss)
- badGuy3.png (final boss)
- NPC1.png, NPC2.png, NPC3.png (NPC sprites)
- door.png (door sprite)
- health.png (health potion)
- speed.png (speed potion)
- Sword.png (weapon sprite)
- bg.png (background image)

## Game Structure

The game is built using object-oriented programming with the following main components:
- NPC class: Handles NPC behavior and interactions
- Player class: Manages player attributes and actions
- Enemy management system
- Level progression system
- Power-up system
- Combat mechanics

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or bug fixes.

## License

[Add your chosen license here] # Amy-ShannieFInalProject
