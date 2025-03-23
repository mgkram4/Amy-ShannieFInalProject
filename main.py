# wn in the game planted face down and he gets out
# wasd or arrow keys for quadriteral movement
# key binding to interact with in game objects (NPC, doors, flowers)

# scaling system for enemy

# win by finding the past NPC "friends" they lead you to the exit

# Sounds

# List of sprites : USER , Enemies(final boss, small, mini boss ), Object (flower bed, signs, armor, wepons)
# Background image
# Boost items (postions: heal, +speed, -health )
# Levels : 5

# NPC diglog
# One gives item
# one chats
# random information


class NPC():
    def __init__(self, health, attack, defense, speed, isBad, level):
        
        pass
    
class Player(NPC):
    
    def __init__(self, health, attack, defense, speed, isBad, level):
        super().__init__(health, attack, defense, speed, isBad, level)
        
        
        
        
import math
import os
import random
import time  # Add time module import

import pygame
import pygame.mixer  # For background music

# Initialize Pygame
pygame.init()

# Initialize the mixer for music
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 800, 600
SCREEN_SCALE = min(pygame.display.Info().current_w / WIDTH, pygame.display.Info().current_h / HEIGHT) * 0.8  # Reduced by 20%
WIDTH = int(WIDTH * SCREEN_SCALE)
HEIGHT = int(HEIGHT * SCREEN_SCALE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Downfall")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)
BLUE = (0, 0, 255)  # Added back for enemy color

# Player stats
player_size = int(40 * SCREEN_SCALE)  # Scale player size
player_pos = [WIDTH // 2 - player_size // 2, -player_size]  # Now uses player_size after it's defined
player_speed = int(6 * SCREEN_SCALE)  # Scale speed
player_health = 10000
player_damage = 15
player_attack_cooldown = 15

# Game state
current_level = 1
MAX_LEVELS = 6  # Reduced from 7 to match available levels
current_room = "intro"  # Start with intro scene

# Door positions for each level
door_positions = {
    f"level_{i}": {"pos": [700, 300], "size": [60, 100]} for i in range(1, MAX_LEVELS + 1)
}

# NPCs for each level with different dialogues
level_npcs = {
    "level_1": [
        {"pos": [400, 100], "message": "Welcome to your journey... The path ahead is dangerous!", "sprite": "npc1"},
        {"pos": [200, 300], "message": "You'll face regular enemies first, then bosses later...", "sprite": "npc2"}
    ],
    "level_2": [
        {"pos": [300, 200], "message": "These are just regular enemies. The real challenge is yet to come.", "sprite": "npc3"}
    ],
    "level_3": [
        {"pos": [100, 100], "message": "Be careful! The mini boss is much stronger than regular enemies!", "sprite": "npc1"}
    ],
    "level_4": [
        {"pos": [300, 200], "message": "WARNING: Mini-boss ahead! They can shoot projectiles!", "sprite": "npc2"},
        {"pos": [500, 200], "message": "Be careful and dodge their attacks!", "sprite": "npc3"}
    ],
    "level_5": [
        {"pos": [100, 100], "message": "This is it. The final boss awaits...", "sprite": "npc1"}
    ],
    "level_6": [
        {"pos": [300, 200], "message": "The final boss is next. Prepare yourself!", "sprite": "npc2"}
    ],
    "level_7": [
        {"pos": [100, 100], "message": "This is it. The final boss awaits...", "sprite": "npc3"}
    ]
}

# Enemy configurations for each level
enemy_configs = {

    "level_1": {"count": 2, "health": 50, "speed": 1.2, "damage": 5},  # Basic enemies
    "level_2": {"count": 3, "health": 75, "speed": 1.3, "damage": 8},  # More enemies
    "level_3": {"count": 0, "health": 0, "speed": 0, "damage": 0},  # Checkpoint/warning level
    "level_4": {"count": 1, "health": 200, "speed": 1.5, "damage": 12, "is_boss": True, "name": "Mini Boss", "can_shoot": True},
    "level_5": {"count": 4, "health": 100, "speed": 1.6, "damage": 10},  # Hard enemies
    "level_6": {"count": 1, "health": 500, "speed": 1.8, "damage": 20, "is_boss": True, "name": "Final Boss", "can_shoot": True}
}

# Current level enemies
enemies = []

# Add these near the other game state variables
# Attack animation
attack_animation = None
ATTACK_DURATION = 15  # frames
ATTACK_FRAMES_PER_DIRECTION = 4  # Each direction gets 4 frames
player_direction = 0
last_movement_key = None
npc_message = None
message_time = 0

# Add to the game state variables
enemy_respawn_timer = 0
ENEMY_RESPAWN_TIME = 5000  # 5 seconds in milliseconds

# Add to game state variables
projectiles = []  # Store active projectiles
PROJECTILE_SPEED = 5
PROJECTILE_SIZE = int(10 * SCREEN_SCALE)
BOSS_SHOOT_COOLDOWN = 60  # Frames between boss shots

# Add new constants for items/potions
POTION_SIZE = int(30 * SCREEN_SCALE)
potions = []  # List to store active potions on the ground

# Load images
player_img = pygame.image.load('assets/goodGuy.png')
player_img = pygame.transform.scale(player_img, (player_size, player_size))

enemy_imgs = {
    'regular': pygame.image.load('assets/badGuy1.png'),
    'miniboss': pygame.image.load('assets/badGuy2.png'),
    'boss': pygame.image.load('assets/badGuy3.png')
}

# Scale enemy images
for key in enemy_imgs:
    enemy_imgs[key] = pygame.transform.scale(enemy_imgs[key], (player_size, player_size))

# Load item images
health_potion_img = pygame.image.load('assets/health.png')
speed_potion_img = pygame.image.load('assets/speed.png')
sword_img = pygame.image.load('assets/Sword.png')
sword_img = pygame.transform.scale(sword_img, (48, 48))  # Adjust size as needed
health_potion_img = pygame.transform.scale(health_potion_img, (POTION_SIZE, POTION_SIZE))
speed_potion_img = pygame.transform.scale(speed_potion_img, (POTION_SIZE, POTION_SIZE))

# Add to the image loading section
npc_imgs = {
    'npc1': pygame.image.load('assets/NPC1.png'),
    'npc2': pygame.image.load('assets/NPC2.png'),
    'npc3': pygame.image.load('assets/NPC3.png')
}

# Scale NPC images
for key in npc_imgs:
    npc_imgs[key] = pygame.transform.scale(npc_imgs[key], (player_size, player_size))

# Doors
main_door_pos = [700, 300]
main_door_size = [int(96 * SCREEN_SCALE), int(160 * SCREEN_SCALE)]  # Increase door size
main_door_rect = pygame.Rect(main_door_pos[0], main_door_pos[1], main_door_size[0], main_door_size[1])

second_door_pos = [50, 300]
second_door_size = [int(96 * SCREEN_SCALE), int(160 * SCREEN_SCALE)]  # Increase door size
second_door_rect = pygame.Rect(second_door_pos[0], second_door_pos[1], second_door_size[0], second_door_size[1])

# Load door image after door sizes are defined
door_img = pygame.image.load('assets/door.png')
door_img = pygame.transform.scale(door_img, (main_door_size[0], main_door_size[1]))

# Font
font = pygame.font.Font(None, 36)

# Add a flag to track if level is cleared
level_cleared = False

# Add to the image loading section
bg_img = pygame.image.load('assets/bg.png')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))  # Scale to fit screen
flower_bg_img = pygame.image.load('assets/doorway.png')
flower_bg_img2 = pygame.image.load('assets/flower.png')
flower_bg_img = pygame.transform.scale(flower_bg_img, (WIDTH, HEIGHT))
flower_bg_img2 = pygame.transform.scale(flower_bg_img2, (WIDTH, HEIGHT))
dungeon_bg_img = pygame.image.load('assets/dungeon_thing.jpg')
# Load the dungeon background
dungeon_bg_img = pygame.transform.scale(dungeon_bg_img, (WIDTH, HEIGHT))  # Scale to fit screen

