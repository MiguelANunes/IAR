from random import randint
from contextlib import redirect_stdout

import pygame       #pip install pygame
from pygame.locals import *

import sys, os, time, Render, Logic

width, height = 700, 600

def dump_formigueiro(formigueiro, iteracao):
    file_formigueiro = "dump/formigueiro"+str(iteracao)+".txt"

    with open(file_formigueiro, 'w')  as f:
        with redirect_stdout(f):
            for linha in formigueiro:
                for item in linha:
                    print(item, end=" ")
                print()

def simulate(formigueiro, formigas, possible_moves):
    for f in formigas:
        if f.current_state == 0:
            Logic.state_not_carrying(f, formigueiro, possible_moves)
        else:
            Logic.state_carrying(f,formigueiro, possible_moves)

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

def end_simulation(iteracao, DISPLAY):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print(f"Execução salva como formigueiro{str(iteracao)}-END.jpg")
                pygame.image.save(DISPLAY , f"formigueiro{str(iteracao)}-END.jpg")
                pygame.quit()
                sys.exit()
            else:
                pygame.quit()
                sys.exit()

def terminar_formigas(formigueiro, formigas, possible_moves):
    for f in formigas:
        if f.current_state == 0:
            formigas.remove(f)
        else:
            Logic.state_carrying(f,formigueiro, possible_moves)

def main_loop(DISPLAY):
    formigueiro, formigas = Logic.cria_formigueiro()
    iteracao = 0

    raio = 5
    possible_moves = []
    for i in range(-raio, raio+1):
        for j in range(-raio, raio+1):  
            possible_moves.append((i,j))

    pause = False
    end = False
    limite_iter = 1_000_000
    printed = False
    extra_iter = 0

    while(True):

        if pause and not end:
            pause = check_resume()
        elif not end:
            pause = check_pause()

        if pause == None:
            return

        if end:
            while formigas != []:
                terminar_formigas(formigueiro, formigas, possible_moves)
                Render.draw(formigueiro, formigas, DISPLAY, width, height)
                pygame.display.update()
                extra_iter += 1
            if formigas == []:
                if not printed:
                    print("Fim da Simulação!", iteracao, "Iterações foram Executadas")
                    print("Aperte Espaço p/ salvar uma imagem desta iteração, qualquer outra tecla para sair")
                    print("Foram executadas", extra_iter, "iterações a mais para remover as formigas que ainda carregavam itens")
                    printed = True
                Render.draw(formigueiro, formigas, DISPLAY, width, height)
                pygame.display.update()
                end_simulation(iteracao, DISPLAY)
            
        if not pause and not end:
            if iteracao % 10000 == 0:
                Render.draw(formigueiro, formigas, DISPLAY, width, height)
                pygame.display.update()
            simulate(formigueiro, formigas, possible_moves)
            
            if limite_iter != None and iteracao >= limite_iter:
                end = True
            else:
                iteracao += 1


def main():
    # https://www.geeksforgeeks.org/command-line-arguments-in-python/
    pygame.init()
    DISPLAY = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption("Formigas")
    DISPLAY.fill((0,128,0))

    main_loop(DISPLAY)

    # print("Renderizar Iteração Passada? [y/n]")
    # if input() not in ["y","Y","s","S"]:
    return

if __name__ == "__main__":
    main()