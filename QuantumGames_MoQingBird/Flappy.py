import pygame
import sys
import random
from pygame.constants import SYSTEM_CURSOR_SIZEALL
from pygame.transform import rotate, smoothscale
import textwrap


def rotateBird(bird):
    # rotate a bird
    newBird = pygame.transform.rotozoom(bird, -birdMovement*3, 1)
    return newBird


def birdAnimation():
    # create a function to animate the bird draw rectangles around the flaps so its the same size
    newBird = birdFrames[birdIndex]
    newBirdRectangle = newBird.get_rect(center=(100, birdieRectangle.centery))
    return newBird, newBirdRectangle

# a function to make sure floor is repeated again and again


def draw_floor():
    screen.blit(floorSurface, (floor_x_pos, 700))
    screen.blit(floorSurface, (floor_x_pos + screenWidth, 700))

# function to create pipes


def createPipe():
    #randomPipePosition = random.choice(pipeHeight)
    randomPipePosition = 400  # maybe add 600 in the pipeHeight as well, just for variety
    bottomPipe = pipeSurface.get_rect(midtop=(700, randomPipePosition))
    topPipe = pipeSurface.get_rect(midbottom=(700, randomPipePosition-300))
    return bottomPipe, topPipe

# move the pipes on screen


def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5  # takes all the pipes and it moves them to the left by a little bit
    # despawning the pipes
    visiblePipes = [pipe for pipe in pipes if pipe.right > -50]
    return visiblePipes


def drawPipes(pipes):
    # draw pipes on the background
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipeSurface, pipe)
        else:
            # flipping in the x direction not the y direction
            flipPipe = pygame.transform.flip(pipeSurface, False, True)
            screen.blit(flipPipe, pipe)


def createRing():
    # randomRingPosition = random.choice(pipeHeight) 400,600
    bottomRing = ringSurface.get_rect(midtop=(1200, 500))
    topRing = ringSurface.get_rect(midbottom=(1200, 500-200))
    return bottomRing, topRing


def drawRings(rings):
    # draw pipes on the background
    for ring in rings:
        screen.blit(ringSurface, ring)


def moveRings(rings):
    for ring in rings:
        ring.centerx -= 5  # takes all the rings and it moves them to the left by a little bit
    # despawning the rings
    visibleRings = [ring for ring in rings if ring.right > -50]
    return visibleRings


def checkCollision(pipes):
    # check for collisions
    global canScore
    for pipe in pipes:
        if birdieRectangle.colliderect(pipe):
            buhByeSound.play()
            canScore = True  # when game restarts, canScore is True so that the first pipe the bird crosses can give us a point
            return False
    # we use >= becasue pixel measurements are never precise
    if birdieRectangle.top <= -100 or birdieRectangle.bottom >= 700:
        canScore = True
        return False

    return True


# def checkPassing(rings):  # this function works fine: checks if the bird has passed the ring or not
#     # check for collisions
#     global canScore
#     for ring in rings:
#         if birdieRectangle.colliderect(ring):
#             buhByeSound.play()
#             canScore = True  # when game restarts, canScore is True so that the first pipe the bird crosses can give us a point
#             return False
#     # we use >= becasue pixel measurements are never precise
#     if birdieRectangle.top <= -100 or birdieRectangle.bottom >= 700:
#         canScore = True
#         return False

#     return True

