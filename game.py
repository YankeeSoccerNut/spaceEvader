# TODO: Need stronger visual/audio cue when powerUp is over...r2d2 is weak
# TODO: Could play with volume so that Sound Effects trump Background music
# TODO: Game play -- what's the goal?  Good v Evil...1st to 10 wins?  Shortest time to 10 wins for our hero?
# TODO: Retro effects -- could have Coins and Start, could add Top Players list
# TODO: improve the KeepInBounds....use up/down/left/right technique...won't work for Vader through....
# TODO: Look at hypot technique as well...variation on pointMe

#  Include pygame
import pygame
import random

# from the python built-in get the absolute value method
# we'll use this in our collision detection
from math import fabs

# don't need these math funcions unless I want to implement Distance
# from math import sqrt
# from math import pow

# Init pygame
# we have to run their init method

pygame.init()
# print pygame.mixer.get_num_channels() - Default is 8, confirmed!

# Create a screen with a particular size
# Use a tuple (an immutable list) for screen size...pygame requires it
screen_size_x = 512
screen_size_y = 480
# screen_size_x = 600
# screen_size_y = 800
screen_size = (screen_size_x, screen_size_y)
# Tell pygame to set the screen up and store it
pygame_screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("Space eVader")
background_image = pygame.image.load("./images/spaceScene.png")

font = pygame.font.Font(None, 25)

# our Hero!
hero_image_right = pygame.image.load("./images/yoda.png")
hero_image_left = pygame.image.load("./images/yodaleft.png")
hero_image = hero_image_right

# our Boss!
lordVaderImageLeft = pygame.image.load("./images/lordVaderLeft.png")
lordVaderImageRight = pygame.image.load("./images/lordVaderRight.png")
lordVader_image = lordVaderImageLeft

lightsaberNormal = pygame.image.load("./images/lightsaber.png")
lightsaberInvert = pygame.image.load("./images/invertLightsaber.png")
lightsaber_image = lightsaberNormal

# got some sound channel conflicts....group and play sounds through assigned channels
# channel objects
# pygame.mixer.set_reserved(3)
mixChannel1 = pygame.mixer.Channel(0)
mixChannel2 = pygame.mixer.Channel(1)
mixChannel3 = pygame.mixer.Channel(2)

# e.g. Lord Vader and Yoda never speak at same time...so they're in same group
# sounds groups
vaderWarningSound = pygame.mixer.Sound(file="./sounds/swvader01.wav")
yodaLaughingSound = pygame.mixer.Sound(file="./sounds/yodalaughing.wav")

saberOnSound = pygame.mixer.Sound(file="./sounds/ltsaberon01.wav")
r2d2WarnSound = pygame.mixer.Sound(file="./sounds/R2D2Warn.wav")

saberHitSound = pygame.mixer.Sound(file="./sounds/ltsaberhit01.wav")
saberAppearsSound = pygame.mixer.Sound(file="./sounds/ltsaberappears.wav")

hero = {
    "x": 100,
    "y": 100,
    "speed": 15,
    "wins": 0,
    "height": 32,
    "width": 32
}

lightsaber = {
    "x": 200,
    "y": 200,
    "speed": 10,
    "height": 32,
    "width": 32
}

lordVader = {
    "x": 300,
    "y": 300,
    "speed": 15,
    "height": 50,
    "width": 38
}

topLeftCorner = {
    "x": 0,
    "y": 0
}

topRightCorner = {
    "x": screen_size_x,
    "y": 0
}

bottomLeftCorner = {
    "x": 0,
    "y": screen_size_y
}

bottomRightCorner = {
    "x": screen_size_x,
    "y": screen_size_y
}

keys = {
    "esc": 27,
    "space": 32,
    "i": 105,
    "j": 106,
    "k": 107,
    "l": 108,
    "up": 273,
    "down": 274,
    "right": 275,
    "left": 276
}

keys_down = {
    "up": False,
    "down": False,
    "right": False,
    "left": False
}


def keepCharInBounds(character):
    if character['y'] < 0:
        character['y'] = 0
    elif character['y'] + 32 >= screen_size_y:
        character['y'] = screen_size_y - 32

    if character['x'] < 0:
        character['x'] = 0
    elif character['x'] + 32 >= screen_size_x:
        character['x'] = screen_size_x - 32

# let's implement goal-oriented movement...
# Trying to keep it abstracted...
# Give your x,y position and goal x,y position  get delta x and delta y from your position (to calculate slope of direct line to goal)


def pointMe(yourPosition, goalPosition):
    # print yourPosition
    # print goalPosition
    delta = [0, 0]
    delta[0] = yourPosition[0] - goalPosition[0]
    delta[1] = yourPosition[1] - goalPosition[1]
    # lineDistance = sqrt((pow(delta[0],2)) + (pow(delta[1],2)))
    # print lineDistance
    return delta


