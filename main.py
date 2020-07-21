import pygame
import random
import math

# initialize game
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Go Corona Go")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Tap
tapImg = pygame.image.load('tap.png')
tapX = 480
tapY = 20
tapX_change = 0

# Virus
virusImg = []
virusX = []
virusY = []
virusX_change = []
virusY_change = []
num_of_virus = 2

for i in range(num_of_virus):
    virusImg.append(pygame.image.load('corona.png'))
    virusX.append(random.randint(20, 780))
    virusY.append(random.randint(50, 150))
    virusX_change.append(2)
    virusY_change.append(40)

# Drop
dropImg = pygame.image.load('drop.png')
dropX = 0
dropY = 20
dropX_change = 0
dropY_change = 10
drop_state = "ready"

# Score
score_value = 0
font = pygame.font.SysFont("comicsansms", 32)
textX = 10
textY = 10

# Game over
over_text = pygame.font.SysFont("comicsansms", 80)


# Show Score
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


# Show Game over text
def game_over_text():
    over_text = font.render("Game over", True, (0, 0, 0))
    screen.blit(over_text, (300, 250))


# Draw Tap
def tap(x, y):
    screen.blit(tapImg, (x, y))


# Draw virus
def virus(x, y, i):
    screen.blit(virusImg[i], (x, y))


# Destroy using drop
def drop(x, y):
    global drop_state
    drop_state = "destroy"
    screen.blit(dropImg, (x + 15, y + 15))


def isCollision(virusX, virusY, dropX, dropY):
    distance = math.sqrt((math.pow(dropX- virusX,2))+(math.pow(dropY - virusY, 2)))
    if distance < 120:
        return True


# Game Loop
running = True
while running:
    # Screen background colour
    screen.fill((224, 172, 105))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tapX_change = -2
            if event.key == pygame.K_RIGHT:
                tapX_change = +2
            if event.key == pygame.K_DOWN or event.key == pygame.K_SPACE:
                if drop_state is "ready":
                    dropX = tapX
                    drop(dropX, dropY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                tapX_change = 0

    # Tap movement
    tapX += tapX_change
    if tapX <= 0:
        tapX = 0
    if tapX >= 700:
        tapX = 700

    # Virus movement
    for i in range(num_of_virus):
        # Game over
        if virusY[i] > 400:
            for j in range(num_of_virus):
                virusY[j] = 2000
            game_over_text()
            break
        virusX[i] += virusX_change[i]
        if virusX[i] <= 0:
            virusX_change[i] = 1
            virusY[i] += virusY_change[i]
        elif virusX[i] >= 730:
            virusX_change[i] = -1
            virusY[i] += virusY_change[i]
        # Collision
        collision = isCollision(virusX[i], virusY[i], dropX, dropY)
        if collision:
            dropY = 20
            drop_state = "ready"
            score_value += 1
            virusX[i] = random.randint(0, 736)
            virusY[i] = random.randint(50, 150)
        virus(virusX[i], virusY[i], i)

    # Drop movement
    if dropY <= 480:
        dropY = 20
        drop_state = "ready"
    if drop_state is "destroy":
        drop(dropX, dropY)
        dropY -= dropY_change

    tap(tapX, tapY)
    show_score(textX, textY)
    pygame.display.update()

