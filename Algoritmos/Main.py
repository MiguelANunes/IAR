from random import randint
from contextlib import redirect_stdout

import pygame       #pip install pygame
from pygame.locals import *

import sys,Render, Logic

width, height = 700, 600

def dump_formigueiro(formigueiro, iteracao):
    file_formigueiro = "dump/formigueiro"+str(iteracao)+".txt"

    with open(file_formigueiro, 'w')  as f:
        with redirect_stdout(f):
            for linha in formigueiro:
                for item in linha:
                    print(item, end=" ")
                print()

def simulate(formigueiro, formigas):
    for f in formigas:
        if f.current_state == 0:
            Logic.state_not_carrying(f, formigueiro)
        else:
            Logic.state_carrying(f,formigueiro)

def main_loop(DISPLAY):
    formigueiro, formigas = Logic.cria_formigueiro()
    iteracao = 0

    while(True):
        # if iteracao % 50 == 0:
        #     dump_formigueiro(formigueiro, iteracao)
        simulate(formigueiro, formigas)
        Render.draw(formigueiro, formigas, DISPLAY, width, height)
        pygame.display.update()
        iteracao += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def main():
    # https://stackoverflow.com/questions/66209365/how-to-save-pygame-scene-as-jpeg
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