# Add these variables near other game state variables
intro_completed = False
player_falling = True
player_fall_speed = 3
intro_door_pos = [WIDTH // 2 - 45, HEIGHT - 180]
intro_door_size = [90, 150]
intro_door_rect = pygame.Rect(intro_door_pos[0], intro_door_pos[1], intro_door_size[0], intro_door_size[1])

# Load victory screen image
victory_img = pygame.image.load('assets/you_win.png')
victory_img = pygame.transform.scale(victory_img, (WIDTH, HEIGHT))

# Add these variables near other game state variables
game_start_time = 0
elapsed_time = 0
high_scores = []
SCORES_FILE = "speedrun_scores.txt"

# Add these constants near the top with other game settings
DIALOG_WIDTH = int(WIDTH * 0.8)
DIALOG_HEIGHT = int(HEIGHT * 0.2)
DIALOG_PADDING = 20
DIALOG_BG_COLOR = (50, 50, 50, 180)  # Dark gray with transparency
DIALOG_TEXT_COLOR = WHITE
DIALOG_DISPLAY_TIME = 5000  # Display for 5 seconds instead of 3

try:
    dialog_font = pygame.font.Font("assets/font.ttf", 28)  # Try to load a custom font
except:
    dialog_font = pygame.font.Font(None, 32)  # Fallback to default font but smaller

# Add these new variables with other game state variables
current_music = None
music_files = {
    'intro': 'assets/intro_music.mp3',  # Add your music file paths here
    'dungeon': 'assets/dungeon_music.mp3',
    'boss': 'assets/boss_music.mp3',
    'victory': 'assets/victory_music.mp3'
}

# Add this new function to handle music
def play_background_music(music_type):
    global current_music
    try:
        # Only change music if it's different from what's currently playing
        if current_music != music_type:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music_files[music_type])
            pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
            current_music = music_type
            print(f"Now playing: {music_type} music")
    except:
        print(f"Error loading music: {music_type}")

