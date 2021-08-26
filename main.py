from typing import List

import pygame
import random
import math

pygame.init()

# Dimensions
height = 600
width = 800

# Create the screen
screen = pygame.display.set_mode((width, height))

# Background
background = pygame.image.load('background.png')
bg = pygame.transform.scale(background, (width, height))
bgY_change = 0

# Title and Icon
pygame.display.set_caption("Fight Against Covid")
icon = pygame.image.load('infected-2.png')  # enemies
pygame.display.set_icon(icon)

# Player
playImg = pygame.image.load('boy.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('infected-1.png'))
    enemyX.append(random.randint(0, width))
    enemyY.append(random.randint(50, height / 2))
    enemyX_change.append(1)
    enemyY_change.append(40)

# life
life = 5
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# score
score = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
scoreTextX = 10
scoreTextY = 40

# font for Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_life(x, y):
    life_value = font.render("Lives: " + str(life), True, (255, 255, 255))
    screen.blit(life_value, (x, y))

def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))

def GameOver_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt((math.pow(enemyX - playerX, 2)) + math.pow(enemyY - playerY, 2))
    if distance < 40:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # Increase score consistently until game ends
    if life > 0:
        score += 1

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, bgY_change))
    screen.blit(background, (0, height + bgY_change))

    if bgY_change == -height:
        screen.blit(background, (0, height + bgY_change))
        bgY_change = 0

    # use this variable to control how fast the background is scrolling
    bgY_change -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:

            # sets event key to equal left and right keys
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_UP:
                playerY_change = -0.5
            if event.key == pygame.K_DOWN:
                playerY_change = 0.5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.KEYUP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # 5 = 5 + -0.1 -> 5 = 5- 0.1
    # 5 = 5 + 0.1
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    elif playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Enemy Movement
    for i in range(num_of_enemies):

        #Game Over
        if life ==0 :
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            GameOver_text()
            break
        # Update horizontal position of enemy.
        enemyX[i] += enemyX_change[i]

        # Update vertical position of enemy.
        if enemyX[i] <= 0:
            enemyX_change[i] = .5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -.5
            enemyY[i] += enemyY_change[i]

        # Respawn enemy if fallen off the screen. And add even more enemies.
        if enemyY[i] > height + 32:  # TO-DO: Need to refactor to avoid hard-coding values throughout this file.
            enemyY[i] = 0
            if num_of_enemies < 16:
                num_of_enemies += 1
                enemyImg.append(pygame.image.load(f'infected-{random.randint(1, 4)}.png'))
                enemyX.append(random.randint(0, width))
                enemyY.append(0)
                enemyX_change.append(random.randint(1, num_of_enemies))
                enemyY_change.append(random.randint(40, 50))

        # Collision check
        collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if collision:
            playerY = 480
            player_state = "ready"
            life -= 1
            print(life)
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_life(textX, textY)
    show_score(scoreTextX, scoreTextY)
    pygame.display.update()
