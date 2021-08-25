from typing import List

import pygame
import random
import math

pygame.init()
#dimensions 
height = 600
width = 800

# create the screen
screen = pygame.display.set_mode((width, height))

# Background
background = pygame.image.load('background.jpg')
bg = pygame.transform.scale(background, (width, height))
bgY_change = 0
# Title and Icon
pygame.display.set_caption("Fight Against Trashers")
icon = pygame.image.load('trash.png')  # enemies
pygame.display.set_icon(icon)

# player
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
num_of_enemies = 6

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load('trash64.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

life = 5

def player(x, y):
    screen.blit(playImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt((math.pow(enemyX - playerX, 2)) + math.pow(enemyY - playerY, 2))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

     # RGB = Red, Green, Blue
    screen.fill((0,0,0))
    # Background Image
    screen.blit(background, (0, bgY_change))
    screen.blit(background, (0, height+bgY_change))

    if bgY_change == -height:
      screen.blit(background, (0, height+bgY_change))
      bgY_change = 0

    #use this variable to control how fast the background is scrolling
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

    if playerX <= 0 or playerY <= 0:
        playerX = 0
        playerY = 0
    elif playerX >= 736 or playerY >= 736:
        playerX = 736
        playerY = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = .5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -.5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i],enemyY[i],playerX,playerY)
        if collision:
            playerY = 480
            player_state = "ready"
            life -= 1
            print(life)
            enemyX = random.randint(0, 800)
            enemyY = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)


    player(playerX, playerY)

    pygame.display.update()