def randomlyPlaceChar(character):
    character['x'] = random.randint(32, screen_size_x - 32)
    character['y'] = random.randint(32, screen_size_y - 32)
    return (character['x'], character['y'])


def removeObjectFromBackground(object):
    pygame_screen.blit(background_image, (object['x'], object['y']), pygame.Rect(
        object['x'], object['y'], object['height'], object['width']))
    object['x'] = screen_size_x + 100
    object['y'] = screen_size_y + 100
    return (object['x'], object['y'])


def detectCollision(character1, character2):
    distance_between = fabs(
        character1['x'] - character2['x']) + fabs(character1['y'] - character2['y'])

    if distance_between < 32:
        return True

    return (False)


def moveLordVader(character, pursue=True):
    # Move Vader either towards or away from character depending on bool
    # default is to pursue, when pursue is false we evade

    # Use pointMe to get the deltas for calculating slope
    target = pointMe([lordVader['x'], lordVader['y']],
                     [character['x'], character['y']])

    # TODO Ask why I have to do global here but NOT above
    global lordVader_image

    # Setting x coordinate is easy...based on sign and speed
    if pursue:
        if target[0] < 0:  # delta x
            lordVader_image = lordVaderImageRight
            lordVader['x'] += lordVader['speed']
        elif target[0] > 0:
            lordVader_image = lordVaderImageLeft
            lordVader['x'] -= lordVader['speed']
        else:
            # print "Collision Along X"
            # kluge....avoid potential divide by zero error!
            target[0] = 1
    else:  # need to evade, reverse everthing above
        if target[0] < 0:  # delta x
            lordVader_image = lordVaderImageLeft
            lordVader['x'] -= lordVader['speed']
        elif target[0] > 0:
            lordVader_image = lordVaderImageRight
            lordVader['x'] += lordVader['speed']
        else:
            # print "Collision Along X"
            # kluge....avoid potential divide by zero error!
            target[0] = 1

    # y coordinate is tougher...speed is a proxy for distance
    # we know slope so ratio should hold along the hypotenuse (goal path)...
    # y is "speed" we're looking for...

    if pursue:
        if target[0] <= 32:
            if target[1] <= 0:
                lordVader['y'] += lordVader['speed']
            else:
                lordVader['y'] -= lordVader['speed']
        elif target[1] < 0:  # delta y
            lordVader['y'] += round(fabs(lordVader['speed']
                                         * target[1] / target[0]))
        elif target[1] > 0:
            lordVader['y'] -= round(fabs(lordVader['speed']
                                         * target[1] / target[0]))
        # else:  delta Y is 0
        #     print "Collision Along Y"
    else:  # evade...opposite of above
        if target[0] <= 32:  # already collided along X
            if target[1] <= 0:
                lordVader['y'] -= lordVader['speed']
            else:
                lordVader['y'] += lordVader['speed']
        elif target[1] < 0:  # delta y
            lordVader['y'] -= round(fabs(lordVader['speed']
                                         * target[1] / target[0]))
        elif target[1] > 0:
            lordVader['y'] += round(fabs(lordVader['speed']
                                         * target[1] / target[0]))
        # else:  Delta Y is zero
        #     print "Collision Along Y"
        # kluge to the 4 corners problem...
        if ((detectCollision(lordVader, topLeftCorner)) or
            (detectCollision(lordVader, topRightCorner)) or
            (detectCollision(lordVader, bottomLeftCorner)) or
                (detectCollision(lordVader, bottomRightCorner))):
            randomlyPlaceChar(lordVader)

    # print "After Y-Speed calc...Lord Vader x: %r y: %r" % (lordVader['x'], lordVader['y'])
    keepCharInBounds(lordVader)


# Create a game loop (while)
# use a boolean
game_on = True
advantageLight = True
vaderPursues = True
advantageTimer = 10
advantageStartTicks = pygame.time.get_ticks()
powerTimer = 5
powerStartTicks = 0
powerUp = False

randomlyPlaceChar(lightsaber)

# start the music...
pygame.mixer.music.load("./sounds/swmain.mp3")
pygame.mixer.music.play(-1)

