from random import randint
from contextlib import redirect_stdout

import pygame       #pip install pygame
from pygame.locals import *

import sys, os, time, Render, Logic

# width, height = 756, 672
# pygame.init()
# DISPLAY = pygame.display.set_mode((width, height), 0, 32)
# pygame.display.set_caption("Robô")

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

def simulate(robot, possible_moves, simulationMap, itemList, factoryList):
    if robot.state == 0: # estado procurando
        cost = Logic.state_search(robot, possible_moves, simulationMap, itemList, factoryList)
    elif robot.state == 1: # estado calculando path
        pass # se o robô está calculando o path, não há nada para fazer aqui
        # Logic.state_fetch(robot, possible_moves, simulationMap, itemList, factoryList)
    else: # estado executando path
        Logic.state_fetch(robot, simulationMap, itemList, factoryList)

def main_loop():
    
    pause = False
    end = False

    simulationMap = Logic.load_map()
    factoryList   = Logic.generate_factories(simulationMap)
    itemList      = Logic.generate_items(simulationMap)
    robot         = Logic.Robo((randint(0,41), randint(0,41)))

    possible_moves = [(0,-1),(0,1),(-1,0),(1,0)]
    # apenas se move esq/dir cima/baixo
    
    pygame.display.update()
    Render.draw(simulationMap, itemList, factoryList, robot)
    while(True):

        if not pause:
            pause = check_pause()
        else:
            pause = check_resume()
        
        if pause == None:
            return

        simulate(robot, possible_moves, simulationMap, itemList, factoryList)

        pygame.display.update()
        Render.draw(simulationMap, itemList, factoryList, robot)
        
def main():

    Render.init_window()

    main_loop()

if __name__ == "__main__":
    main()
