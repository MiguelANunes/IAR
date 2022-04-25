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

def check_pause():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True

    return False

def check_resume():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return False

    return True

# def check_kill():
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 pygame.quit()
#                 sys.exit()

def main_loop(DISPLAY):
    formigueiro, formigas = Logic.cria_formigueiro()
    iteracao = 0

    pause = False
    while(True):

        if pause:
            pause = check_resume()
        else:
            pause = check_pause()

        # if iteracao % 50 == 0:
        #     dump_formigueiro(formigueiro, iteracao)
            
        if not pause:
            simulate(formigueiro, formigas)
            Render.draw(formigueiro, formigas, DISPLAY, width, height)
            pygame.display.update()
            iteracao += 1


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