import pygame
from pygame.locals import *

width, height = 756, 672
DISPLAY = None

def init_window():
    pygame.init()
    global DISPLAY
    DISPLAY = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption("Robô")

def draw(simulationMap, itemList, factoryList, robot):#, DISPLAY, width, height):
    pos_x = 0 # linha onde vai desenhar
    for x in range(42):
        pos_y = 0 # coluna onde vai desenhar
        for y in range(42):
            Cor = simulationMap[x][y].cor
            # desenhando as células do mapa
            pygame.draw.rect(DISPLAY, Cor, (18*pos_x, 16*pos_y, 18, 16))
            pos_y += 1
        pos_x += 1

    for item in itemList: # desenhando os itens
        pygame.draw.circle(DISPLAY, item.cor, ((18*item.position[0])+9, (16*item.position[1])+8), 5)
        pygame.draw.circle(DISPLAY, (0,0,0),  ((18*item.position[0])+9, (16*item.position[1])+8), 5, 1)

    for factory in factoryList: # desenhando as fábricas
        pygame.draw.rect(DISPLAY, factory.cor, ((18*factory.position[0])+3, (16*factory.position[1])+2, 14, 12))
        pygame.draw.rect(DISPLAY, (0,0,0),     ((18*factory.position[0])+3, (16*factory.position[1])+2, 14, 12), 1)

    # desenhando o robô
    pygame.draw.rect(DISPLAY, (255,255,255), ((18*robot.position[0])+3, (16*robot.position[1])+2, 14, 12))
    pygame.draw.rect(DISPLAY, (0,0,0),       ((18*robot.position[0])+3, (16*robot.position[1])+2, 14, 12), 2)
        
    for x in range(0,756,18): # desenhando linhas verticais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (x, 0), (x, height))
    for y in range(0,672,16): # desenhando linhas horizontais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (0, y), (width, y))

def draw_border(border:list):
    # desenha uma borda branca ao redor das células que estão na fronteira do A*
    for target in border:
        pygame.draw.line(DISPLAY, (255,255,255), ((18*target[0])-18, (16*target[1])-16), ((18*target[0]),    (16*target[1])-16))
        pygame.draw.line(DISPLAY, (255,255,255), ((18*target[0])-18, (16*target[1])-16), ((18*target[0])-18, (16*target[1])))
        pygame.draw.line(DISPLAY, (255,255,255), ((18*target[0])-18, (16*target[1])),    ((18*target[0]),    (16*target[1])))
        pygame.draw.line(DISPLAY, (255,255,255), ((18*target[0]),    (16*target[1])-16), ((18*target[0]),    (16*target[1])))

def draw_looking_at(lookingAt):
    # desenha uma borda amarela ao redor das células que estão sendo avaliadas pelo A*
    pygame.draw.line(DISPLAY, (255,255,0), ((18*lookingAt[0])-18, (16*lookingAt[1])-16), ((18*lookingAt[0]),    (16*lookingAt[1])-16))
    pygame.draw.line(DISPLAY, (255,255,0), ((18*lookingAt[0])-18, (16*lookingAt[1])-16), ((18*lookingAt[0])-18, (16*lookingAt[1])))
    pygame.draw.line(DISPLAY, (255,255,0), ((18*lookingAt[0])-18, (16*lookingAt[1])),    ((18*lookingAt[0]),    (16*lookingAt[1])))
    pygame.draw.line(DISPLAY, (255,255,0), ((18*lookingAt[0]),    (16*lookingAt[1])-16), ((18*lookingAt[0]),    (16*lookingAt[1])))

def erase_looking_at(lookingAt):
    # desfaz a borda amarela ao redor da célula
    pygame.draw.line(DISPLAY, (255,255,255), ((18*lookingAt[0])-18, (16*lookingAt[1])-16), ((18*lookingAt[0]),    (16*lookingAt[1])-16))
    pygame.draw.line(DISPLAY, (255,255,255), ((18*lookingAt[0])-18, (16*lookingAt[1])-16), ((18*lookingAt[0])-18, (16*lookingAt[1])))
    pygame.draw.line(DISPLAY, (255,255,255), ((18*lookingAt[0])-18, (16*lookingAt[1])),    ((18*lookingAt[0]),    (16*lookingAt[1])))
    pygame.draw.line(DISPLAY, (255,255,255), ((18*lookingAt[0]),    (16*lookingAt[1])-16), ((18*lookingAt[0]),    (16*lookingAt[1])))

def draw_path(robot):
    # desenha uma borda vermelha ao reder das células do path escolhido pelo robô
    for cell in robot.path: 
        pygame.draw.line(DISPLAY, (255,0,0), ((18*cell[0])+18, (16*cell[1])+16), ((18*cell[0]),    (16*cell[1])+16))
        pygame.draw.line(DISPLAY, (255,0,0), ((18*cell[0])+18, (16*cell[1])+16), ((18*cell[0])+18, (16*cell[1])))
        pygame.draw.line(DISPLAY, (255,0,0), ((18*cell[0])+18, (16*cell[1])),    ((18*cell[0]),    (16*cell[1])))
        pygame.draw.line(DISPLAY, (255,0,0), ((18*cell[0]),    (16*cell[1])+16), ((18*cell[0]),    (16*cell[1])))