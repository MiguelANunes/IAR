from random import randint
from contextlib import redirect_stdout

import pygame       #pip install pygame
from pygame.locals import *

import sys, os, time, Render, Logic

width, height = 756, 672
pygame.init()
DISPLAY = pygame.display.set_mode((width, height), 0, 32)

# ver distância de Manhatan

def check_pause():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                return

    return False

def check_resume():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return False
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                return

    return True

def main_loop(simMap):
    
    pause = False
    end = False

    # for x in range(42):
    #     for y in range(42):
    #         print(simMap[x][y].__str__(),end=" ")
    #     print()
    # input()

    while(True):

        if pause == None:
            return

        if not pause:
            pause = check_pause()
        else:
            pause = check_resume()

        Render.draw(simMap, DISPLAY, width, height)
        pygame.display.update()
        
def main():

    # pygame.init()
    # DISPLAY = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption("Robô")
    DISPLAY.fill((0,128,0))
    main_loop(Logic.load_map())

if __name__ == "__main__":
    main()
