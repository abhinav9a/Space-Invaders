import pygame
import random
from math import sqrt
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the Screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height), pygame.SRCCOLORKEY | pygame.SRCALPHA, 32)

# Load background image, pause, play and replay images
bg = pygame.image.load('images/background.png')
play_icon = pygame.image.load('images/play.png')
pause_icon = pygame.image.load('images/pause.png')
replay_icon = pygame.image.load('images/restart.png')

# Background Music
mixer.music.load('music/background.wav')
mixer.music.play(-1)

# Explosion and Bullet Sound
explosion_sound = mixer.Sound('music/explosion.wav')
bullet_sound = mixer.Sound('music/laser.wav')

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

# Player (SpaceShip)
playerImg = pygame.image.load('images/player.png')
playerX = 368
playerY = 400
player_width = 64
player_height = 64
playerX_change = 0
playerY_change = 0
player_rate = 5

# Enemy
num_of_enemies = 6
enemy_width = 64
enemy_height = 64
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/enemy1.png'))
    enemyX.append(random.randint(0, width - enemy_width))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(3)
    enemyY_change.append(25)

# Bullet
# 'ready' - bullet is not visible
# 'fire' - bullet is visible and moving
bulletImg = pygame.image.load('images/bullet.png')
bullet_width = 32
bullet_height = 32
bulletX = 368
bulletY = 400
# bulletX_change = 0
bulletY_change = 5
bullet_state = 'ready'

# Score
score = 0
scoreX = 10
scoreY = 10
font = pygame.font.Font('freesansbold.ttf', 32)

# GAME OVER
game_state = 'playing'
game_overX = 250
game_overY = 250
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def view_score(x, y):
    score_value = font.render(f'Score : {score}', True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y))


def is_collided(enemyX, enemyY, bulletX, bulletY, collision_distance=27):
    distance = sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < collision_distance:
        explosion_sound.play()
        return True
    return False


def game_over(x, y):
    game_over_text = game_over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(game_over_text, (x, y))


def pause_game():
    global game_state
    game_state = 'pause'
    pause_screen_text = welcome_text_font.render('Game Paused', True, (255, 255, 255))
    screen.blit(bg, (0, 0))
    screen.blit(replay_icon, (336, 284))
    screen.blit(play_icon, (432, 284))
    screen.blit(pause_screen_text, (200, 150))
    pygame.display.update()

    while game_state is 'pause':

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if (336 <= pos[0] <= 368) and (284 <= pos[1] <= 316):
                    game_state = 'playing'
                    restart_game()
                if (432 <= pos[0] <= 464) and (284 <= pos[1] <= 316):
                    game_state = 'playing'


def restart_game():
    global enemyX
    global enemyY
    global score
    global playerX
    global playerY
    score = 0
    playerX = 368
    playerY = 400

    for i in range(num_of_enemies):
        enemyX[i] = (random.randint(0, width - enemy_width))
        enemyY[i] = (random.randint(0, 100))
    player(playerX, playerY)


# ******************************************* WELCOME SCREEN **************************************************
running = False

welcome_text_font = pygame.font.Font('freesansbold.ttf', 64)
welcome_text = welcome_text_font.render('SPACE INVADERS', True, (0, 0, 0))
screen.blit(bg, (0, 0))
screen.blit(play_icon, (384, 284))
screen.blit(welcome_text, (100, 150))
pygame.display.update()

while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # print(pos)
            if (384 <= pos[0] <= 416) and (284 <= pos[1] <= 316):
                running = True

# ********************************************** GAME LOOP ****************************************************

while running:
    # Background Image
    screen.blit(bg, (0, 0))
    # Pause Image
    screen.blit(pause_icon, (758, 10))
    # Change mouse cursor
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    # Checking for Key and Mouse Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        # **************** SpaceShip Movement Detection ****************
        # Key press
        if event.type == pygame.KEYDOWN:
            # UP arrow key
            if event.key == pygame.K_UP:
                playerY_change = -player_rate
            # DOWN arrow key
            if event.key == pygame.K_DOWN:
                playerY_change = player_rate
            # LEFT arrow key
            if event.key == pygame.K_LEFT:
                playerX_change = -player_rate
            # RIGHT arrow key
            if event.key == pygame.K_RIGHT:
                playerX_change = player_rate

            # ************************ Fire Bullet ******************************
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    bulletY = playerY
                    bullet_sound.play()
                    fire(bulletX, playerY)

        # Key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

        # Mouse Events
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if (pos[0] >= 755) and (pos[1] <= 45):
                # print(f'Mouse clicked at : {pos}')
                pause_game()

    # ******************************* Moving spaceship *******************************
    playerX += playerX_change
    playerY += playerY_change

    # Defining boundary to avoid the SPACESHIP from moving out of the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= (width - player_width):
        playerX = width - player_width
    if playerY <= 0:
        playerY = 0
    elif playerY >= (height - player_height):
        playerY = height - player_height

    # ****************************** Enemy Movement **********************************
    if game_state is 'playing':
        for i in range(num_of_enemies):
            # Moving enemy
            enemyX[i] += enemyX_change[i]

            # Defining boundary to avoid the ENEMY from moving out of the screen
            if (enemyX[i] <= 0) or (enemyX[i] >= (width - enemy_width)):
                enemyX_change[i] *= -1
                enemyY[i] += enemyY_change[i]
            # Respawn enemy if enemy moves beyond screen height
            if enemyY[i] >= height:
                enemyX[i] = random.randint(0, width - enemy_width)
                enemyY[i] = random.randint(0, 100)

            # ************************ Collision detection between bullet and enemy ***************************
            collision = is_collided(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision and bullet_state is 'fire':
                bullet_state = 'ready'
                score += 1
                bulletY = playerY
                enemyX[i] = random.randint(0, width - enemy_width)
                enemyY[i] = random.randint(0, 100)
                # print(score)

            enemy(enemyX[i], enemyY[i], i)

            # ********************************** Game Over ****************************************
            spaceship_collision = is_collided(enemyX[i], enemyY[i], playerX, playerY, 50)
            if spaceship_collision:
                game_state = 'game over'
                for j in range(num_of_enemies):
                    enemyX_change[j] = 0
                    enemyY_change[j] = 0
                game_over(game_overX, game_overY)
                break

    # ************************** Moving Bullet ********************************
    if bulletY <= 0:
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # Drawing the player on the screen
    player(playerX, playerY)

    # Drawing score on the screen
    view_score(scoreX, scoreY)

    # Game Over
    if game_state is 'game over':
        for i in range(num_of_enemies):
            enemy(enemyX[i], enemyY[i], i)
        game_over(game_overX, game_overY)

    # Update screen
    pygame.display.update()