def draw_player():
    screen.blit(player_img, (player_pos[0], player_pos[1]))


def draw_npcs():
    if current_room.startswith('level_') and current_room != "level_1":  # Skip drawing NPCs in level 1
        if current_room in level_npcs:
            for npc in level_npcs[current_room]:
                npc_img = npc_imgs[npc["sprite"]]
                screen.blit(npc_img, (npc["pos"][0], npc["pos"][1]))

def draw_door():
    if current_room == "main":
        screen.blit(door_img, (main_door_pos[0], main_door_pos[1]))
    else:
        screen.blit(door_img, (second_door_pos[0], second_door_pos[1]))

def draw_enemies():
    if current_room.startswith('level_'):
        for enemy in enemies:
            # Choose appropriate enemy image based on type
            if enemy.get("is_boss"):
                if enemy.get("name") == "Final Boss":
                    img = enemy_imgs['boss']
                else:
                    img = enemy_imgs['miniboss']
            else:
                img = enemy_imgs['regular']
            
            # Draw the enemy
            screen.blit(img, (enemy["pos"][0], enemy["pos"][1]))
            
            # Draw health bar
            health_percentage = enemy["health"] / enemy["max_health"]
            bar_width = enemy["size"] * 1.5
            pygame.draw.rect(screen, RED, (enemy["pos"][0], enemy["pos"][1] - 15, bar_width, 10))
            pygame.draw.rect(screen, GREEN, (enemy["pos"][0], enemy["pos"][1] - 15, bar_width * health_percentage, 10))
            
            if enemy.get("is_boss"):
                name_text = font.render(enemy["name"], True, BLACK)
                screen.blit(name_text, (enemy["pos"][0], enemy["pos"][1] - 30))

def draw_attack():
    if attack_animation:
        frame, start_direction = attack_animation
        # Calculate which direction to show based on animation progress
        direction_progress = (ATTACK_DURATION - frame) // ATTACK_FRAMES_PER_DIRECTION
        current_direction = (start_direction + direction_progress) % 4
        
        sword_pos = [0, 0]
        rotated_sword = sword_img
        
        if current_direction == 0:  # right
            sword_pos = [player_pos[0] + player_size, player_pos[1]]
            rotated_sword = sword_img
        elif current_direction == 1:  # down
            sword_pos = [player_pos[0], player_pos[1] + player_size]
            rotated_sword = pygame.transform.rotate(sword_img, -90)
        elif current_direction == 2:  # left
            sword_pos = [player_pos[0] - int(48 * SCREEN_SCALE), player_pos[1]]
            rotated_sword = pygame.transform.rotate(sword_img, 180)
        elif current_direction == 3:  # up
            sword_pos = [player_pos[0], player_pos[1] - int(48 * SCREEN_SCALE)]
            rotated_sword = pygame.transform.rotate(sword_img, 90)
            
        screen.blit(rotated_sword, sword_pos)

def is_near_npc():
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    if current_room in level_npcs:
        for npc in level_npcs[current_room]:
            npc_rect = pygame.Rect(npc["pos"][0], npc["pos"][1], player_size, player_size)
            if player_rect.colliderect(npc_rect):
                return npc["message"]
    return None

def is_at_door():
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    if current_room == "intro":
        return player_rect.colliderect(intro_door_rect)
    elif current_room == "main":
        return player_rect.colliderect(main_door_rect)
    else:
        return player_rect.colliderect(second_door_rect)

