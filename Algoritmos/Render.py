import pygame,sys               #pip install pygame
from pygame.locals import *


def draw(formigueiro, formigas, DISPLAY, width, height):

    pos_x = 0 # linha onde vai desenhar
    for x in range(50):
        pos_y = 0 # coluna onde vai desenhar
        for y in range(50):

            if formigueiro[x][y] == 0:
                Cor = (0, 128, 0)
            else:
                r = 8 * formigueiro[x][y]
                r = 255 if r >= 256 else r
                Cor = (r, 0, 0)
            # desenhando quadrados das formigas/mapa/itens
            pygame.draw.rect(DISPLAY, Cor, (14*pos_x, 12*pos_y, 14, 12))
            pos_y += 1
        pos_x += 1

    for f in formigas:
        x, y = f.current_pos
        Cor = (128, 128, 128)
        pygame.draw.rect(DISPLAY, Cor, (14*x, 12*y, 10, 10))

    for x in range(0,700,14): # desenhando linhas verticais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (x, 0), (x, height))
    for y in range(0,600,12): # desenhando linhas horizontais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (0, y), (width, y))
