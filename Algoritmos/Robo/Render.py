import pygame             #pip install pygame
from pygame.locals import *


def draw(simMap, DISPLAY, width, height):
    pos_x = 0 # linha onde vai desenhar
    for x in range(42):
        pos_y = 0 # coluna onde vai desenhar
        for y in range(42):
            Cor = simMap[y][x].cor
            
            pygame.draw.rect(DISPLAY, Cor, (18*pos_x, 16*pos_y, 18, 16))
            pos_y += 1
        pos_x += 1

    for x in range(0,756,18): # desenhando linhas verticais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (x, 0), (x, height))
    for y in range(0,672,16): # desenhando linhas horizontais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (0, y), (width, y))