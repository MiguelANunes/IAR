import sys
import Render, Logic

import pygame       #pip install pygame
from pygame.locals import *

testMap = Logic.load_map()

robo1 = Logic.Robo((0,0))
robo2 = Logic.Robo((1,1))

robo2.path = [(1,1),(1,2),(1,3),(1,4),(2,4),(2,5)]

robots = [robo1, robo2]

Render.init_window()

while True:
    pygame.display.update()
    Render.test_draw(testMap, robots)
    Render.draw_path(robo2)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
