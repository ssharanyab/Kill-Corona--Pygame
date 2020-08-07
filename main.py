import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# background
mixer.music.load('background.wav')
mixer.music.play(-1)


# Title and Icon
pygame.display.set_caption("KILL CORONA")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# tap
tapImg = pygame.image.load('tap.png')
tapX = 370
tapY = 50
tapX_change = 0

# corona
coronaImg = []
coronaX = []
coronaY = []
coronaX_change = []
coronaY_change = []
num_of_corona = 3

for i in range(num_of_corona):
    coronaImg.append(pygame.image.load('corona.png'))
    coronaX.append(random.randint(20, 780))
    coronaY.append(random.randint(200, 220))
    coronaX_change.append(4)
    coronaY_change.append(4)

# drop
dropImg = pygame.image.load('drop.png')
dropX = 0
dropY = 150
dropX_change = 0
dropY_change = 1
drop_state = "ready"  # Ready - No drop on screen

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over
over_text = pygame.font.Font('freesansbold.ttf', 72)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render("Game over ", True, (0, 0, 0))
    screen.blit(over_text, (300, 250))


def tap(x, y):
    screen.blit(tapImg, (x, y))


def corona(x, y, i):
    screen.blit(coronaImg[i], (x, y))


def fire_drop(x, y):
    global drop_state
    drop_state = "fire"
    screen.blit(dropImg, (x + 16, y + 10))


def isCollision(coronaX, coronaY, dropX, dropY):
    distance = math.sqrt((math.pow(coronaX - dropX, 2)) + (math.pow(coronaY - dropY, 2)))
    if distance < 27:
        return True


# Game Loop
running = True
while running:
    # Adding colour to screen
    screen.fill((255, 228, 181))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tapX_change = -5
            if event.key == pygame.K_RIGHT:
                tapX_change = 5
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                if drop_state is "ready":
                    dropX = tapX
                    fire_drop(dropX, dropY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                tapX_change = 0

    # tap movement
    tapX += tapX_change
    if tapX <= 0:
        tapX = 0
    elif tapX >= 690:
        tapX = 690

    # corona movement
    for i in range(num_of_corona):

        # Game Over
        if coronaY[i] > 400:
            for j in range(num_of_corona):
                coronaY[j] = 2000
            game_over_text()
            break
        coronaX[i] += coronaX_change[i]
        if coronaX[i] <= 0:
            coronaX_change[i] = 1
            coronaY[i] += coronaY_change[i]
        elif coronaX[i] >= 736:
            coronaX_change[i] = -1
            coronaY[i] += coronaY_change[i]
        # Collision
        collision = isCollision(coronaX[i], coronaY[i], dropX, dropY)
        if collision:
            dropY = 20
            drop_state = "ready"
            score_value += 1
            coronaX[i] = random.randint(0, 736)
            coronaY[i] = random.randint(200, 220)
        corona(coronaX[i], coronaY[i], i)

    # drop movement
    if dropY >= 600:
        dropY = 150
        drop_state = "ready"
    if drop_state is "fire":
        fire_drop(dropX, dropY)
        dropY += dropY_change

    tap(tapX, tapY)
    show_score(textX, textY)
    pygame.display.update()
