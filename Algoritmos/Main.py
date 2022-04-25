from random import randint
from contextlib import redirect_stdout

import pygame       #pip install pygame
from pygame.locals import *

import sys, os, Render, Logic

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

def main_loop(DISPLAY):
    formigueiro, formigas = Logic.cria_formigueiro()
    iteracao = 0

    pause = False
    while(True):

        if pause:
            pause = check_resume()
        else:
            pause = check_pause()

        if pause == None:
            return

        if iteracao % 500 == 0:
            dump_formigueiro(formigueiro, iteracao)
            
        if not pause:
            Render.draw(formigueiro, formigas, DISPLAY, width, height)
            pygame.display.update()
            simulate(formigueiro, formigas)

            if iteracao % 1000 == 0:
                pygame.image.save(DISPLAY , "dump/formigueiro"+str(iteracao)+".jpg")
            
            iteracao += 1


def main():
    pygame.init()
    DISPLAY = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption("Formigas")
    DISPLAY.fill((255,255,255))

    main_loop(DISPLAY)

    # print("Renderizar Iteração Passada? [y/n]")
    # if input() not in ["y","Y","s","S"]:
    return

    file_list = []
    with os.scandir("dump/") as folder:
        for item in folder:
            if item.name.endswith("txt"):
                file_list.append(item)
    
    print("Escolha a Iteração")
    for i,file in enumerate(file_list):
        name = file.name.replace("formigueiro","")
        name = name.replace(".txt","")
        print(i, name)

    Render.draw_dump(file_list[int(input())].name, DISPLAY, width, height)
    input("Enter p/ sair")
    pygame.quit()

if __name__ == "__main__":
    main()