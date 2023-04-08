import pygame
import random

# Set up Pygame
pygame.init()

# Set up screen dimensions
screen_width = 800
screen_height = 600

# Set up player dimensions
player_width = 64
player_height = 96

# Set up enemy dimensions
enemy_width = 64
enemy_height = 96

# Load images
background = pygame.image.load('background.png')
player_image = pygame.image.load('player.png')
enemy_image = pygame.image.load('enemy.png')
player_image = pygame.transform.scale(player_image, (player_width, player_height))
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
# Set up player initial position
player_x = screen_width // 2
player_y = screen_height - player_height * 4

# Set up player velocity
player_vel = 5

# Set up player jump
is_jumping = False
jump_count = 10

# Set up enemy initial position and velocity
enemy_x = screen_width
enemy_y = screen_height - enemy_height * 4
enemy_vel = 3

# Set up enemy health
enemy_health = 2

# Set up game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Horizontal Fighting Game")

# Set up clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
run = True
while run:
    clock.tick(60)  # Set frame rate to 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Fill the screen with background image
    screen.blit(background, (0, 0))

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_vel
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_vel

    # Handle player jump
    if not is_jumping:
        if keys[pygame.K_UP]:
            is_jumping = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    # Draw player image on screen
    screen.blit(player_image, (player_x, player_y))

    # Handle enemy movement
    enemy_x -= enemy_vel

    # Draw enemy image on screen
    screen.blit(enemy_image, (enemy_x, enemy_y))

    # Check for collisions between player and enemy
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    if player_rect.colliderect(enemy_rect):
        enemy_health -= 1
        if enemy_health <= 0:
            enemy_x = screen_width
            enemy_health = 2

    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()