def move_enemies():
    for enemy in enemies:
        dx = player_pos[0] - enemy["pos"][0]
        dy = player_pos[1] - enemy["pos"][1]
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist != 0:
            # Bosses have different movement patterns
            if enemy.get("is_boss"):
                # Bosses move more strategically - charge and retreat
                if dist < 200:  # If player is too close, back away
                    enemy["pos"][0] -= (dx / dist) * enemy["speed"]
                    enemy["pos"][1] -= (dy / dist) * enemy["speed"]
                else:  # Otherwise charge at player
                    enemy["pos"][0] += (dx / dist) * enemy["speed"]
                    enemy["pos"][1] += (dy / dist) * enemy["speed"]
            else:
                # Regular enemies just chase the player
                enemy["pos"][0] += (dx / dist) * enemy["speed"]
                enemy["pos"][1] += (dy / dist) * enemy["speed"]
            
            # Keep enemies on screen
            enemy["pos"][0] = max(0, min(enemy["pos"][0], WIDTH - enemy["size"]))
            enemy["pos"][1] = max(0, min(enemy["pos"][1], HEIGHT - enemy["size"]))

def check_enemy_collisions():
    global player_health
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy["pos"][0], enemy["pos"][1], enemy["size"], enemy["size"])
        if player_rect.colliderect(enemy_rect):
            player_health -= enemy["damage"]
            print(f"Player hit! Health: {player_health}")
            if player_health <= 0:
                print("Game Over!")
                return False
    return True

def change_level():
    global current_level, current_room, player_pos
    if current_level < MAX_LEVELS:
        current_level += 1
        current_room = f"level_{current_level}"
        player_pos = [50, HEIGHT // 2]  # Reset player position
        spawn_enemies_for_level(current_level)
        return True
    return False

def check_level_complete():
    global level_cleared
    if len(enemies) == 0:
        level_cleared = True  # Set flag when all enemies are defeated
        if current_level == MAX_LEVELS:
            # The player has defeated the final boss!
            return True
    return False

def spawn_potion(pos):
    # 70% chance for health potion, 30% chance for speed potion
    potion_type = 'health' if random.random() < 0.7 else 'speed'
    # Make the collision rect slightly larger than the image for easier pickup
    collision_rect = pygame.Rect(pos[0]-5, pos[1]-5, POTION_SIZE+10, POTION_SIZE+10)
    potions.append({
        'type': potion_type,
        'pos': list(pos),
        'rect': collision_rect
    })
    print(f"Spawned {potion_type} potion at {pos}")

def draw_potions():
    for potion in potions:
        img = health_potion_img if potion['type'] == 'health' else speed_potion_img
        screen.blit(img, potion['pos'])
        # Debug: Draw the collision rectangle
        pygame.draw.rect(screen, (255, 255, 255, 100), potion['rect'], 1)

def collect_potions():
    global player_health, player_speed
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    
    # Debug information
    if potions:
        print(f"Potions available: {len(potions)}")
        print(f"Player position: {player_pos}")
        for i, potion in enumerate(potions):
            print(f"Potion {i} position: {potion['pos']}, type: {potion['type']}")
    
    for potion in potions[:]:  # Use a copy of the list to safely remove items
        # Update the collision rect position (in case it moved)
        potion['rect'] = pygame.Rect(potion['pos'][0]-5, potion['pos'][1]-5, POTION_SIZE+10, POTION_SIZE+10)
        
        # Check collision with more debug info
        collision = player_rect.colliderect(potion['rect'])
        if collision:
            print(f"COLLISION DETECTED with {potion['type']} potion!")
            if potion['type'] == 'health':
                heal_amount = 500
                old_health = player_health
                player_health = min(10000, player_health + heal_amount)
                print(f"Health restored! +{player_health - old_health} HP")
            elif potion['type'] == 'speed':
                player_speed += int(1 * SCREEN_SCALE)
                print("Speed increased!")
            potions.remove(potion)

def player_attack():
    global enemies, attack_animation, enemy_respawn_timer, current_time, running
    
    # Start with current direction and animate in a circle
    attack_animation = (ATTACK_DURATION, player_direction)
    
    # Check for hits in all four directions since the attack will sweep all around
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    for dx, dy in directions:
        attack_rect = pygame.Rect(
            player_pos[0] + dx * player_size, 
            player_pos[1] + dy * player_size,
            player_size + abs(dx) * int(96 * SCREEN_SCALE), 
            player_size + abs(dy) * int(96 * SCREEN_SCALE)
        )
        
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy["pos"][0], enemy["pos"][1], enemy["size"], enemy["size"])
            if attack_rect.colliderect(enemy_rect):
                enemy["health"] -= player_damage
                print(f"Enemy hit! Enemy health: {enemy['health']}")
                if enemy["health"] <= 0:
                    # Check if this is the Final Boss
                    if enemy.get("name") == "Final Boss":
                        print("Final boss defeated! Game complete!")
                        # Remove the immediate exit and just remove the enemy
                        enemies.remove(enemy)
                        return "victory"  # Return a signal that victory has been achieved
                    
                    # Otherwise handle normal enemy defeat
                    spawn_potion(enemy["pos"])
                    enemies.remove(enemy)
                    print(f"{enemy.get('name', 'Enemy')} defeated!")
                    if not enemy.get("is_boss"):
                        enemy_respawn_timer = current_time + ENEMY_RESPAWN_TIME
    return None  # Return None when no victory condition is met

