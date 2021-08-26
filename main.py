import math
from random import randint
import pygame

###################################################### Constants ######################################################

# Messages
GAME_NAME = "Fight Against Covid"
GAME_OVER_MESSAGE = "GAME OVER"

# Assets
GAME_ICON = "infected-2.png"
BACKGROUND = "background.png"
PLAYER = "boy.png"
ENEMIES = [
    "infected-1.png",
    "infected-2.png",
    "infected-3.png",
    "infected-4.png"
]

# Dimensions and Positions
VIEW_HEIGHT = 600
VIEW_WIDTH = 800
VIEW_SIZE = (VIEW_WIDTH, VIEW_HEIGHT)
ENTITY_WIDTH = ENTITY_HEIGHT = 64
LIVES_TEXT_POSITION = (10, 10)
SCORE_TEXT_POSITION = (10, 40)

# Settings
INITIAL_ENEMY_COUNT = 2
MAXIMUM_ENEMY_COUNT = 10
INITIAL_LIVES = 5
INITIAL_SCORE = 0
BACKGROUND_COLOR = (0, 0, 0)  # Black
FONT = ('freesansbold.ttf', 32)
FONT_COLOR = (0, 0, 0)  # Black
BACKGROUND_SCROLL_SPEED = 5
PLAYER_MOVEMENT_SPEED = 5


####################################################### Classes #######################################################

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class GameEntity:
    def __init__(self,
                 sprite_path,
                 position=None,
                 movement_delta=None):
        self.sprite = pygame.image.load(sprite_path)
        self.position = Vector(randint(0, VIEW_WIDTH), randint(0, VIEW_HEIGHT // 4)) if position is None else position
        self.movement_delta = Vector(randint(3, 6), randint(8, 64)) if movement_delta is None else movement_delta


###################################################### Functions ######################################################

def get_random_enemy_sprite():
    return ENEMIES[randint(0, len(ENEMIES) - 1)]


###################################################### Main Logic ######################################################

# Initialize Pygame and settings dependent on Pygame being initialized first.
pygame.init()
font = pygame.font.Font(*FONT)

# Create the window and set its properties.
pygame.init()
pygame.display.set_caption(GAME_NAME)
pygame.display.set_icon(pygame.image.load(GAME_ICON))

# Create the drawing surface and load the background image.
surface = pygame.display.set_mode(VIEW_SIZE)
background_image = pygame.image.load(BACKGROUND)
background_offset = 0

# Create the player.
player = GameEntity(PLAYER, Vector(VIEW_WIDTH // 2, VIEW_HEIGHT // 2), Vector())
life = INITIAL_LIVES
score = INITIAL_SCORE

# Generate an initial set of random enemies.
enemies = [GameEntity(get_random_enemy_sprite()) for _ in range(INITIAL_ENEMY_COUNT)]


#
def is_collision(entity1, entity2):
    distance = math.sqrt((entity1.position.x - entity2.position.x) ** 2 + (entity1.position.y - entity2.position.y) ** 2)
    return distance < max(ENTITY_WIDTH, ENTITY_HEIGHT) // 2


def draw_background():
    global background_offset  # TO-DO: Encapsulate the game logic into a class.
    surface.fill(BACKGROUND_COLOR)
    surface.blit(background_image, (0, background_offset))
    surface.blit(background_image, (0, VIEW_HEIGHT + background_offset))
    if background_offset == -VIEW_HEIGHT:  # Tile the background so that it looks continuous.
        surface.blit(background_image, (0, VIEW_HEIGHT + background_offset))
        background_offset = 0
    else:
        background_offset -= BACKGROUND_SCROLL_SPEED  # Scroll the background.


def draw_entity(entity):
    surface.blit(entity.sprite, (entity.position.x, entity.position.y))


def draw_player():
    draw_entity(player)


def draw_lives():
    surface.blit(font.render(f"Lives: {life}", True, FONT_COLOR), LIVES_TEXT_POSITION)


def draw_score():
    surface.blit(font.render(f"Score: {score}", True, FONT_COLOR), SCORE_TEXT_POSITION)


def draw_end_game():
    rendered_message = font.render(GAME_OVER_MESSAGE, True, (255, 255, 255))
    surface.blit(rendered_message, ((VIEW_WIDTH - rendered_message.get_width()) // 2, (VIEW_HEIGHT - rendered_message.get_height()) // 2))


# Game Loop
clock = pygame.time.Clock()
running = True
game_over = False
while running:
    if not game_over:
        draw_background()

    # Handle events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Update player’s character’s movements depending on the key press state.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.movement_delta.x = -PLAYER_MOVEMENT_SPEED
            elif event.key == pygame.K_RIGHT:
                player.movement_delta.x = PLAYER_MOVEMENT_SPEED
            elif event.key == pygame.K_UP:
                player.movement_delta.y = -PLAYER_MOVEMENT_SPEED
            elif event.key == pygame.K_DOWN:
                player.movement_delta.y = PLAYER_MOVEMENT_SPEED
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.movement_delta.x = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                player.movement_delta.y = 0

    if not game_over:
        # Update the player’s position.
        player.position.x += player.movement_delta.x
        player.position.y += player.movement_delta.y

        if player.position.x <= 0:
            player.position.x = 0
        elif player.position.x >= VIEW_WIDTH - ENTITY_WIDTH:
            player.position.x = VIEW_WIDTH - ENTITY_WIDTH
        elif player.position.y <= 0:
            player.position.y = 0
        elif player.position.y >= VIEW_HEIGHT - ENTITY_HEIGHT:
            player.position.y = VIEW_HEIGHT - ENTITY_HEIGHT

    # Update the enemies’ positions.
    for enemy in enemies:
        if not game_over:
            # Update horizontal position of enemy.
            enemy.position.x += enemy.movement_delta.x

            # Update vertical position of enemy.
            if not 0 <= enemy.position.x <= VIEW_WIDTH - ENTITY_WIDTH:
                enemy.movement_delta.x *= -1
                enemy.position.y += enemy.movement_delta.y

            # Respawn enemy if fallen off the screen. And add even more enemies.
            if enemy.position.y > VIEW_HEIGHT:
                enemy.position.y = 0
                if len(enemies) < MAXIMUM_ENEMY_COUNT:
                    enemies.append(GameEntity(get_random_enemy_sprite()))

            # Check for collision between the player and the enemy.
            if is_collision(player, enemy):
                player.position.y = VIEW_HEIGHT // 2
                enemy.position.y = 0
                life -= 1
                if life < 1:
                    game_over = True

        draw_entity(enemy)

    # Increment the score a little bit for each frame while the game is not over. Otherwise, show “game over”.
    if not game_over:
        score += 1
    else:
        draw_end_game()

    draw_player()
    draw_lives()
    draw_score()

    pygame.display.update()

    clock.tick(60)
