from random import randint
from contextlib import redirect_stdout

import pygame, argparse     #pip install pygame
from pygame.locals import *

import Render, Logic, Classes

# TODO: Adicionar comentários de docstring para as funções

# TODO: Sobre inserção de obstaculos: (ter pelo menos alguns desses)
#       fazer uma entrada ou por arquivo de texto
#       ou inserir aleatóriamente
#       ou prompt que da highlight na linha/coluna que será inserido, 
#       com confirmação antes de inserir

def check_pause() -> bool:
    """
    Usa funções do pygame para verificar se espaço ou esc foram apertados
    Se espaço foi apertado, retona True, que faz com que a execução da simulação pause
    Se esc foi apertado, retorna None, que faz com que a simulação termine
    Se nada foi apertado, retona False, que faz com que a simulação continue rodando
    """

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

def check_resume() -> bool:
    """
    Usa funções do pygame para verificar se espaço ou esc foram apertados
    Se espaço foi apertado, retona False, que faz com que a execução da simulação retome
    Se esc foi apertado, retorna None, que faz com que a simulação termine
    Se nada foi apertado, retona True, que faz com que a simulação continue pausada
    """

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

def get_custom_robot_position() -> tuple:
    """
    Tenta ler a posição do robô de um arquivo de entrada
    Se conseguiu ler, retorna a própria posição, se não, retorna None
    """

    robotPos  = None

    choice = input("Ler posicao do robo de arquivo de entrada? (y/n) ")
    if choice.casefold() == 'y'.casefold() or choice.casefold() == 's'.casefold():
        pos = Logic.load_robot()

        if pos == None:
            print("Erro, não achei ou não consegui abrir o arquivo robo.txt na pasta inputs")
        else:
            robotPos = pos

    return robotPos

def get_custom_factory_position() -> dict:
    """
    Tenta ler a posição das fábricas de um arquivo de entrada
    Se conseguiu ler, retorna um dict contendo o tipo de cada fábrica associada
        com sua posição, se não conseguiu retorna None
    """
    factories = None

    choice = input("Ler posicao de fabricas de arquivo de entrada? (y/n) ")
    if choice.casefold() == 'y'.casefold() or choice.casefold() == 's'.casefold():
        posList = Logic.load_factories()

        if posList == None:
            print("Erro, não achei ou não consegui abrir o arquivo fabrica.txt na pasta inputs")
        else:
            factories = posList
    return factories

def simulate(robot, possible_moves:list, simulationMap:list, itemList:list, factoryList:list) -> int:
    """
    Executa um passo da simulação, de acordo com o estado atual do robô
    Retorna o custo do último caminho calculado pelo robô
    """

    if robot.state == 0: # estado procurando
        return Logic.state_search(robot, possible_moves, simulationMap, itemList, factoryList)
    elif robot.state == 1: # estado calculando path
        pass # se o robô está calculando o path, não há nada para fazer aqui
    else: # estado executando path
        Logic.state_fetch(robot, simulationMap, itemList, factoryList)

def main_loop(robotPos:tuple=None,factoriesPos:list=None) -> int:
    """
    Loop principal da simulação
    Cria o mapa, fábrica, itens, robô, janela do pygame e roda a simulação em loop
    """

    pause = False
    end = False

    simulationMap = Logic.load_map()
    robot         = Logic.generate_robot(simulationMap, robotPos)
    robotPos      = robot.position
    factoryList   = Logic.generate_factories(simulationMap, robotPos, factoriesPos)
    itemList      = Logic.generate_items(simulationMap, robotPos)
    totalCost     = 0

    possible_moves = [(0,-1),(0,1),(-1,0),(1,0)]
    # apenas se move esq/dir cima/baixo
    
    Render.init_window() # inicializando a janela do pygame

    pygame.display.update()
    Render.draw(simulationMap, itemList, factoryList, robot)
    while(True):
        
        if not pause:
            pause = check_pause()
        else:
            pause = check_resume()
        
        if pause == None:
            return totalCost

        if not pause:
            cost = simulate(robot, possible_moves, simulationMap, itemList, factoryList)
            if cost != None:
                totalCost += cost

            pygame.display.update()
            Render.draw(simulationMap, itemList, factoryList, robot)

def main() -> None:

    # exec_args = dict()
    robotPos  = None
    factories = None

    # argumentos de linha de comando
    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--noRobot", help="Pula leitura de posição do robô", 
    action="store_true", dest="readRobot")
    parser.add_argument("-F", "--nofactory", help="Pula leitura de posição das fábricas", 
    action="store_true", dest="readFactory")
    args = parser.parse_args()

    if not args.readRobot:
        robotPos = get_custom_robot_position()
    if not args.readFactory:
        factories = get_custom_factory_position()


    print("")
    print("")
    cost = main_loop(robotPos=robotPos, factoriesPos=factories)

    print("Ao fim da execução, o custo total dos caminhos percorridos pelo robô foi:",cost)

if __name__ == "__main__":
    main()
