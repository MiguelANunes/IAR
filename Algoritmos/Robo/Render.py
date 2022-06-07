import pygame             #pip install pygame
from pygame.locals import *

import Logic

def draw(simMap, itemList, factoryList, robot, DISPLAY, width, height):
    pos_x = 0 # linha onde vai desenhar
    for x in range(42):
        pos_y = 0 # coluna onde vai desenhar
        for y in range(42):
            Cor = simMap[y][x].cor
            # desenhando as células do mapa
            pygame.draw.rect(DISPLAY, Cor, (18*pos_x, 16*pos_y, 18, 16))
            pos_y += 1
        pos_x += 1

    for item in itemList: # desenhando os itens
        pygame.draw.circle(DISPLAY, item.cor, ((18*item.pos[0])+9, (16*item.pos[1])+8), 5)

    for factory in factoryList: # desenhando as fábricas
        pygame.draw.rect(DISPLAY, factory.cor, ((18*factory.pos[0])+3, (16*factory.pos[1])+2, 14, 12))

    # desenhando o robô
    pygame.draw.rect(DISPLAY, (255,255,255), ((18*robot.pos[0])+3, (16*robot.pos[1])+2, 14, 12))
    pygame.draw.rect(DISPLAY, (0,0,0), ((18*robot.pos[0])+3, (16*robot.pos[1])+2, 14, 12), 2)
        
    for x in range(0,756,18): # desenhando linhas verticais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (x, 0), (x, height))
    for y in range(0,672,16): # desenhando linhas horizontais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (0, y), (width, y))

    if Logic.is_valid(robot.target): # se o robô quer chegar em alguma célula
        pygame.draw.line(DISPLAY, (255,0,0), ((18*robot.target[0])-18, (16*robot.target[1])-16), ((18*robot.target[0]),    (16*robot.target[1])-16))
        pygame.draw.line(DISPLAY, (255,0,0), ((18*robot.target[0])-18, (16*robot.target[1])-16), ((18*robot.target[0])-18, (16*robot.target[1])))
        pygame.draw.line(DISPLAY, (255,0,0), ((18*robot.target[0])-18, (16*robot.target[1])),    ((18*robot.target[0]),    (16*robot.target[1])))
        pygame.draw.line(DISPLAY, (255,0,0), ((18*robot.target[0]),    (16*robot.target[1])-16), ((18*robot.target[0]),    (16*robot.target[1])))

    if Logic.is_valid(robot.lookingAt): # se o robô está olhando pra alguma célula
        pygame.draw.line(DISPLAY, (255,255,255), ((18*robot.lookingAt[0])-18, (16*robot.lookingAt[1])-16), ((18*robot.lookingAt[0]),    (16*robot.lookingAt[1])-16))
        pygame.draw.line(DISPLAY, (255,255,255), ((18*robot.lookingAt[0])-18, (16*robot.lookingAt[1])-16), ((18*robot.lookingAt[0])-18, (16*robot.lookingAt[1])))
        pygame.draw.line(DISPLAY, (255,255,255), ((18*robot.lookingAt[0])-18, (16*robot.lookingAt[1])),    ((18*robot.lookingAt[0]),    (16*robot.lookingAt[1])))
        pygame.draw.line(DISPLAY, (255,255,255), ((18*robot.lookingAt[0]),    (16*robot.lookingAt[1])-16), ((18*robot.lookingAt[0]),    (16*robot.lookingAt[1])))