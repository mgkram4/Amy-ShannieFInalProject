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

import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Undertale-like RPG")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)
BLUE = (0, 0, 255)  # Added back for enemy color

# Player stats
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 40
player_speed = 6
player_health = 10000
player_damage = 1000
player_attack_cooldown = 15

# Game state
current_level = 1
MAX_LEVELS = 7
current_room = f"level_{current_level}"

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
    "level_1": {"count": 0, "health": 0, "speed": 0, "damage": 0},  # Introduction level
    "level_2": {"count": 2, "health": 50, "speed": 1.2, "damage": 5},  # Basic enemies
    "level_3": {"count": 3, "health": 75, "speed": 1.3, "damage": 8},  # More enemies
    "level_4": {"count": 0, "health": 0, "speed": 0, "damage": 0},  # Checkpoint/warning level
    "level_5": {"count": 1, "health": 200, "speed": 1.5, "damage": 12, "is_boss": True, "name": "Mini Boss", "can_shoot": True},
    "level_6": {"count": 4, "health": 100, "speed": 1.6, "damage": 10},  # Hard enemies
    "level_7": {"count": 1, "health": 500, "speed": 1.8, "damage": 20, "is_boss": True, "name": "Final Boss", "can_shoot": True}
}

# Current level enemies
enemies = []

# Add these near the other game state variables
# Attack animation
attack_animation = None
ATTACK_DURATION = 15  # frames
player_direction = 0  # Add this for tracking player direction
npc_message = None
message_time = 0

# Add to the game state variables
enemy_respawn_timer = 0
ENEMY_RESPAWN_TIME = 5000  # 5 seconds in milliseconds

# Add to game state variables
projectiles = []  # Store active projectiles
PROJECTILE_SPEED = 5
PROJECTILE_SIZE = 10
BOSS_SHOOT_COOLDOWN = 60  # Frames between boss shots

# Add new constants for items/potions
POTION_SIZE = 30
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
main_door_size = [96, 160]  # Increase door size
main_door_rect = pygame.Rect(main_door_pos[0], main_door_pos[1], main_door_size[0], main_door_size[1])

second_door_pos = [50, 300]
second_door_size = [96, 160]  # Increase door size
second_door_rect = pygame.Rect(second_door_pos[0], second_door_pos[1], second_door_size[0], second_door_size[1])

# Load door image after door sizes are defined
door_img = pygame.image.load('assets/door.png')
door_img = pygame.transform.scale(door_img, (main_door_size[0], main_door_size[1]))

# Fish
fish_caught = 0

# Font
font = pygame.font.Font(None, 36)

# Add a flag to track if level is cleared
level_cleared = False

# Add to the image loading section
bg_img = pygame.image.load('assets/bg.png')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))  # Scale to fit screen

def draw_player():
    screen.blit(player_img, (player_pos[0], player_pos[1]))

def draw_fishing_area():
    if current_room == "main":
        pygame.draw.rect(screen, BLUE, fishing_area, 2)

def draw_npcs():
    if current_room.startswith('level_'):  # Check if we're in a level
        if current_room in level_npcs:  # Check if the level has NPCs
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
        frame, direction = attack_animation
        sword_pos = [0, 0]
        rotated_sword = sword_img
        
        if direction == 0:  # right
            sword_pos = [player_pos[0] + player_size, player_pos[1]]
            rotated_sword = sword_img
        elif direction == 1:  # down
            sword_pos = [player_pos[0], player_pos[1] + player_size]
            rotated_sword = pygame.transform.rotate(sword_img, -90)
        elif direction == 2:  # left
            sword_pos = [player_pos[0] - 48, player_pos[1]]
            rotated_sword = pygame.transform.rotate(sword_img, 180)
        elif direction == 3:  # up
            sword_pos = [player_pos[0], player_pos[1] - 48]
            rotated_sword = pygame.transform.rotate(sword_img, 90)
            
        screen.blit(rotated_sword, sword_pos)

def is_in_fishing_area():
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    return player_rect.colliderect(fishing_area)

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
    if current_room == "main":
        return player_rect.colliderect(main_door_rect)
    else:
        return player_rect.colliderect(second_door_rect)