while game_on:  # main loop
    pygame_screen.blit(background_image, [0, 0])

    seconds = (pygame.time.get_ticks() - advantageStartTicks) / 1000

    if seconds >= 1:  # updates the timer each second
        advantageTimer -= 1
        seconds = 0
        advantageStartTicks = pygame.time.get_ticks()
        moveLordVader(hero, not powerUp)  # evades if powerUp

    if advantageTimer <= 0:  # advantage has shifted
        if advantageLight:  # now it's Darkside Advantage
            advantageLight = False
            advantageTimer = 5
            vaderPursues = True
            mixChannel1.play(vaderWarningSound)
        else:  # time for Lightside to have the advantage
            mixChannel1.play(yodaLaughingSound)
            advantageLight = True
            advantageTimer = 10
            randomlyPlaceChar(lightsaber)
            mixChannel3.play(saberAppearsSound)

    # Manage the Power Timer in main loop (collision is 1 point in time)

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):  # Trap the quit event
            # user clicked red x to quit the game, set the boolean
            game_on = False
        elif (event.type == pygame.KEYDOWN):
            # print "Key %r" % event.key
            if (event.key == keys['up'] or event.key == keys['i']):
                keys_down['up'] = True
            elif (event.key == keys['down'] or event.key == keys['k']):
                keys_down['down'] = True
            elif (event.key == keys['right'] or event.key == keys['l']):
                keys_down['right'] = True
            elif (event.key == keys['left']) or event.key == keys['j']:
                keys_down['left'] = True
            elif (event.key == keys['esc']):
                # Move the hero to a random position a la hyperspace in Asteroids...consider separate function and negative consequence
                randomlyPlaceChar(hero)
            moveLordVader(hero, vaderPursues)  # pursue/evade our hero
        elif (event.type == pygame.KEYUP):
            # print "User released a key"
            if (event.key == keys['up'] or event.key == keys['i']):
                keys_down['up'] = False
            elif (event.key == keys['down'] or event.key == keys['k']):
                keys_down['down'] = False
            elif (event.key == keys['right'] or event.key == keys['l']):
                keys_down['right'] = False
            elif (event.key == keys['left'] or event.key == keys['j']):
                keys_down['left'] = False
            moveLordVader(hero, vaderPursues)  # pursue/evade our hero

    if keys_down['up']:
        hero_image = hero_image_left
        hero['y'] -= hero['speed']
    elif keys_down['down']:
        hero_image = hero_image_left
        hero['y'] += hero['speed']

    if keys_down['left']:
        hero_image = hero_image_left
        hero['x'] -= hero['speed']
    elif keys_down['right']:
        hero_image = hero_image_right
        hero['x'] += hero['speed']

    keepCharInBounds(hero)

    # look for collision with lightsaber

    if (detectCollision(hero, lightsaber)):
        powerUp = True

        # wipe out the lightsaber and make sound
        removeObjectFromBackground(lightsaber)
        mixChannel2.play(saberOnSound)

        # Make Vader run away!
        vaderPursues = False

        # get the baseline for the timer
        powerStartTicks = pygame.time.get_ticks()

    if (detectCollision(lordVader, hero)):
        if powerUp:  # Win!
            #"print our hero wins!"
            mixChannel3.play(saberHitSound)
            hero['wins'] += 1
            randomlyPlaceChar(hero)
            randomlyPlaceChar(lordVader)
        else:
            if advantageLight:
                print "Vader caught you while you had the advantage"
            else:
                print "Dark forces are at play!"

    if powerUp:  # we know hero has lightsaber
        hero_image = lightsaberNormal  # override the hero image

        powerSeconds = (pygame.time.get_ticks() - powerStartTicks) / 1000

        if powerSeconds >= 1:  # updates the timer each second
            powerTimer -= 1
            powerSeconds = 0
            powerStartTicks = pygame.time.get_ticks()

        if powerTimer <= 0:  # time expired, set flag and reset timer
            powerUp = False
            powerTimer = 5
            hero_image = hero_image_left
            print "reset hero_image after powerUp expired"
            mixChannel2.play(r2d2WarnSound)
            if advantageLight:  # another chance to grab the lightsaber
                randomlyPlaceChar(lightsaber)
                mixChannel3.play(saberAppearsSound)

    if advantageLight:
        advantage_text = font.render(
            "Lightside Rules: %d" % advantageTimer, True, (255, 255, 255))

        if not powerUp:  # make lightsaber blink
            if lightsaber_image == lightsaberInvert:
                lightsaber_image = lightsaberNormal
            else:
                lightsaber_image = lightsaberInvert
            pygame_screen.blit(lightsaber_image, [
                               lightsaber['x'], lightsaber['y']])

    else:  # advantage Darkside!  No lightsaber to save our hero!
        advantage_text = font.render(
            "DARKSIDE RULES! %d" % advantageTimer, True, (255, 255, 255))

        # if the hero was powerUp the Darkside takes it away!
        powerTimer = 5  # reset timer
        powerUp = False

        if hero_image == lightsaberNormal:  # kluge to squash hero_image bug
            hero_image = hero_image_left

        # wipe out the lightsaber
        removeObjectFromBackground(lightsaber)

    # Fill in the screen with a color or image...use blit

    wins_text = font.render("Wins: %d" % (hero['wins']), True, (255, 255, 255))
    pygame_screen.blit(wins_text, [40, 40])
    pygame_screen.blit(advantage_text, [300, 40])
    pygame_screen.blit(lordVader_image, [lordVader['x'], lordVader['y']])

    # Always want the hero on top so blit him last!
    pygame_screen.blit(hero_image, [hero['x'], hero['y']])

# Repeat over and over until quit
    pygame.display.flip()