# Add new function to handle boss shooting
def handle_boss_shooting():
    for enemy in enemies:
        if enemy.get("can_shoot") and enemy.get("is_boss"):
            # Add shoot_cooldown if it doesn't exist
            if "shoot_cooldown" not in enemy:
                enemy["shoot_cooldown"] = 0
            
            if enemy["shoot_cooldown"] <= 0:
                # Calculate direction to player
                dx = player_pos[0] - enemy["pos"][0]
                dy = player_pos[1] - enemy["pos"][1]
                dist = math.sqrt(dx**2 + dy**2)
                
                if dist != 0:  # Avoid division by zero
                    # Normalize direction
                    dx = dx / dist
                    dy = dy / dist
                    
                    # Create new projectile
                    projectiles.append({
                        "pos": [enemy["pos"][0] + enemy["size"]/2, enemy["pos"][1] + enemy["size"]/2],
                        "dir": [dx, dy],
                        "damage": enemy["damage"] // 2  # Projectiles do half the contact damage
                    })
                    
                    enemy["shoot_cooldown"] = BOSS_SHOOT_COOLDOWN
            else:
                enemy["shoot_cooldown"] -= 1

def update_projectiles():
    global player_health
    
    # Move projectiles
    for projectile in projectiles[:]:
        projectile["pos"][0] += projectile["dir"][0] * PROJECTILE_SPEED
        projectile["pos"][1] += projectile["dir"][1] * PROJECTILE_SPEED
        
        # Check if projectile is off screen
        if (projectile["pos"][0] < 0 or projectile["pos"][0] > WIDTH or 
            projectile["pos"][1] < 0 or projectile["pos"][1] > HEIGHT):
            projectiles.remove(projectile)
            continue
        
        # Check collision with player
        projectile_rect = pygame.Rect(projectile["pos"][0], projectile["pos"][1], 
                                    PROJECTILE_SIZE, PROJECTILE_SIZE)
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
        
        if projectile_rect.colliderect(player_rect):
            player_health -= projectile["damage"]
            print(f"Hit by projectile! Health: {player_health}")
            projectiles.remove(projectile)
            if player_health <= 0:
                print("Game Over!")
                return False
    return True

def draw_projectiles():
    for projectile in projectiles:
        pygame.draw.circle(screen, RED, 
                         (int(projectile["pos"][0]), int(projectile["pos"][1])), 
                         PROJECTILE_SIZE // 2)

def spawn_enemies_for_level(level):
    global enemies
    enemies = []
    config = enemy_configs[f"level_{level}"]
    for _ in range(config["count"]):
        enemy_pos = [random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)]
        enemy = {
            "pos": enemy_pos,
            "size": 40 if not config.get("is_boss") else 80,  # Bosses are bigger
            "health": config["health"],
            "max_health": config["health"],  # Store max health for health bar
            "speed": config["speed"],
            "damage": config["damage"],
            "is_boss": config.get("is_boss", False),
            "name": config.get("name", "Enemy"),
            "can_shoot": config.get("can_shoot", False)
        }
        enemies.append(enemy)

# Update the draw_messages function to not show "Press SPACE to proceed" on final level
def draw_messages():
    if is_at_door():
        # Don't show any message if this is the final level and enemies are all defeated
        if current_level == MAX_LEVELS and len(enemies) == 0:
            return
            
        msg_bg = pygame.Surface((WIDTH * 0.6, 50), pygame.SRCALPHA)
        msg_bg.fill((0, 0, 0, 150))  # Semi-transparent black background
        screen.blit(msg_bg, (WIDTH * 0.2, HEIGHT - 60))
        
        if len(enemies) > 0:
            message = font.render("Defeat all enemies first!", True, RED)
            screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 45))
        else:
            message = font.render("Press SPACE to proceed", True, GREEN)
            screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 45))

