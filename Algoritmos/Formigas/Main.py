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
    file_formigueiro = "dump/formigueiro_Iter"+str(iteracao)+".txt"

    with open(file_formigueiro, 'w')  as f:
        with redirect_stdout(f):
            for linha in formigueiro:
                for item in linha:
                    print(item, end=" ")
                print()

def dump_formigueiro2(formigueiro, iteracao):
    file_formigueiro = "dump/formigueiro2D"+str(iteracao)+".txt"

    with open(file_formigueiro, 'w')  as f:
        with redirect_stdout(f):
            for x in range(50):
                for y in range(50):
                    if formigueiro[x][y] != 0:
                        print(x,y,formigueiro[x][y], end=" ")
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

def render_dump2():
    file_list = []
    with os.scandir("dump/") as folder:
        for item in folder:
            if item.name.endswith("txt"):
                file_list.append(item)
    
    print("Escolha a Iteração")
    for i,file in enumerate(file_list):
        name = file.name.replace("formigueiro2D","")
        name = name.replace(".txt","")
        print(i, name)

    iteracao = file_list[int(input())].name
    Render.draw_dump(iteracao, DISPLAY, width, height)
    print("Aperte Espaço p/ salvar uma imagem desta iteração, qualquer outra tecla para sair")
    while True:
        end_simulation(iteracao)
    pygame.quit()

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

def terminar_formigas(formigueiro, formigas, possible_moves):
    for f in formigas:
        if f.current_state == 0:
            formigas.remove(f)
        else:
            Logic.state_carrying(f,formigueiro, possible_moves)

def end_simulation(iteracao):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Execução salva como formigueiro",str(iteracao),"END.jpg")
                pygame.image.save(DISPLAY , f"formigueiro{str(iteracao)}END.jpg")
                pygame.quit()
                sys.exit()
            else:
                pygame.quit()
                sys.exit()

def main_loop(exec_args):

    limite_iter = None
    render_period = 1
    txt_dump = None
    save_period = None
    raio = 1
    extra_iter = 0
    # no_render = False

    if "iterlimit" in exec_args:
        limite_iter = exec_args["iterlimit"]
    if "renderperiod" in exec_args:
        render_period = exec_args["renderperiod"]
    if "textdump" in exec_args:
        txt_dump = exec_args["textdump"]
    if "SaveMatrix" in exec_args:
        save_period = exec_args["SaveMatrix"]
    if "raio" in exec_args:
        raio = exec_args["raio"]
    # if "norender" in exec_args:
    #     no_render = True
    if "readfrom" in exec_args:
        filename = exec_args["readfrom"]
        if "size" in exec_args:
            size = exec_args["size"]
        else: 
            size = 2
        formigueiro, formigas = Logic.read_formigueiro(size, filename)
    else:
        formigueiro, formigas = Logic.cria_formigueiro(2)

    iteracao = 0

    possible_moves = []
    for i in range(-raio, raio+1):
        for j in range(-raio, raio+1):  
            possible_moves.append((i,j))

    pause = False
    end = False
    printed = False
    while True:

        if pause and not end:
            pause = check_resume()
        elif not end:
            pause = check_pause()

        if end:
            while formigas != []:
                terminar_formigas(formigueiro, formigas, possible_moves)
                Render.draw(formigueiro, formigas, DISPLAY, width, height, size)
                pygame.display.update()
                extra_iter += 1
            if formigas == []:
                if not printed:
                    print("Fim da Simulação!", iteracao, "Iterações foram Executadas")
                    print("Aperte Espaço p/ salvar uma imagem desta iteração, qualquer outra tecla para sair")
                    print("Foram executadas", extra_iter, "iterações a mais para remover as formigas que ainda carregavam itens")
                    printed = True
                end_simulation(iteracao)


        if pause == None:
            return

        if txt_dump != None and iteracao % txt_dump == 0:
            dump_formigueiro(formigueiro, iteracao)

        if save_period != None and iteracao % save_period == 0:
            pygame.image.save(DISPLAY , "dump/formigueiro"+str(iteracao)+".jpg")
            
        if not pause and not end:

            if iteracao % render_period == 0:
                Render.draw(formigueiro, formigas, DISPLAY, width, height, size)
                pygame.display.update()
            # input()
        
            simulate(formigueiro, formigas, possible_moves)

            if "iterlimit" in exec_args:
                if limite_iter != None and iteracao >= limite_iter:
                    end = True
                else:
                    iteracao += 1
            
def main():
    exec_args = dict()

    # argumentos de linha de comando
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius", help="Define o raio de visão das formigas, padrão 1", type=int, metavar='N')
    parser.add_argument("--iterlimit", help="Limite de Iterações da Simulação", type=int, metavar='N')
    parser.add_argument("--renderperiod", help="Quantas Iterações devem ser executadas antes de renderizar", 
    type=int, metavar='N')
    parser.add_argument("--textdump", help="Quantas Iterações devem ser executadas antes de escrever a matriz num arquivo", 
    type=int, metavar='N')
    parser.add_argument("--savematrix", help="Quantas Iterações devem ser executadas antes salvar uma imagem da matriz", 
    type=int, metavar='N')
    parser.add_argument("--size", help="Tamanhos dos dados", type=int, metavar='N')
    # parser.add_argument("--Alpha", help="Valor p/ parametro alpha", type=int, metavar='N')
    # parser.add_argument("--K1", help="Valor p/ parametro k1", type=int, metavar='N')
    # parser.add_argument("--K2", help="Valor p/ parametro k2", type=int, metavar='N')
    parser.add_argument("--readfrom", help="Define o arquivo fonte dos dados para a simulação", 
    type=str, metavar='filename')
    parser.add_argument("--renderdump", help="Renderiza um dump de uma matriz, não executa a simulação", 
    action="store_true")
    parser.add_argument("--norender", help="Não renderiza a simulação, salva a imagem ao final da execução", 
    action="store_true")
    args = parser.parse_args()

    if args.radius:
        exec_args["raio"] = args.radius
    if args.iterlimit:
        exec_args["iterlimit"] = args.iterlimit
    if args.renderperiod:
        exec_args["renderperiod"] = args.renderperiod
    if args.textdump:
        exec_args["textdump"] = args.textdump
    if args.savematrix:
        exec_args["savematrix"] = args.savematrix
    if args.size:
        exec_args["size"] = args.size
    if args.readfrom:
        exec_args["readfrom"] = args.readfrom
    if args.norender:
        exec_args["norender"] = args.norender
    if args.renderdump:
        render_dump()
        return

    pygame.display.set_caption("Formigas")
    DISPLAY.fill((0,128,0))

    main_loop(exec_args)

if __name__ == "__main__":
    main()