from random import randint
from contextlib import redirect_stdout

import pygame       #pip install pygame
from pygame.locals import *

import sys, os, time, Render, Logic

width, height = 756, 672
pygame.init()
DISPLAY = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Robô")

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

def simulate(robot, possible_moves, simulationMap, listItems, listFactories):
    if robot.state == 0: # estado procurando
        pass
        # Logic.state_search(robot, possible_moves, simulationMap, listItems, listFactories)
    elif robot.state == 1: # estado calculando path
        pass
        # Logic.state_fetch(robot, possible_moves, simulationMap, listItems, listFactories)
    else: # estado executando path
        pass

def main_loop():
    
    pause = False
    end = False

    simulationMap = Logic.load_map()
    factoryList   = Logic.generate_factories(simulationMap)
    itemList      = Logic.generate_items(simulationMap)
    robot         = Logic.Robo((randint(0,41), randint(0,41)))

    possible_moves = []
    for i in range(-1,2):
        for j in range(-1,2):
            possible_moves.append((i,j))

    while(True):

        if pause == None:
            return

        if not pause:
            pause = check_pause()
        else:
            pause = check_resume()

        pygame.display.update()
        Render.draw(simulationMap, itemList, factoryList, robot, DISPLAY, width, height)
        
def main():

    # pygame.init()
    # DISPLAY = pygame.display.set_mode((width, height), 0, 32)
    
    
    main_loop()

if __name__ == "__main__":
    main()
