import pygame             #pip install pygame
from pygame.locals import *


def draw(simMap, DISPLAY, width, height):

    for x in range(50):
        for y in range(50):
            pygame.draw.rect(DISPLAY, (100,100,100), (14*x,12*y,14,12))
            # print("Desenhou")

    # pos_x = 0 # linha onde vai desenhar
    # for x in range(42):
    #     pos_y = 0 # coluna onde vai desenhar
    #     for y in range(42):
    #         if simMap[x][y] == '0':
    #             Cor = (0,128,0)
    #         elif simMap[x][y] == '1':
    #             Cor = (78, 78, 78)
    #         elif simMap[x][y] == '2':
    #             Cor = (0,0,128)
    #         elif simMap[x][y] == '3':
    #             Cor = (128,0,0)
    #         else:
    #             Cor = (200,200,200)

    #         pygame.draw.rect(DISPLAY, Cor, (18*pos_x, 16*pos_y, 18, 16))
    #         pos_y += 1
    #     pos_x += 1

    # for x in range(0,756,18): # desenhando linhas verticais separadoras
    #     pygame.draw.line(DISPLAY, (64,64,64), (x, 0), (x, height))
    # for y in range(0,672,16): # desenhando linhas horizontais separadoras
    #     pygame.draw.line(DISPLAY, (64,64,64), (0, y), (width, y))