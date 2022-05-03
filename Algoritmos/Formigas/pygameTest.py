import pygame
from pygame.locals import *

width, height = 700, 600
pygame.init()
DISPLAY = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Formigas")
DISPLAY.fill((0,128,0))

Cor = (255,255,255)
x = 10
y = 10
pygame.display.update()
while True:
    # pygame.draw.rect(DISPLAY, (0,0,0), (14*x, 12*y, 10.5, 10.5), 0)
    pygame.draw.rect(DISPLAY, Cor, (14*x, 12*y, 10, 10), 0)
    for x in range(0,700,14): # desenhando linhas verticais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (x, 0), (x, height))
    for y in range(0,600,12): # desenhando linhas horizontais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (0, y), (width, y))
    pygame.display.update()