def fish_minigame():
    global fish_caught

    bar_pos = 100
    bar_speed = 15
    green_zone = (370, 440)
    clock = pygame.time.Clock()
    fishing = True
    start_time = pygame.time.get_ticks()

    while fishing:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000  # Convert to seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if green_zone[0] <= bar_pos <= green_zone[1]:
                    fish_caught += 1
                    print("Fish caught!")
                else:
                    print("Fish got away!")
                fishing = False

        screen.fill(WHITE)

        # Draw fishing rod
        pygame.draw.line(screen, BLACK, (50, HEIGHT - 50), (bar_pos + 5, 300), 2)

        # Draw water
        pygame.draw.rect(screen, BLUE, (0, HEIGHT - 100, WIDTH, 100))

        # Draw fishing line
        pygame.draw.line(screen, BLACK, (bar_pos + 5, 300), (bar_pos + 5, HEIGHT - 20), 1)

        # Draw fishing bar
        pygame.draw.rect(screen, BLACK, (100, 300, 600, 50))
        pygame.draw.rect(screen, GREEN, (green_zone[0], 300, green_zone[1] - green_zone[0], 50))
        pygame.draw.rect(screen, RED, (bar_pos, 290, 10, 70))

        # Move the bar
        bar_pos += bar_speed
        if bar_pos <= 100 or bar_pos >= 700:
            bar_speed = -bar_speed

        # Draw timer
        timer_text = font.render(f"Time: {elapsed_time:.1f}s", True, BLACK)
        screen.blit(timer_text, (WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(60)

        # End the minigame after 10 seconds if no fish is caught
        if elapsed_time > 10:
            print("Fish got away!")
            fishing = False

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
            # Show victory screen for final boss
            screen.fill(WHITE)
            win_text = font.render("Congratulations! You defeated the Final Boss!", True, BLACK)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            return True
    return False

def spawn_potion(pos):
    # 70% chance for health potion, 30% chance for speed potion
    potion_type = 'health' if random.random() < 0.7 else 'speed'
    potions.append({
        'type': potion_type,
        'pos': list(pos),
        'rect': pygame.Rect(pos[0], pos[1], POTION_SIZE, POTION_SIZE)
    })

def draw_potions():
    for potion in potions:
        img = health_potion_img if potion['type'] == 'health' else speed_potion_img
        screen.blit(img, potion['pos'])

def collect_potions():
    global player_health, player_speed
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    
    for potion in potions[:]:  # Use a copy of the list to safely remove items
        if player_rect.colliderect(potion['rect']):
            if potion['type'] == 'health':
                player_health = min(10000, player_health + 30)  # Heal 30 HP, max 100
                print("Health restored!")
            elif potion['type'] == 'speed':
                player_speed += 1  # Permanent speed boost
                print("Speed increased!")
            potions.remove(potion)

def player_attack():
    global enemies, attack_animation, enemy_respawn_timer, current_time
    attack_rect = None
    if player_direction == 0:  # right
        attack_rect = pygame.Rect(player_pos[0] + player_size, player_pos[1], 96, player_size)
    elif player_direction == 1:  # down
        attack_rect = pygame.Rect(player_pos[0], player_pos[1] + player_size, player_size, 96)
    elif player_direction == 2:  # left
        attack_rect = pygame.Rect(player_pos[0] - 96, player_pos[1], 96, player_size)
    elif player_direction == 3:  # up
        attack_rect = pygame.Rect(player_pos[0], player_pos[1] - 96, player_size, 96)

    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy["pos"][0], enemy["pos"][1], enemy["size"], enemy["size"])
        if attack_rect.colliderect(enemy_rect):
            enemy["health"] -= player_damage
            print(f"Enemy hit! Enemy health: {enemy['health']}")
            if enemy["health"] <= 0:
                # Spawn potion at enemy's position when defeated
                spawn_potion(enemy["pos"])
                enemies.remove(enemy)
                print(f"{enemy.get('name', 'Enemy')} defeated!")
                if not enemy.get("is_boss"):
                    enemy_respawn_timer = current_time + ENEMY_RESPAWN_TIME

    attack_animation = (ATTACK_DURATION, player_direction)

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

# Add this function before the main game loop
def draw_messages():
    if is_at_door():
        if not level_cleared:
            message = font.render("Defeat all enemies first!", True, RED)
            screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 30))
        elif level_cleared:
            message = font.render("Press SPACE to proceed", True, GREEN)
            screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 30))

# Main game loop
running = True
clock = pygame.time.Clock()
spawn_enemies_for_level(1)

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if is_at_door():
                    if level_cleared and current_level < MAX_LEVELS:
                        current_level += 1
                        current_room = f"level_{current_level}"
                        player_pos = [50, HEIGHT // 2]
                        enemies = []
                        level_cleared = False  # Reset flag for new level
                        spawn_enemies_for_level(current_level)
                        print(f"You entered level {current_level}")
                    elif not level_cleared:
                        print("Defeat all enemies before proceeding!")
                elif current_room.startswith('level_'):
                    npc_message = is_near_npc()
                    if npc_message:
                        message_time = current_time
            elif event.key == pygame.K_RETURN and current_room.startswith('level_') and player_attack_cooldown <= 0:
                player_attack()
                player_attack_cooldown = 30

    # Modified key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_pos[1] += player_speed
        

    # Keep player on screen
    player_pos[0] = max(0, min(player_pos[0], WIDTH - player_size))
    player_pos[1] = max(0, min(player_pos[1], HEIGHT - player_size))

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
    screen.blit(bg_img, (0, 0))  # Draw background first
    if current_room.startswith('level_'):
        draw_npcs()
        draw_enemies()
        draw_potions()
        draw_projectiles()
    draw_door()
    draw_player()
    draw_attack()
    draw_messages()

    # Draw player health
    
    health_text = font.render(f"Health: {player_health}", True, BLACK)
    screen.blit(health_text, (10, 50))

    # Draw room name
    room_text = font.render(f"Current Room: {current_room.capitalize()}", True, BLACK)
    screen.blit(room_text, (WIDTH - 250, 10))

    # Draw NPC message
    if npc_message and current_time - message_time < 3000:  # Display message for 3 seconds
        message_surface = font.render(npc_message, True, BLACK)
        screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, HEIGHT - 50))

    # Draw attack cooldown
    if player_attack_cooldown > 0:
        cooldown_text = font.render(f"Attack Cooldown: {player_attack_cooldown // 6 + 1}", True, BLACK)
        screen.blit(cooldown_text, (WIDTH - 250, 50))

    # Draw level information
    level_text = font.render(f"Level: {current_level}", True, BLACK)
    screen.blit(level_text, (WIDTH - 150, 10))

    # Check for level completion (all enemies defeated)
    if check_level_complete():
        running = False

    # Handle enemy respawning for regular enemies
    if enemy_respawn_timer and current_time >= enemy_respawn_timer:
        if current_room.startswith('level_') and not any(e.get("is_boss") for e in enemies):
            config = enemy_configs[current_room]
            if not config.get("is_boss") and len(enemies) < config["count"]:
                spawn_enemies_for_level(current_level)
        enemy_respawn_timer = 0

    # Check for potion collection
    collect_potions()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()