# Add a new function to draw NPC dialog
def draw_npc_dialog():
    if npc_message and current_time - message_time < DIALOG_DISPLAY_TIME:
        # Create dialog box with semi-transparent background
        dialog_box = pygame.Surface((DIALOG_WIDTH, DIALOG_HEIGHT), pygame.SRCALPHA)
        dialog_box.fill(DIALOG_BG_COLOR)
        dialog_x = (WIDTH - DIALOG_WIDTH) // 2
        dialog_y = HEIGHT - DIALOG_HEIGHT - 20
        
        # Add border
        pygame.draw.rect(dialog_box, WHITE, (0, 0, DIALOG_WIDTH, DIALOG_HEIGHT), 2)
        
        # Split message into multiple lines if needed (wrap text)
        words = npc_message.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            text_width = dialog_font.size(test_line)[0]
            
            if text_width < DIALOG_WIDTH - DIALOG_PADDING * 2:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        
        lines.append(current_line)  # Add the last line
        
        # Draw dialog box
        screen.blit(dialog_box, (dialog_x, dialog_y))
        
        # Draw text lines
        line_spacing = 35
        for i, line in enumerate(lines):
            text_surface = dialog_font.render(line, True, DIALOG_TEXT_COLOR)
            screen.blit(text_surface, (dialog_x + DIALOG_PADDING, dialog_y + DIALOG_PADDING + i * line_spacing))
        
        # Add a "Press SPACE to dismiss" hint if there are NPCs nearby
        if is_near_npc():
            hint_text = font.render("Press SPACE to continue", True, (200, 200, 200))
            screen.blit(hint_text, (dialog_x + DIALOG_WIDTH - hint_text.get_width() - 10, dialog_y + DIALOG_HEIGHT - hint_text.get_height() - 5))

# Add this function to draw the intro scene
def draw_intro_scene():
    screen.blit(flower_bg_img, (0, 0))
    screen.blit(door_img, (intro_door_pos[0], intro_door_pos[1]))
    screen.blit(player_img, (player_pos[0], player_pos[1]))
    
    if not player_falling:
        message = font.render("Press SPACE to enter the door", True, BLACK)
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 50))

def create_button(x, y, width, height, text, color, hover_color):
    return {
        "rect": pygame.Rect(x, y, width, height),
        "text": text,
        "color": color,
        "hover_color": hover_color,
        "is_hovered": False
    }

def draw_button(button):
    color = button["hover_color"] if button["is_hovered"] else button["color"]
    pygame.draw.rect(screen, color, button["rect"])
    pygame.draw.rect(screen, BLACK, button["rect"], 2)  # Border
    
    text_surface = font.render(button["text"], True, BLACK)
    text_rect = text_surface.get_rect(center=button["rect"].center)
    screen.blit(text_surface, text_rect)

# Add this function to load high scores
def load_high_scores():
    global high_scores
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as file:
                high_scores = []
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        score_time = float(parts[0])
                        date = parts[1]
                        high_scores.append((score_time, date))
                high_scores.sort()  # Sort by time (fastest first)
        except:
            high_scores = []
    else:
        high_scores = []

# Add this function to save a new high score
def save_high_score(completion_time):
    global high_scores
    current_date = time.strftime("%Y-%m-%d")
    high_scores.append((completion_time, current_date))
    high_scores.sort()  # Sort by time (fastest first)
    high_scores = high_scores[:10]  # Keep only top 10
    
    try:
        with open(SCORES_FILE, 'w') as file:
            for score in high_scores:
                file.write(f"{score[0]},{score[1]}\n")
    except:
        print("Error saving high scores")

# Add this function to format time
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:06.3f}"

