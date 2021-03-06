import random
import time

import pygame

from input import run_neuro_cycle as run_neuro_cycle1
from inputL import run_neuro_cycle as run_neuro_cycle2

pygame.init()

right_event = pygame.event.Event(pygame.K_RIGHT)
crash_sound = pygame.mixer.Sound("music/fail.mp3")
pygame.mixer.music.load("music/lala.wav")

# width and  height for game window
display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))

programIcon = pygame.image.load('img/icon.png')
pygame.display.set_icon(programIcon)

pygame.display.set_caption('Bikini Bottom race')

clock = pygame.time.Clock()

carImg = pygame.image.load("img/f.png")
sImg = pygame.image.load("img/s.png")

car_width = carImg.get_width()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == 'play':
                time.sleep(0.1)
                game_loop()
            elif action == 'quit':
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    gameDisplay.blit(TextSurf, TextRect)


def game_intor():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('font/BlobSpongey-ByjG.ttf', 90)
        TextSurf, TextRect = text_objects("Let's Play Game", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button('Play', 150, 450, 100, 50, '#A3E4BD', bright_green, 'play')
        button('Quit', 550, 450, 100, 50, '#E99CA1', bright_red, 'quit')

        pygame.display.update()


def stuff_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("score : " + str(count), True, white)
    gameDisplay.blit(text, (10, 10))


def stuff(stuffx, stuffy):
    gameDisplay.blit(sImg, (stuffx, stuffy))


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('BlobSpongey-ByjG.ttf', 90)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

    time.sleep(2)
    game_loop()


def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    largeText = pygame.font.Font('font/BlobSpongey-ByjG.ttf', 90)
    TextSurf, TextRect = text_objects('YOU CRASHED', largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button('Try Again', 150, 450, 100, 50, green, bright_green, 'play')
        button('Quit', 550, 450, 100, 50, red, bright_red, 'quit')
        pygame.display.update()


def game_loop():
    pygame.mixer.music.play(-1)
    x = (display_width * 0.45)
    y = (display_height * 0.7)

    x_change = 0

    stuff_startx = random.randrange(0, display_width - 200)
    stuff_starty = -700

    stuff_speed = 3
    stuff_width = sImg.get_width()
    stuff_height = sImg.get_height()

    dodged = 0

    gameExit = False

    while not gameExit:

        valueR = run_neuro_cycle1()
        valueL = run_neuro_cycle2()

        if valueR > 0.8:
            x_change = 5
        if valueL > 0.8:
            x_change = -5

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.K_RIGHT or event == right_event:
                x_change = 5

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT or event == right_event:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        if x_change > 0 and x < 600:
            x += x_change
        if x_change < 0 and x > 5:
            x += x_change
        gameDisplay.fill(white)
        bg = pygame.image.load("img/bot1.png")

        # INSIDE OF THE GAME LOOP
        gameDisplay.blit(bg, (0, 0))

        # stuffx,stuffy,stuffw,stuffh,color
        stuff(stuff_startx, stuff_starty, stuff_width, stuff_height, red)
        stuff_starty += stuff_speed

        stuff_dodged(dodged)

        car(x, y)

        if x > display_width - car_width or x < 0:
            crash()

        if stuff_starty > display_height:
            stuff_starty = 0 - stuff_height
            stuff_startx = random.randrange(0, display_width - 200)

            dodged += 1
            if (dodged % 5 == 0):
                stuff_speed += 2

        if y < stuff_starty + stuff_height:
            if x > stuff_startx and x < stuff_startx + stuff_width or x + car_width > stuff_startx and x + car_width < stuff_startx + stuff_width:
                crash()

        clock.tick(160)
        pygame.display.update()


game_intor()


def invoke_right_event():
    pygame.event.post(right_event)