def gameIntro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
            if event.type == pygame.KEYDOWN:  # check if any key is pressed
                if event.key == pygame.K_SPACE:
                    intro = True
                    # overlay
                    overlaySize = (screenWidth, screenHeight)
                    overlaySurface = pygame.Surface(overlaySize)
                    pygame.draw.rect(overlaySurface, pygame.Color(
                        0, 0, 0), overlaySurface.get_rect())
                    overlaySurface.set_alpha(90)
                    screen.blit(overlaySurface, (0, 0))

                    # title
                    titleSurface = gameFont.render(
                        'Welcome to MoQingbird', True, (255, 255, 255))
                    titleRect = titleSurface.get_rect(
                        center=(screenWidth/2, 100))
                    screen.blit(titleSurface, titleRect)

                    # instructions: how do I change font?
                    line1 = 'The gameplay is based on the Stern-Gerlach experiment.The pipes represent a magnet and the bird represents an electron.'
                    line2 = 'After passing through the pipes, the aim is to make the bird pass through either the ring above or below, similar to how the electrons either'
                    line3 = ' display positive spin or negative spin after passing through a magnet in the Stern-Gerlach experiment setup.'
                    line4 = 'Players win a point for every pipe they pass, and the positive and negative spins are also counted.'
                    line5 = ''

                    #message = [line1, line2, line3, line4, line4]
                    # for line in message:
                    #     index = message.index(line)
                    #     # Wrap this text.
                    #     # wrapper = textwrap.TextWrapper(width=5000)
                    #     # wrappedMessage = wrapper.fill(text=message)
                    #     messageSurface = messageFont.render(
                    #         str(line), True, (255, 255, 255))
                    #     messageRect = messageSurface.get_rect(
                    #         midleft=(0, index*10+300))
                    #     screen.blit(messageSurface, messageRect)
                    line1Surface = messageFont.render(
                        line1, True, (255, 255, 255))
                    line1Rect = line1Surface.get_rect(
                        midleft=(50, 300))
                    screen.blit(line1Surface, line1Rect)

                    line2Surface = messageFont.render(
                        line2, True, (255, 255, 255))
                    line2Rect = line2Surface.get_rect(
                        midleft=(50, 350))
                    screen.blit(line2Surface, line2Rect)

                    line3Surface = messageFont.render(
                        line3, True, (255, 255, 255))
                    line3Rect = line3Surface.get_rect(
                        midleft=(50, 400))
                    screen.blit(line3Surface, line3Rect)

                    line4Surface = messageFont.render(
                        line4, True, (255, 255, 255))
                    line4Rect = line4Surface.get_rect(
                        midleft=(50, 450))
                    screen.blit(line4Surface, line4Rect)

                    line5Surface = messageFont.render(
                        line5, True, (255, 255, 255))
                    line5Rect = line5Surface.get_rect(
                        midleft=(50, 500))
                    screen.blit(line5Surface, line5Rect)

                    # end message
                    endMessage = gameFont.render(
                        'Happy flapping!', True, (255, 255, 255))
                    endMessageRect = endMessage.get_rect(
                        center=(screenWidth/2, 700))
                    screen.blit(endMessage, endMessageRect)

                    clock.tick(15)
                    pygame.display.update()


def scoreDisplay(gameState):  # this function works fine: displays all the scores
    # to recognise the state of the game and display high score automatically, based on if the game is over or not.

    if gameState == 'mainGame':
        # anti-aliasing settings here
        scoreSurface = gameFont.render(
            str(int(score)), True, (255, 255, 255))  # score has to be a string to be displayed, which is why we convert score
        scoreRect = scoreSurface.get_rect(center=(screenWidth/2, 100))
        screen.blit(scoreSurface, scoreRect)

    if gameState == 'gameOver':

        # anti-aliasing settings here
        # score has to be a string to be displayed, which is why we convert score
        # we use an f string to pass the integer as a string here

        # adding overlay
        overlaySize = (screenWidth, screenHeight)
        overlaySurface = pygame.Surface(overlaySize)
        pygame.draw.rect(overlaySurface, pygame.Color(
            0, 0, 0), overlaySurface.get_rect())
        overlaySurface.set_alpha(90)
        screen.blit(overlaySurface, (0, 0))

        # adding main score
        scoreSurface = gameFont.render(
            f'Score: {int(score)}', True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center=(screenWidth/2, 100))
        screen.blit(scoreSurface, scoreRect)

        # high score
        highScoreSurface = gameFont.render(
            f'High Score: {int(highScore)}', True, (255, 255, 255))
        highScoreRect = highScoreSurface.get_rect(center=(screenWidth/2, 550))
        screen.blit(highScoreSurface, highScoreRect)

        # positive spin count
        positiveSpinSurface = gameFont.render(
            f'Positive Spin Score: {int(positiveSpin)}', True, (255, 255, 255))  # positiveSpin has to be a string to be displayed, which is why we convert score
        positiveSpinRect = positiveSpinSurface.get_rect(
            center=(screenWidth/2, 300))
        screen.blit(positiveSpinSurface, positiveSpinRect)

        # negative spin count
        negativeSpinSurface = gameFont.render(
            f'Negative Spin Score: {int(negativeSpin)}', True, (255, 255, 255))  # negativeSpin has to be a string to be displayed, which is why we convert score
        negativeSpinRect = negativeSpinSurface.get_rect(
            center=(screenWidth/2, 400))
        screen.blit(negativeSpinSurface, negativeSpinRect)


