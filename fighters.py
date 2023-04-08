import pygame
import random
import base64
import zlib
import io
import bytes_data


# initialize pygame
def get_bytes(b64):
    decoded_bytes = base64.b64decode(b64)
    decoded_bytes = zlib.decompress(decoded_bytes)
    return io.BytesIO(decoded_bytes)


pygame.init()

# set the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_LOW_SPEED = 3
PLAYER_HIGHSPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set the game title
pygame.display.set_caption("Flight Fighter")

# set the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255,165,0)
RED = (255, 0, 0)

# set the player and enemy variables
player_x = 350
player_y = 500
player_width = 50
player_height = 50
player_bullet_speed = 10
player_speed = PLAYER_HIGHSPEED
player_bullets = []

enemy_width = 50
enemy_height = 50
enemy_speed = 2
enemy_bullet_speed = 3
enemy_bullets = []

bullet_width = 10
bullet_height = 20
bullet_image = pygame.Surface((bullet_width, bullet_height))
bullet_image.fill(ORANGE)

game_over_font = pygame.font.SysFont(None, 36)

 # create the player and enemy sprites
#player = pygame.Rect(player_x, player_y, player_width, player_height)
jet_width, jet_height = 50, 50
player_jet = pygame.image.load(get_bytes(bytes_data.player_jet_img_b64)).convert_alpha()
enemy_jet = pygame.image.load(get_bytes(bytes_data.enemy_jet_img_b64)).convert_alpha()
player_jet = pygame.transform.scale(player_jet, (jet_width, jet_height))
enemy_jet = pygame.transform.scale(enemy_jet, (jet_width, jet_height))

enemy_list = []
score = 0
font = pygame.font.SysFont(None, 30)

def draw_text(window, text, color, x, y):
    img = font.render(text, True, color)
    window.blit(img, (x, y))


def refresh_enemy():
    n = random.randint(5, 50)
    for i in range(n):
        enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
        enemy_y = random.randint(0, 200)
        enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        enemy_list.append(enemy)

# Load sounds
pygame.mixer.init()
pygame.mixer.music.load(get_bytes( bytes_data.raiden2))
pygame.mixer.music.play(-1)  # Play music indefinitely
pygame.mixer.music.set_volume(1)

clock = pygame.time.Clock()
game_over = False
while True:
    # handle events
    if not enemy_list:
        refresh_enemy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if game_over:
        game_over_text = game_over_font.render("Game Over. Press R to restart, or Q to quit.", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        keys = pygame.key.get_pressed()
        #all_keys = [keys[i] for i in range(512)]
        #if any(all_keys):
        #    print(all_keys.index(True))
        if keys[114]:
            enemy_list = []
            enemy_bullets = []
            game_over = False
            score = 0
            player_bullets = []
            continue
        elif keys[113]:
            # Quit the game
            break
    else:

        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_SHIFT:
            player_speed = PLAYER_LOW_SPEED
        else:
            player_speed = PLAYER_HIGHSPEED
        keys = pygame.key.get_pressed()
        if keys[113]:
            break
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 50:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - 50:
            player_y += player_speed
        if keys[pygame.K_z]:
            player_bullet = pygame.Rect(player_x + player_width / 2 - 2, player_y - 10, 5, 10)
            player_bullets.append(player_bullet)

        # handle player bullets
        for bullet in player_bullets:
            bullet.y -= player_bullet_speed
            if bullet.top < 0:
                player_bullets.remove(bullet)
            else:
                for enemy in enemy_list:
                    if bullet.colliderect(enemy):
                        # remove the enemy and the bullet if they collide
                        enemy_list.remove(enemy)
                        if bullet in player_bullets:
                            player_bullets.remove(bullet)
                        score += 10

        # handle enemy movement and shooting
        for enemy in enemy_list:
            enemy.y += enemy_speed

            # add a bullet for the enemy
            if random.randint(0, 50) == 0:
                enemy_bullet = pygame.Rect(enemy.x + enemy_width / 2 - 2, enemy.y + enemy_height, 5, 10)
                enemy_bullets.append(enemy_bullet)

            # check for collisions with the player
            player_rect = pygame.Rect(player_x+jet_width/5*2, player_y+jet_height/5*2, jet_width/5, jet_height/5)
            if player_rect.colliderect(enemy):
                game_over = True

            # remove enemies that have gone off screen
            if enemy.top > SCREEN_HEIGHT:
                enemy_list.remove(enemy)
                enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
                enemy_y = random.randint(0, 200)
                new_enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
                enemy_list.append(new_enemy)

        # handle enemy bullets
        for bullet in enemy_bullets:
            bullet.y += enemy_bullet_speed
            if bullet.colliderect(player_rect):
                game_over = True
            elif bullet.bottom > SCREEN_HEIGHT:
                enemy_bullets.remove(bullet)

        screen.fill(BLACK)
        # draw the player
        # Draw the player jet and enemy jets on the screen
        # draw the enemy bullets
        screen.blit(player_jet, (player_x, player_y))
        judge_point=pygame.Rect(player_x+jet_width/5*2, player_y+jet_height/5*2, jet_width/5, jet_height/5)
        pygame.draw.rect(screen, ORANGE, judge_point)
        for enemy in enemy_list:
            screen.blit(enemy_jet, enemy)
        # draw the player bullets
        for bullet in player_bullets:
            pygame.draw.rect(screen, ORANGE, bullet)
        for bullet in enemy_bullets:
            pygame.draw.rect(screen, RED, bullet)
        draw_text(screen, f"Score: {score}", RED, 10, 10)
        draw_text(screen, "Z: shoot, SHIFT: reduce speed, Q: quit", WHITE, SCREEN_WIDTH/2 - 20, 10)
    pygame.display.update()

    clock.tick(60)

pygame.quit()






