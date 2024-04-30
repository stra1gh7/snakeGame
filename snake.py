# USED PACKAGES
import pygame
import random

# GAME CONSTANTS
snakeSpeed = 7.5
x_axis = 800
y_axis = 800
gridSize = 40

# COLORS
BLACK = pygame.Color(0, 0, 0)
GRAY = pygame.Color(85,85,85)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

# INITIALIZE
pygame.init()
pygame.display.set_caption('Snake game by stra1gh7')
pygame.display.set_icon(pygame.image.load('images\icon.png'))
window = pygame.display.set_mode((x_axis, y_axis))

# POSITIONS (SNAKE/FRUIT)
snakeInitialX = random.randrange(1, (x_axis//gridSize))*gridSize
snakeInitialY = random.randrange(1, (x_axis//gridSize))*gridSize
snakePosition = [snakeInitialX,snakeInitialY] 
snakeBody = [[snakeInitialX, snakeInitialY]]
fruitPosition = [random.randrange(1, (x_axis//gridSize))*gridSize,
                 random.randrange(1, (y_axis//gridSize))*gridSize]
fruitSpawn = True

# DIRECTIONS
direction = ''
changedDirection = direction

score = 0
gameStarted = False

def showScore(choice, color, font, size):
    scoreFont = pygame.font.SysFont(font, size)
    scoreSurface = scoreFont.render('Score: ' + str(score), True, color)
    scoreRect = scoreSurface.get_rect()
    window.blit(scoreSurface, scoreRect)

def displayText(text, color, font, size, x, y):
    font = pygame.font.SysFont(font, size)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.topleft = (x, y)
    window.blit(textSurface, textRect)

def gameOver():
    gameOverFont = pygame.font.SysFont('comic sans', 20)
    gameOverSurface = gameOverFont.render('Final score: ' + str(score), True, RED)
    gameOverRect = gameOverSurface.get_rect()
    gameOverRect.midtop = (x_axis/2, y_axis/4)
    window.blit(gameOverSurface, gameOverRect)
    pygame.display.flip()

    displayText("Play again? (Y/N)", WHITE, 'comic sans', 20, x_axis/2 - 80, y_axis/2)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    resetGame()
                    return
                elif event.key == pygame.K_n:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

def resetGame():
    global snakePosition, snakeBody, fruitPosition, fruitSpawn, direction, changedDirection, score, gameStarted
    snakeInitialX = random.randrange(1, (x_axis//gridSize))*gridSize
    snakeInitialY = random.randrange(1, (x_axis//gridSize))*gridSize

    snakePosition = [snakeInitialX,snakeInitialY] 
    snakeBody = [[snakeInitialX, snakeInitialY]]
    fruitPosition = [random.randrange(1, (x_axis//gridSize))*gridSize,
                     random.randrange(1, (y_axis//gridSize))*gridSize]
    fruitSpawn = True
    direction = ''
    changedDirection = direction
    score = 0
    gameStarted = False

# GAME SCRIPT
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if not gameStarted:
                gameStarted = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_UP:
                changedDirection = 'UP'
            if event.key == pygame.K_DOWN:
                changedDirection = 'DOWN'
            if event.key == pygame.K_RIGHT:
                changedDirection = 'RIGHT'
            if event.key == pygame.K_LEFT:
                changedDirection = 'LEFT'

    if gameStarted:
        if changedDirection == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if changedDirection == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if changedDirection == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        if changedDirection == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        
        if direction == 'UP':
            snakePosition[1] -= gridSize
            if snakePosition[1] < 0:
                snakePosition[1] = y_axis - gridSize

        if direction == 'DOWN':
            snakePosition[1] += gridSize
            if snakePosition[1] >= y_axis:
                snakePosition[1] = 0

        if direction == 'LEFT':
            snakePosition[0] -= gridSize
            if snakePosition[0] < 0:
                snakePosition[0] = x_axis - gridSize

        if direction == 'RIGHT':
            snakePosition[0] += gridSize
            if snakePosition[0] >= x_axis:
                snakePosition[0] = 0

        if [snakePosition[0], snakePosition[1]] in snakeBody[1:]:
            gameOver()

        snakeBody.insert(0, list(snakePosition))

        if snakePosition[0] == fruitPosition[0] and snakePosition[1] == fruitPosition[1]:
            score += 20
            fruitSpawn = False
        else:
            snakeBody.pop()

        if not fruitSpawn:
            fruitPosition = [random.randrange(1, (x_axis//gridSize))*gridSize,
                              random.randrange(1, (y_axis//gridSize))*gridSize]
            
        fruitSpawn = True

        window.fill(BLACK)

        for bodyPosition in snakeBody:
            pygame.draw.rect(window, GRAY, pygame.Rect(bodyPosition[0], bodyPosition[1], gridSize, gridSize))
        pygame.draw.rect(window, RED, pygame.Rect(fruitPosition[0], fruitPosition[1], gridSize, gridSize))
        displayText("Press ESC to exit", WHITE, 'comic sans', 20, 10, y_axis - 30)
        showScore(1, pygame.Color(255,255,255), 'comic sans', 20)
    else:
        window.fill(BLACK)
        displayText("Press ESC to exit", WHITE, 'comic sans', 20, 10, y_axis - 30)
        showScore(1, pygame.Color(255,255,255), 'comic sans', 20)
        pygame.draw.rect(window, GRAY, pygame.Rect(snakePosition[0], snakePosition[1], gridSize, gridSize))
        pygame.draw.rect(window, RED, pygame.Rect(fruitPosition[0], fruitPosition[1], gridSize, gridSize))

    pygame.display.update()

    pygame.time.Clock().tick(snakeSpeed)
