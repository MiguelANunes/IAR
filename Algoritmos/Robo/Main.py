from random import randint
from contextlib import redirect_stdout

import pygame       #pip install pygame
from pygame.locals import *

import sys, os, time, Render

width, height = 700,600#756, 672
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

def load_map():
    simMap = []
    with open(f"inputs/input.txt") as f:
        for line in f:
            line = (line.replace("\t"," ")).replace(",",".")
            cell = [l.rstrip('\n') for l in line.split(" ") if l != '' and l != '\n']
            simMap.append(cell)
    
    # for x in range(42):
    #     for y in range(42):
    #         print(simMap[x][y], end=" ")
    #     print()
    # input()
    return simMap

def main_loop(simMap):
    
    pause = False
    end = False

    while(True):

        if pause == None:
            return

        if not pause:
            pause = check_pause()
        else:
            pause = check_resume()

        # for x in range(42):
        #     for y in range(42):
        #         print(simMap[x][y], end=" ")
        #     print()
        # input()
        Render.draw(simMap, DISPLAY, width, height)
        # for x in range(50):
        #     for y in range(50):
        #         pygame.draw.rect(DISPLAY, (100,100,100), (14*x,12*y,14,12))
        
def main():

    # pygame.init()
    # DISPLAY = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption("Robô")
    DISPLAY.fill((0,128,0))
    M = load_map()
    main_loop(M)

if __name__ == "__main__":
    main()
