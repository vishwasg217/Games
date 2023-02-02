import pygame, sys, time
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((400, 300))



pygame.mixer.music.load("Assets/gun.mp3")
pygame.mixer.music.play()
time.sleep(2)
pygame.mixer.music.stop()

while True: # Main Loop

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()