import random
import math
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.jpg")

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font("Middletown.ttf", 32)

textX = 10
textY = 10

# Game Over Text
game_over_font = pygame.font.Font("Middletown.ttf", 64)


def display_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (240, 128, 128))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (220, 270))


# Button

buttonImg = pygame.image.load("play_again.png")


def button():
    screen.blit(buttonImg, (270, 280))


# Mouse
mouse_pos = []
mouseX = 0
mouseY = 0


# Speed of objects

def speed_control():
    speed = 0
    global play_again
    if play_again:
        speed += 4
    return speed


def speed_control_bullet():
    speed = 0
    global play_again
    if play_again:
        speed += 10
    return speed


# Player
playerImg = pygame.image.load("Spaceship.png")
playerX = 380
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Invader
invaderImg = []
invaderX = []
invaderY = []
invaderX_change = []
invaderY_change = []
num_of_invaders = 9

for i in range(num_of_invaders):
    invaderImg.append(pygame.image.load("invaders.png"))
    invaderX.append(random.randint(0, 736))
    invaderY.append(random.randint(50, 150))
    invaderX_change.append(0.7)
    invaderY_change.append(40)


def invader(x, y, i):
    screen.blit(invaderImg[i], (x, y))


# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(invaderX, invaderY, bulletX, bulletY):
    distance = math.sqrt((math.pow(invaderX - bulletX, 2)) + (math.pow(invaderY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop

play_again = False
running = True

# For anything that has to remain on the screen
while running:

    # RGB
    screen.fill((0, 0, 0))
    # background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # When keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -(0.3 + speed_control())
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3 + speed_control()
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Cursor Movement

            mouse_pos += list(pygame.mouse.get_pos())
            mouseX = mouse_pos[0]
            mouseY = mouse_pos[1]
            if mouseX in range(290, 500) and mouseY in range(395, 450):
                play_again = True
            mouse_pos = []

    # Boundaries
    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0

    playerX += playerX_change

    for i in range(num_of_invaders):
        # Enemy Movement
        if invaderY[i] > 440:
            for j in range(num_of_invaders):
                invaderY[j] = 2000
            game_over()
            button()
            if play_again:
                score_value = 0
                screen.blit(background, (0, 0))
                for k in range(num_of_invaders):
                    invaderY[k] = random.randint(50, 150)
                play_again = False
            else:
                break

        if invaderX[i] >= 736:
            invaderX_change[i] = -(0.7 + speed_control())
            invaderY[i] += invaderY_change[i]
        elif invaderX[i] <= 0:
            invaderX_change[i] = 0.7 + speed_control()
            invaderY[i] += invaderY_change[i]

        invaderX[i] += invaderX_change[i]
        # Collision Activity
        collision = isCollision(invaderX[i], invaderY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            invaderX[i] = random.randint(0, 736)
            invaderY[i] = random.randint(50, 150)

        invader(invaderX[i], invaderY[i], i)
    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change + speed_control_bullet()
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    player(playerX, playerY)
    display_score(textX, textY)
    pygame.display.update()
