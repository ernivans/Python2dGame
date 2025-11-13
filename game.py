import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight Adventure with Enemies")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
player_image = pygame.image.load("knight.png")
player_size = 50
player_image = pygame.transform.scale(player_image, (player_size, player_size))

chest_image = pygame.image.load("chest.png")
chest_size = 40
chest_image = pygame.transform.scale(chest_image, (chest_size, chest_size))

enemy_image = pygame.image.load("enemy.png")
enemy_size = 50
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

fireball_image = pygame.image.load("fireball.png")
fireball_size = 20
fireball_image = pygame.transform.scale(fireball_image, (fireball_size, fireball_size))

# Player setup
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5
player_health = 3

# Chest setup
chest_x = random.randint(0, WIDTH - chest_size)
chest_y = random.randint(0, HEIGHT - chest_size)

# Enemy setup
num_enemies = 3
enemies = []
for _ in range(num_enemies):
    x = random.randint(0, WIDTH - enemy_size)
    y = random.randint(0, HEIGHT - enemy_size)
    enemies.append({'x': x, 'y': y, 'dir_x': random.choice([-2, 2]), 'dir_y': random.choice([-2, 2])})

# Fireballs
fireballs = []

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed

    # Check collision with chest
    if (player_x < chest_x + chest_size and player_x + player_size > chest_x and
        player_y < chest_y + chest_size and player_y + player_size > chest_y):
        score += 1
        chest_x = random.randint(0, WIDTH - chest_size)
        chest_y = random.randint(0, HEIGHT - chest_size)

    # Move enemies
    for enemy in enemies:
        enemy['x'] += enemy['dir_x']
        enemy['y'] += enemy['dir_y']

        # Bounce off walls
        if enemy['x'] <= 0 or enemy['x'] >= WIDTH - enemy_size:
            enemy['dir_x'] *= -1
        if enemy['y'] <= 0 or enemy['y'] >= HEIGHT - enemy_size:
            enemy['dir_y'] *= -1

        # Randomly shoot fireballs
        if random.randint(0, 100) < 2:  # 2% chance per frame
            fireballs.append({'x': enemy['x'] + enemy_size//2, 
                              'y': enemy['y'] + enemy_size//2, 
                              'dir_x': (player_x - enemy['x'])/60, 
                              'dir_y': (player_y - enemy['y'])/60})

        screen.blit(enemy_image, (enemy['x'], enemy['y']))

    # Move fireballs
    for fireball in fireballs[:]:
        fireball['x'] += fireball['dir_x']
        fireball['y'] += fireball['dir_y']

        # Remove fireball if off screen
        if (fireball['x'] < 0 or fireball['x'] > WIDTH or
            fireball['y'] < 0 or fireball['y'] > HEIGHT):
            fireballs.remove(fireball)
            continue

        # Check collision with player
        if (player_x < fireball['x'] + fireball_size and player_x + player_size > fireball['x'] and
            player_y < fireball['y'] + fireball_size and player_y + player_size > fireball['y']):
            player_health -= 1
            fireballs.remove(fireball)
            if player_health <= 0:
                running = False
            continue

        screen.blit(fireball_image, (fireball['x'], fireball['y']))

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw chest
    screen.blit(chest_image, (chest_x, chest_y))

    # Draw score and health
    score_text = font.render(f"Score: {score}  Health: {player_health}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