def updateHighScore(score, highScore):
    # function to update High Score
    if score > highScore:
        highScore = score
    return highScore


def pipeCheck():
    # check if FLappy Bird has passed the pipes:
    global score, canScore
    # we need to make sure the following line of code is triggered only once.
    # hence we update score once, but then we quickly disable updating score feature
    # we need the x position and the x position of the pipes, which is stored in pipeList
    if pipeList:
        for pipe in pipeList:
            if 95 < pipe.centerx < 105 and canScore:  # change this value when you're changing dimensions
                score += 1
                scoreSound.play()
                canScore = False
            if pipe.centerx < 0:
                canScore = True


def upperRingCheck():
    # check if FLappy Bird has passed the rings:
    global score, canScore, positiveSpin
    # we need to make sure the following line of code is triggered only once.
    # hence we update score once, but then we quickly disable updating score feature
    # we need the x position and the x position of the rings, which is stored in ringList
    if ringList:
        for ring in ringList:
            if 105 < ring.centerx < 205 and canScore:  # change this value when you're changing dimensions
                positiveSpin += 1
                scoreSound.play()
                canScore = False
            if ring.centerx < 0:
                canScore = True


def lowerRingCheck():
    # check if FLappy Bird has passed the rings:
    global score, canScore, negativeSpin
    # we need to make sure the following line of code is triggered only once.
    # hence we update score once, but then we quickly disable updating score feature
    # we need the x position and the x position of the rings, which is stored in ringList
    if ringList:
        for ring in ringList:
            if 95 < ring.centerx < 105 and canScore:  # change this value when you're changing dimensions
                negativeSpin += 1
                scoreSound.play()
                canScore = False
            if ring.centerx < 0:
                canScore = True


pygame.init()
# the resolution of the canvas
# this can be changed and accordingly, the floor and other details also need to be altered
screenWidth = 1500
screenHeight = 820  # do not change this

screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