# Update the show_victory_screen function for better leaderboard display
def show_victory_screen():
    global high_scores
    
    # Save the current completion time
    completion_time = elapsed_time
    save_high_score(completion_time)
    
    # Create buttons
    button_width, button_height = 200, 60
    play_again_button = create_button(
        WIDTH // 2 - button_width - 20, 
        HEIGHT - 100, 
        button_width, 
        button_height, 
        "Play Again", 
        (100, 200, 100),  # Green
        (150, 255, 150)   # Light green on hover
    )
    
    exit_button = create_button(
        WIDTH // 2 + 20, 
        HEIGHT - 100, 
        button_width, 
        button_height, 
        "Exit", 
        (200, 100, 100),  # Red
        (255, 150, 150)   # Light red on hover
    )
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
                
            # Handle mouse hover
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                play_again_button["is_hovered"] = play_again_button["rect"].collidepoint(mouse_pos)
                exit_button["is_hovered"] = exit_button["rect"].collidepoint(mouse_pos)
                
            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button["rect"].collidepoint(mouse_pos):
                    return "play_again"
                if exit_button["rect"].collidepoint(mouse_pos):
                    return "exit"
        
        # Draw victory screen
        screen.blit(victory_img, (0, 0))
        
        # Draw congratulations text
        congrats_text = dialog_font.render("Congratulations! You've completed the game!", True, WHITE)
        screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, HEIGHT // 2 - 180))
        
        # Draw completion time
        time_text = dialog_font.render(f"Your Time: {format_time(completion_time)}", True, WHITE)
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 - 140))
        
        # Create leaderboard background
        leaderboard_width = 500
        leaderboard_height = 350
        leaderboard_x = (WIDTH - leaderboard_width) // 2
        leaderboard_y = HEIGHT // 2 - 100
        
        leaderboard_bg = pygame.Surface((leaderboard_width, leaderboard_height), pygame.SRCALPHA)
        leaderboard_bg.fill((0, 0, 0, 160))  # Semi-transparent black
        screen.blit(leaderboard_bg, (leaderboard_x, leaderboard_y))
        
        # Add border to leaderboard
        pygame.draw.rect(screen, (255, 215, 0), (leaderboard_x, leaderboard_y, leaderboard_width, leaderboard_height), 2)
        
        # Draw leaderboard title
        title_text = dialog_font.render("TOP 10 SPEEDRUNS", True, (255, 215, 0))  # Gold color
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, leaderboard_y + 10))
        
        # Draw header line
        pygame.draw.line(screen, (255, 215, 0), 
                       (leaderboard_x + 20, leaderboard_y + 50),
                       (leaderboard_x + leaderboard_width - 20, leaderboard_y + 50), 2)
        
        # Draw table headers
        rank_text = dialog_font.render("Rank", True, WHITE)
        time_header = dialog_font.render("Time", True, WHITE)
        date_header = dialog_font.render("Date", True, WHITE)
        
        screen.blit(rank_text, (leaderboard_x + 40, leaderboard_y + 60))
        screen.blit(time_header, (leaderboard_x + 150, leaderboard_y + 60))
        screen.blit(date_header, (leaderboard_x + 300, leaderboard_y + 60))
        
        # Draw scores
        y_offset = leaderboard_y + 100
        for i, score in enumerate(high_scores[:10]):
            # Highlight current score
            text_color = (255, 255, 0) if abs(score[0] - completion_time) < 0.001 else WHITE
            
            rank_text = dialog_font.render(f"{i+1}.", True, text_color)
            score_text = dialog_font.render(f"{format_time(score[0])}", True, text_color)
            date_text = dialog_font.render(f"{score[1]}", True, text_color)
            
            screen.blit(rank_text, (leaderboard_x + 40, y_offset))
            screen.blit(score_text, (leaderboard_x + 150, y_offset))
            screen.blit(date_text, (leaderboard_x + 300, y_offset))
            
            y_offset += 30
            
            # Add subtle separator line between entries
            if i < 9:  # Don't draw after the last entry
                pygame.draw.line(screen, (100, 100, 100), 
                               (leaderboard_x + 30, y_offset - 15),
                               (leaderboard_x + leaderboard_width - 30, y_offset - 15), 1)
        
        # Draw buttons
        draw_button(play_again_button)
        draw_button(exit_button)
        
        pygame.display.flip()
        clock.tick(60)
    
    return "exit"  # Default return if loop exits

# Add this new function to draw game info in a styled panel
def draw_game_info():
    # Create info panel with semi-transparent background
    info_width = int(WIDTH * 0.25)
    info_height = int(HEIGHT * 0.2)
    info_x = 10
    info_y = 10
    
    info_panel = pygame.Surface((info_width, info_height), pygame.SRCALPHA)
    info_panel.fill((50, 50, 50, 160))  # Semi-transparent dark gray
    
    # Add border
    pygame.draw.rect(info_panel, WHITE, (0, 0, info_width, info_height), 2)
    
    # Draw panel
    screen.blit(info_panel, (info_x, info_y))
    
    # Draw text with padding
    padding = 10
    line_height = 30
    
    # Game info lines
    info_lines = [
        f"Health: {player_health}",
        f"Level: {current_level}",
        f"Time: {format_time(elapsed_time)}",
        f"Room: {current_room.capitalize()}"
    ]
    
    for i, line in enumerate(info_lines):
        text_surface = dialog_font.render(line, True, WHITE)
        screen.blit(text_surface, (info_x + padding, info_y + padding + i * line_height))
    
    # Add attack cooldown if active
    if player_attack_cooldown > 0:
        cooldown_text = dialog_font.render(f"Attack CD: {player_attack_cooldown // 6 + 1}", True, (255, 150, 150))
        screen.blit(cooldown_text, (info_x + padding, info_y + padding + len(info_lines) * line_height))

# Main game loop
running = True
clock = pygame.time.Clock()
spawn_enemies_for_level(1)
load_high_scores()  # Load high scores at startup
game_start_time = time.time()  # Record start time
game_state = "playing"  # Add a game state variable

