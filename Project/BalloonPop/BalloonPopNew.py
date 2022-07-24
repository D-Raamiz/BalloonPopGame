# Import
import pygame as py
import cv2
import numpy as np
import random as rn
from cvzone.HandTrackingModule import HandDetector
from pygame import mixer
from time import sleep

# Initialize
py.init()

# Sound Effect
mixer.init()
mixer.music.load('../Resources/mixkit-ballon-blows-up-3071.wav')
mixer.music.set_volume(0.7)

# Create Window/Display
width, height = 1280, 720
window = py.display.set_mode((width, height))
py.display.set_caption('Balloon Pop')

# Initialize Clock for FPS
fps = 30
clock = py.time.Clock()

# Webcam
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

# Images
background = py.image.load('../Resources/background.jpg').convert()
imgBalloon = py.image.load('../Resources/BalloonRed.png').convert_alpha()
rectBalloon = imgBalloon.get_rect()
rectBalloon.x, rectBalloon.y = 500, 500
start = py.image.load('../Resources/start.png').convert_alpha()
exit = py.image.load('../Resources/exit.png').convert_alpha()
restart = py.image.load('../Resources/restart.png').convert_alpha()

# Variables
speed = 5
score = 900
no_of_balloon = 0
levelStart = 10
level = 10
cycle = 0
s = True
levelPause = False
over = False
a = False

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# To reset balloon to rise from the bottom


def resetBalloon():
    rectBalloon.x = rn.randint(100, img.shape[1]-100)
    rectBalloon.y = img.shape[0] + 50

# Button Class


class Button:
    def __init__(self, x, y, image):
        width = image.get_width()
        height = image.get_height()
        self.image = py.transform.scale(image, (int(width), int(height)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        # get mouse position
        pos = py.mouse.get_pos()
        window.blit(self.image, (self.rect.x, self.rect.y))

        # check mouseclicked condition
        if self.rect.collidepoint(pos):
            if py.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = True

        if not py.mouse.get_pressed()[0]:
            self.clicked = False
        return action


# Instances of Class button
startbutton = Button(1280/4, 720/2-50, start)
restartbutton = Button(1280/4+500, 720/2-50, restart)
exitbutton = Button(1280/4+500, 720/2-50, exit)

# Main Loop
running = True
while running:
    # Conditions to close the window 1. Esc key 2.Click on Cross sign
    for event in py.event.get():
        if event.type == py.QUIT or py.key.get_pressed()[py.K_ESCAPE]:
            running = False

    # OpenCV
    success, img = cap.read()   # reads the images from the webcam
    img = cv2.flip(img, 1)  # flip the image horizontally
    hands, img = detector.findHands(
        img, flipType=False)  # detect hand from img

    # convert img from BGR to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)  # used numpy to rotate the image 90deg
    frame = py.surfarray.make_surface(imgRGB).convert()
    frame = py.transform.flip(frame, True, False)  # flipped the image

    # Apply Logic
    # if s is true, show Start and Exit buttons
    if s:
        window.blit(background, (0, 0))

        # Exit button
        if exitbutton.draw():
            running = False

        # Start button
        elif startbutton.draw():
            s = False

    # Checks if the balloon has reached top without pop, and if does, GAME OVER, or Restart
    elif rectBalloon.y < 0:
        resetBalloon()
        window.blit(background, (0, 0))
        font = py.font.Font('../Resources/Marcellus-Regular.ttf', 50)
        gameOver = font.render(f' Game Over!', True, (50, 50, 255))
        scoreText = font.render(f' Score: {score} ', True, (50, 50, 255))
        window.blit(gameOver, (390, 300))
        window.blit(scoreText, (390, 350))
        over = True
        a = True

    # After Clicking Restart button
    elif over and a:
        if restartbutton.draw():
            over = False
            speed = 5
            no_of_balloon = 0
            score = 0
            level = 1

    # if balloon isn't on the top, the game is been playing
    elif not over:
        window.blit(frame, (0, 0))

        rectBalloon.y -= speed  # Moves the balloon up

        if hands:
            # detects 1st hand (in this case, only hand) in the list hands
            hand = hands[0]
            x, y = hand['lmList'][8][0], hand['lmList'][8][1]
            popped = False  # before pop
            if rectBalloon.collidepoint(x, y):
                popped = True   # after pop
                resetBalloon()
                score += 10     # score increases by 10
                no_of_balloon += 1  # counts the number of balloons being popped

                # list of number of balloons going to appear in each level
                l1 = 5
                l2 = l1 + 10
                l3 = l2 + 10
                l4 = l3 + 10
                l5 = l4 + 10
                l6 = l5 + 10
                l7 = l6 + 10
                l8 = l7 + 10
                l9 = l8 + 10
                l10 = l9 + 10
                levels = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]

                # plays/run the music when popped
                mixer.music.play()

                # jumps to new level and increases speed, when no_of_balloon popped in each level reaches the above mentioned number of balloons going to appear in each level
                if popped and no_of_balloon in levels:
                    level += 1
                    speed += 2
                    levelPause = True

            if not rectBalloon.collidepoint(x, y):
                popped = False

        window.blit(imgBalloon, rectBalloon)

        font = py.font.Font('../Resources/Marcellus-Regular.ttf', 50)
        textScore = font.render(
            f'Score: {score}  Level: {level}', True, (50, 50, 255))
        window.blit(textScore, (35, 35))  # displays score and level on top

    if levelPause:
        window.blit(background, (0, 0))
        over = True
        # After completing level 10/last level
        if level == 11:
            window.blit(background, (0, 0))
            wins = font.render(
                'Congratulations you have completed the game !!!', True, (50, 50, 255))
            scoreText = font.render(f' Score: {score} ', True, (50, 50, 255))
            window.blit(wins, (130, 300))
            window.blit(scoreText, (500, 350))
            over = True
            a = False

        elif level < 11:
            cycle += 1
            window.blit(background, (0, 0))
            nextLevel = font.render(
                f'Level {level} begins ...', True, (50, 50, 255))
            window.blit(nextLevel, (500, 350))
            if cycle == 90:
                levelPause = False
                resetBalloon()
                cycle = 0
                over = False

    # Update Display
    py.display.update()

    # Set FPS
    clock.tick(fps)

cap.release()
cv2.destroyAllWindows()
