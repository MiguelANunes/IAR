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
                Cor = (128, 0, 0)
            # desenhando quadrados das formigas/mapa/itens
            pygame.draw.rect(DISPLAY, Cor, (14*pos_x, 12*pos_y, 14, 12))
            pos_y += 1
        pos_x += 1

    for f in formigas:
        x, y = f.current_pos
        if f.current_state == 1:
            Cor = (192, 192, 192)
        else:
            Cor = (64, 64, 64)
        pygame.draw.rect(DISPLAY, Cor, (14*x, 12*y, 10, 10))

    for x in range(0,700,14): # desenhando linhas verticais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (x, 0), (x, height))
    for y in range(0,600,12): # desenhando linhas horizontais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (0, y), (width, y))


def draw_dump(filename, DISPLAY, width, height):
    formigueiro = []
    with open("dump/"+filename) as f:
        formigueiro = [[int(cell) for cell in line.split(" ") if cell != '\n'] for line in f]

    name = filename.replace("formigueiro","")
    name = name.replace(".txt","")
    
    DISPLAY = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption("Iteração "+name)
    # DISPLAY.fill((255,255,255))
    draw(formigueiro, [], DISPLAY, width, height)
    pygame.display.update()