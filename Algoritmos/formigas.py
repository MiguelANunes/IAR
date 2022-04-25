from random import randint

import pygame,sys               #pip install pygame
from pygame.locals import *

from contextlib import redirect_stdout


width, height = 700, 600

def cria_formigueiro():
    size_formigueiro = 50 # cria um mapa de 50x50
    formigueiro = [[0 for i in range(size_formigueiro)] for i in range(size_formigueiro)]

    for _ in range(1000): # insere 1000 itens
        x = randint(0, 49)
        y = randint(0, 49)
        formigueiro[x][y] += 1

    for _ in range(10): # insere 10 agentes
        x = randint(0, 49)
        y = randint(0, 49)
        while(formigueiro[x][y]) != 0:
            x = randint(0, 49)
            y = randint(0, 49)
        formigueiro[x][y] = -1

    return formigueiro

def dump_formigueiro(formigueiro, iteracao):
    file_formigueiro = "dump/formigueiro"+str(iteracao)+".txt"

    with open(file_formigueiro, 'w')  as f:
        with redirect_stdout(f):
            for linha in formigueiro:
                for item in linha:
                    print(item, end=" ")
                print()

def draw(formigueiro, DISPLAY):

    pos_x = 0 # linha onde vai desenhar
    for x in range(50):
        pos_y = 0 # coluna onde vai desenhar
        for y in range(50):

            if formigueiro[x][y] == 0:
                Cor = (0, 128, 0)
            elif formigueiro[x][y] > 0:
                r = 8 * formigueiro[x][y]
                r = 255 if r >= 256 else r
                Cor = (r, 0, 0)
            else:
                Cor = (128, 128, 128)
            # desenhando quadrados das formigas/mapa/itens
            pygame.draw.rect(DISPLAY, Cor, (14*pos_x, 12*pos_y, 14, 12))
            pos_y += 1
        pos_x += 1

    for x in range(0,700,14): # desenhando linhas verticais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (x, 0), (x, height))
    for y in range(0,600,12): # desenhando linhas horizontais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (0, y), (width, y))

def main_loop(DISPLAY):
    formigueiro = cria_formigueiro()
    iteracao = 0

    while(True):
        if iteracao % 5 == 0:
            dump_formigueiro(formigueiro, iteracao)
        draw(formigueiro, DISPLAY)
        pygame.display.update()
        iteracao += 1
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

def main():
    pygame.init()
    DISPLAY = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption("Formigas")
    DISPLAY.fill((255,255,255))

    main_loop(DISPLAY)
    # pygame.draw.rect(DISPLAY, (255,0,0), (0, 0, 14, 12))
    # pygame.draw.rect(DISPLAY, (0,255,0), (14, 0, 14, 12))
    # pygame.draw.rect(DISPLAY, COR, (COORD_X, COORD_Y, COMPRIMENTO, ALTURA))
    # pygame.draw.circle(window, color, (x, y), radius)
    # pygame.draw.polygon(window, color, [(x1, y1), (x2, y2), (x3, y3)])
        

if __name__ == "__main__":
    main()