# Font
gameFont = pygame.font.Font(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\CODA\\04B_19.TTF', 40)
messageFont = pygame.font.Font(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\CODA\\Poppins-Light.ttf', 20)

# GAME VARIABLES
gravity = 0.25
birdMovement = 0  # used to move the birdieRectangle down
gameActive = True
score = 0
positiveSpin = 0
negativeSpin = 0
highScore = 0
canScore = True
canPass = True

# background surface: change with a sci-fi background here
backgroundSurface = pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\city_night.gif').convert()  # image to pygame easier file
backgroundSurface = pygame.transform.scale2x(backgroundSurface)

# floor surface
floorSurface = pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\base.png').convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floor_x_pos = 0


# pipes
# maybe add a green pipe generator function, as an additional function

pipeSurface = pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\pipe-silver-small-res.png').convert_alpha()
pipeSurface = pygame.transform.scale2x(pipeSurface)
# pipelist with a lot of rectangles that move left
# using these leftward moving rectangles, we create a game
pipeList = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # an event that is triggered every 1.2s
pipeHeight = [400, 600, 800]  # all the possible heights a pipe can have

# ring
ringSurface = pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\ring-3d-low-res.png').convert_alpha()
ringList = []
SPAWNRING = pygame.USEREVENT
# slight delay than pipes, modify as per convenience
pygame.time.set_timer(SPAWNRING, 1500)

# flappy bird changed with an electron here
birdDownFlap = pygame.transform.scale2x(pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\bluebird-downflap.png').convert_alpha())
birdMidFlap = pygame.transform.scale2x(pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\bluebird-midflap.png').convert_alpha())
birdUpFlap = pygame.transform.scale2x(pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\bluebird-upflap.png').convert_alpha())
birdFrames = [birdDownFlap, birdMidFlap, birdUpFlap]
birdIndex = 2
birdie = birdFrames[birdIndex]
birdieRectangle = birdie.get_rect(center=(100, screenHeight/2))

# to give the wings an appearance of flapping
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Game Over Surface
gameOverSurface = pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\message.png').convert_alpha()
gameOverSurface = pygame.transform.scale2x(gameOverSurface)
gameOverRect = gameOverSurface.get_rect(center=(screenWidth/2, screenHeight/2))

# birdie = pygame.image.load(
#     'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\bluebird-midflap.png').convert_alpha()
# birdie = pygame.transform.scale2x(birdie)
# # make a rectangle so that detecting collisions is easier
# birdieRectangle = birdie.get_rect(center=(100, screenHeight/2))


# importing sounds using mixer. mixer can be a lil tricky

flapSound = pygame.mixer.Sound(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\SFX\\sfx_wing.wav')
buhByeSound = pygame.mixer.Sound(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\SFX\\sfx_die.wav')
scoreSound = pygame.mixer.Sound(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\SFX\\sfx_point.wav')
scoreSoundCountdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT, 100)

gameIntro()

# this is our main event loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # check if any key is pressed
            if event.key == pygame.K_SPACE and gameActive:  # check if spacebar is pressed

                birdMovement = 0  # turn this 0 before jumping to prevent unnecessary actions
                birdMovement -= 10  # because it works against the gravity, it is negative
                flapSound.play()  # play the flap sound whenever this loop is run

            if event.key == pygame.K_SPACE and gameActive == False:
                gameActive = True
                pipeList.clear()
                birdieRectangle.center = (100, screenHeight/2)
                birdMovement = 0
                score = 0
                positiveSpin = 0
                negativeSpin = 0

        if event.type == SPAWNPIPE:
            # we want to create a new pipe each time it updates so we use the function createPipe
            # unpacking the tupe, we change from append to extend
            pipeList.extend(createPipe())

        if event.type == SPAWNRING:
            ringList.extend(createRing())

        if event.type == BIRDFLAP:
            if birdIndex < 2:
                birdIndex += 1
            else:
                birdIndex = 0

            birdie, birdieRectangle = birdAnimation()
    # B.A.C.K.G.R.O.U.N.D
    screen.blit(backgroundSurface, (0, 0))

    if gameActive:
        # B.I.R.D
        birdMovement += gravity
        # rotating the bird
        rotatedBird = rotateBird(birdie)
        # rotating makes you lose quality, which is why we employ two surfaces
        # change the position of the birdmovement by the amount specified in the gravity variable
        birdieRectangle.centery += birdMovement
        # instead of a tuple we put this
        screen.blit(rotatedBird, birdieRectangle)
        # game ends if you collide with a pipe
        gameActive = checkCollision(pipeList)

        # P.I.P.E.S
        pipeList = movePipes(pipeList)
        drawPipes(pipeList)

        # R.I.N.G
        ringList = moveRings(ringList)
        drawRings(ringList)

        # S.C.O.R.E: scoring system: bird scores if it passes a pipe
        pipeCheck()
        upperRingCheck()
        lowerRingCheck()
        scoreDisplay('mainGame')
        # bird scores if it jumps through an upper ring

        # scoreDisplay('upperSpin')
        # bird scores if it jumps through a lower ring

        # scoreDisplay('lowerSpin')

    else:
        screen.blit(gameOverSurface, gameOverRect)
        highScore = updateHighScore(score, highScore)
        scoreDisplay('gameOver')

    # F.L.O.O.R
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -screenWidth:
        floor_x_pos = 0  # go back to where the floor_x_pos started
    # this will be moved by tiny increments
    # screen.blit(floorSurface, (floor_x_pos, 900))
    pygame.display.update()
    clock.tick(120)

# Next Steps for Shreya
# 1. convert to stern gerlach experiment using SG logic

# degree of freedom in an electron
# not normal observation
# results split into two possible states: spin up, spin downs
# spins neutralise each other