while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = time.time() - game_start_time  # Calculate elapsed time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_room == "intro" and is_at_door() and not player_falling:
                    current_room = "level_1"  # Go to first level
                    player_pos = [WIDTH // 2, HEIGHT // 2]
                    print("You entered the main game!")
                elif is_at_door():
                    if len(enemies) == 0 and current_level < MAX_LEVELS:
                        current_level += 1
                        current_room = f"level_{current_level}"
                        player_pos = [50, HEIGHT // 2]
                        enemies = []
                        level_cleared = False  # Reset flag for new level
                        spawn_enemies_for_level(current_level)
                        
                        # Play appropriate music based on level
                        if current_level == 2:  # Start music after first level
                            play_background_music('dungeon')
                        elif current_level == 4 or current_level == 6:  # Boss levels
                            play_background_music('boss')
                        
                        print(f"You entered level {current_level}")
                    elif not level_cleared:
                        print("Defeat all enemies before proceeding!")
                elif current_room.startswith('level_'):
                    npc_message = is_near_npc()
                    if npc_message:
                        message_time = current_time
            elif event.key == pygame.K_RETURN and current_room.startswith('level_') and player_attack_cooldown <= 0:
                result = player_attack()
                player_attack_cooldown = 30
                if result == "victory":
                    # Play victory music
                    play_background_music('victory')
                    game_state = "victory"
            elif event.key == pygame.K_p:  # Press 'P' to spawn a test potion near the player
                test_pos = [player_pos[0] + 50, player_pos[1]]
                spawn_potion(test_pos)
                print("Test potion spawned near player!")

    # Handle player falling in intro scene
    if current_room == "intro":
        if player_falling:
            player_pos[1] += player_fall_speed
            if player_pos[1] >= HEIGHT // 2 - player_size // 2:
                player_falling = False
                player_pos[1] = HEIGHT // 2 - player_size // 2
        
        # Only allow movement after falling is complete
        if not player_falling:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_pos[0] -= player_speed
                player_direction = 2  # left
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_pos[0] += player_speed
                player_direction = 0  # right
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_pos[1] -= player_speed
                player_direction = 3  # up
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player_pos[1] += player_speed
                player_direction = 1  # down
            
        # Keep the player on screen
        player_pos[0] = max(0, min(player_pos[0], WIDTH - player_size))
        player_pos[1] = max(0, min(player_pos[1], HEIGHT - player_size))
    else:
        # Normal key handling for other rooms (the existing key handling code)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_pos[0] -= player_speed
            player_direction = 2  # left
            last_movement_key = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_pos[0] += player_speed
            player_direction = 0  # right
            last_movement_key = 'right'
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_pos[1] -= player_speed
            player_direction = 3  # up
            last_movement_key = 'up'
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_pos[1] += player_speed
            player_direction = 1  # down
            last_movement_key = 'down'

    # After player movement and keeping player on screen
    player_pos[0] = max(0, min(player_pos[0], WIDTH - player_size))
    player_pos[1] = max(0, min(player_pos[1], HEIGHT - player_size))
    
    # Check for potion collection - add this line right after player movement
    collect_potions()

    # Update enemy positions and check collisions
    if current_room.startswith('level_'):
        move_enemies()
        handle_boss_shooting()
        if not check_enemy_collisions() or not update_projectiles():
            running = False

    # Decrease attack cooldown
    if player_attack_cooldown > 0:
        player_attack_cooldown -= 1

    # Update attack animation
    if attack_animation:
        frame, direction = attack_animation
        if frame > 0:
            attack_animation = (frame - 1, direction)
        else:
            attack_animation = None

    # Draw everything
    if game_state == "victory":
        action = show_victory_screen()
        if action == "play_again":
            # Reset game state
            current_level = 1
            current_room = "level_1"
            player_pos = [WIDTH // 2, HEIGHT // 2]
            player_health = 10000
            player_speed = int(6 * SCREEN_SCALE)
            spawn_enemies_for_level(1)
            game_state = "playing"
            game_start_time = time.time()
            play_background_music('dungeon')
        elif action == "exit":
            running = False
    elif current_room == "intro":
        draw_intro_scene()
    else:
        # Choose appropriate background based on level
        if current_room == "level_1":
            screen.blit(flower_bg_img, (0, 0))  # Use flower background for level 1
        elif current_level == "level_2":
            screen.blit(flower_bg_img2, (0, 0))
        elif current_level > 4:  # Use dungeon background for levels 5 and 6
            screen.blit(dungeon_bg_img, (0, 0))
        else:
            screen.blit(bg_img, (0, 0))  # Use regular background for other levels
        
        if current_room.startswith('level_'):
            draw_npcs()
            draw_enemies()
            draw_potions()
            draw_projectiles()
        draw_door()
        draw_player()
        draw_attack()
        draw_messages()

    # Draw game info panel instead of individual text elements
    draw_game_info()
    
    # Draw NPC dialog
    draw_npc_dialog()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

