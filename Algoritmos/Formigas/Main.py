import argparse
from random import randint
from contextlib import redirect_stdout

import pygame       #pip install pygame
from pygame.locals import *

import sys, os, time, Render, Logic

width, height = 700, 600
pygame.init()
DISPLAY = pygame.display.set_mode((width, height), 0, 32)

def dump_formigueiro(formigueiro, iteracao):
    file_formigueiro = "dump/formigueiro"+str(iteracao)+".txt"

    with open(file_formigueiro, 'w')  as f:
        with redirect_stdout(f):
            for linha in formigueiro:
                for item in linha:
                    print(item, end=" ")
                print()

def render_dump():
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

    iteracao = file_list[int(input())].name
    Render.draw_dump(iteracao, DISPLAY, width, height)
    print("Aperte Espaço p/ salvar uma imagem desta iteração, qualquer outra tecla para sair")
    while True:
        end_simulation(iteracao)
    pygame.quit()

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

def end_simulation(iteracao):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.image.save(DISPLAY , "formigueiro"+str(iteracao)+"END.jpg")
                pygame.quit()
                sys.exit()
                return
            else:
                pygame.quit()
                sys.exit()
                return

def main_loop(exec_args):
    formigueiro, formigas = Logic.cria_formigueiro()
    limite_iter = None
    render_period = 1
    txt_dump = None
    print_period = None
    if "iterlimit" in exec_args:
        limite_iter = exec_args["iterlimit"]
    if "renderperiod" in exec_args:
        render_period = exec_args["renderperiod"]
    if "textdump" in exec_args:
        txt_dump = exec_args["textdump"]
    if "printrender" in exec_args:
        print_period = exec_args["printrender"]
    iteracao = 0

    pause = False
    end = False
    while True:

        if pause and not end:
            pause = check_resume()
        elif not end:
            pause = check_pause()

        if pause == None:
            return

        if end:
            end_simulation(iteracao)

        if txt_dump != None and iteracao % txt_dump == 0:
            dump_formigueiro(formigueiro, iteracao)

        if print_period != None and iteracao % print_period == 0:
            pygame.image.save(DISPLAY , "dump/formigueiro"+str(iteracao)+".jpg")
            
        if not pause and not end:

            if iteracao % render_period == 0:
                Render.draw(formigueiro, formigas, DISPLAY, width, height)
                pygame.display.update()

            simulate(formigueiro, formigas)

            if "iterlimit" in exec_args:
                if limite_iter != None and iteracao >= limite_iter:
                    end = True
                    print("Fim da Simulação!", iteracao, "Iterações foram Executadas")
                    print("Aperte Espaço p/ salvar uma imagem desta iteração, qualquer outra tecla para sair")
            iteracao += 1

            
def main():
    exec_args = dict()

    # argumentos de linha de comando
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterlimit", help="Limite de Iterações da Simulação", type=int, metavar='N')
    parser.add_argument("--renderperiod", help="Quantas Iterações devem ser executadas antes de renderizar", 
    type=int, metavar='N')
    parser.add_argument("--textdump", help="Quantas Iterações devem ser executadas antes de escrever matriz num arquivo", 
    type=int, metavar='N')
    parser.add_argument("--printrender", help="Quantas Iterações devem ser executadas antes salvar uma imagem do frame", 
    type=int, metavar='N')
    parser.add_argument("--renderdump", help="Renderiza um dump de uma matriz, não executa a simulação", 
    action="store_true")
    args = parser.parse_args()

    if args.iterlimit: # implementado
        exec_args["iterlimit"] = args.iterlimit
    if args.renderperiod: # implementado
        exec_args["renderperiod"] = args.renderperiod
    if args.textdump: # implementado
        exec_args["textdump"] = args.textdump
    if args.printrender: # implementado
        exec_args["printrender"] = args.printrender
    if args.renderdump: # implementado
        render_dump()
        return

    pygame.display.set_caption("Formigas")
    DISPLAY.fill((0,128,0))

    main_loop(exec_args)

if __name__ == "__main__":
    main()