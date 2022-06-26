import pygame, argparse, copy     #pip install pygame
from pygame.locals import *

import Render, Logic

# TODO: Adicionar comentários de docstring para as funções

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
        return Logic.state_search(robot, possible_moves, simulationMap, itemList)
    elif robot.state == 1: # estado calculando path
        pass # se o robô está calculando o path, não há nada para fazer aqui
    else: # estado executando path
        Logic.state_fetch(robot, simulationMap, itemList, factoryList)

def main_loop(robotPos:tuple=None,factoriesPos:list=None, obstacles:tuple=None) -> int:
    """
    Loop principal da simulação
    Cria o mapa, fábrica, itens, robô, janela do pygame e roda a simulação em loop
    """

    pause = True
    end = False

    Render.init_window() # inicializando a janela do pygame

    simulationMap = Logic.load_map()

    if obstacles[0]: # inserindo os obstáculos no mapa
        choice = input("Inserir obstáculos? (y/n) ")
        if choice.casefold() == 'y'.casefold() or choice.casefold() == 's'.casefold():
            choice = input("Ler obstáculos de um arquivo? (y/n) ")
            
            # lendo obstaculos de um arquivo
            if (obstacles[1] or choice.casefold() == 'y'.casefold()) and choice.casefold() != 'n'.casefold(): 
                obstaculos = Logic.load_obstacles()
                if obstaculos == None:
                    print("Erro, não achei ou não consegui abrir o arquivo obstaculos.txt na pasta inputs")
                    return
                for posX,posY in obstaculos:
                    simulationMap[posX][posY].set_obstacle()

            else: # inserindo manualmente
                Logic.generate_obstacles(simulationMap)

    robot         = Logic.generate_robot(simulationMap, robotPos)
    robotPos      = robot.position
    factoryList   = Logic.generate_factories(simulationMap, robotPos, factoriesPos)
    itemList      = Logic.generate_items(simulationMap, robotPos)
    totalCost     = 0

    # passando uma cópia da lista de fábricas para o robô
    # caso eu não faça isso, toda vez que mudar a lista do robô, também mudo a lista global
    # e isso é muito ruim
    robot.set_factories(copy.deepcopy(factoryList)) 

    possible_moves = [(0,-1),(0,1),(-1,0),(1,0)]
    # apenas se move esq/dir cima/baixo
    
    Render.draw(simulationMap, itemList, factoryList, robot)
    pygame.display.update()

    print("\n***********\n")
    print("Aperte espaço para pausar/retomar")
    print("Aperte escape para sair\n")
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

            Render.draw(simulationMap, itemList, factoryList, robot)
            pygame.display.update()

        if robot.factories == []:
            return totalCost

def main():

    """
    Função principal da simulação
    Sobre os argumentos de linha de comando definidos a baixo:
        -h printa um menu de ajuda explicando os argumentos e não executa o programa
        -R pula a leitura da posição do robô de um arquivo
        -F pula a leitura da posição das fábricas de um arquivo
        -O pula a inserção de obstáculo, por linha de comando ou arquivo
        -I insere obstáculo apenas por arquivo
        As flags -O e -I são mutuamente exclusivas, tentar executar o programa com as duas causará erro
    Uso dos argumentos:
        python3 Main.py [-h | [-R] [-F] [-O | -I]]
    """
    # TODO: Implementar arg de linha de comando para tempo de espera
    # TODO: Implementar arg de linha de comando que começa despausado
    robotPos  = None
    factories = None

    # argumentos de linha de comando
    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--noRobot", help="Pula leitura de posição do robô", 
    action="store_true", dest="readRobot")
    parser.add_argument("-F", "--noFactory", help="Pula leitura de posição das fábricas", 
    action="store_true", dest="readFactory")
    parser.add_argument("-O", "--noObstacle", help="Pula a inserção de obstáculos", 
    action="store_true", dest="noObstacle")
    parser.add_argument("-I", "--insertObstacle", help="Insere obstáculos a partir de um arquivo (pula inserção manual)", 
    action="store_true", dest="insertObstacle")
    args = parser.parse_args()

    if args.noObstacle and args.insertObstacle:
        print("Erro, flags -I e -O são mutuamente exclusivas")
        return

    if not args.readRobot:
        robotPos  = get_custom_robot_position()
    if not args.readFactory:
        factories = get_custom_factory_position()
    obstacles     = (not args.noObstacle, args.insertObstacle)

    cost = main_loop(robotPos, factories, obstacles)

    print("Ao fim da execução, o custo total dos caminhos percorridos pelo robô foi:",cost)

if __name__ == "__main__":
    main()
