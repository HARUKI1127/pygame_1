import pygame
from pygame import mixer
import random
import math

# Initialize pygame
pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load("enemy.png")
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change = 4
enemyY_change = 40

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 5
bullet_state = "ready"

# Score & Life
score_value = 0
player_life = 3

# Fonts
font = pygame.font.SysFont(None, 32)
over_font = pygame.font.SysFont(None, 64)

# Draw player
def player(x, y):
    screen.blit(playerImg, (x, y))

# Draw enemy
def enemy(x, y):
    screen.blit(enemyImg, (x, y))

# Fire bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Collision detection
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < 27

# Show score
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Show life
def show_life(x, y):
    life = font.render("Life : " + str(player_life), True, (255, 255, 255))
    screen.blit(life, (x, y))

# Game over text
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (230, 250))

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -4
        enemyY += enemyY_change

    # Enemy reaches bottom → life -1
    if enemyY > 440:
        player_life -= 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

        if player_life <= 0:
            game_over_text()
            pygame.display.update()
            pygame.time.delay(3000)
            running = False

    # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score_value += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    enemy(enemyX, enemyY)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Draw UI
    show_score(20, 20)
    show_life(650, 20)
    player(playerX, playerY)

    pygame.display.update()
