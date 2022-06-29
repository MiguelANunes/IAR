import pygame, argparse, copy     #pip install pygame
from pygame.locals import *

import Render, Logic, FileHandler

WAITTIME = 250_000

def get_confirmation(message:str):
    choice = input(message+" (y/n) ")
    if choice.casefold() == 'y'.casefold() or choice.casefold() == 's'.casefold():
        return True
    else:
        return False

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

def main_loop(simulationMap, robot, factoryList:list=None, itemList:list=None):
    """
    Loop principal da simulação
    Cria o mapa, fábrica, itens, robô, janela do pygame e roda a simulação em loop
    """
    pause = True
    totalCost   = 0

    # passando uma cópia da lista de fábricas para o robô
    # caso eu não faça isso, toda vez que mudar a lista do robô, também mudo a lista global
    # e isso é muito ruim
    robot.set_factories(copy.deepcopy(factoryList)) 

    possible_moves = [(0,-1),(0,1),(-1,0),(1,0)]
    # apenas se move esq/dir cima/baixo

    Logic.set_wait(WAITTIME)

    Render.draw(simulationMap, itemList, factoryList, robot)
    pygame.display.update()

    print("\n***********\n")
    print("Aperte espaço para pausar/retomar")
    print("Aperte escape para sair\n")
    path = False
    while(True):
        
        if not pause:
            pause = check_pause()
            path = False
        else:
            if not path: # garantindo que vai desenhar o path do robô quando estiver pausado
                Render.draw_colored_border(robot.path,(255,0,0))
                pygame.display.update()
                path = True
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
            print("Fim da simulação!")
            print("Ao fim da execução, o custo total dos caminhos percorridos pelo robô foi:",totalCost)
            input("Aperte Enter (no terminal) para sair!")
            return

def main():

    """
    Função principal da simulação
    Gera o mapa, o robô, as fábricas e os obstáculos e manda isso pro loop principal
    No loop principal, os itens são gerados e a simulação começa
    Sobre os argumentos de linha de comando definidos a baixo:

        -h Printa um menu de ajuda explicando os argumentos e não executa o programa

        -r Lê posição do robô por arquivo
        -R Pula a leitura da posição do robô (arquivo e usuário)

        -r Lê posição da fábrica por arquivo
        -F Pula a leitura da posição das fábricas (arquivo e usuário)

        -o Lê posição dos obstáculos
        -O Não insere obstáculo

        -W N define que N operações inúteis são feitas entre passos do algoritmo, usado para desacelerar a execução

        As flags (-r, -R), (-f -F) e (-o, -O) são mutuamente exclusivas, tentar executar o programa com as duas causará erro
    Uso dos argumentos:
        python3 Main.py [-h | [-r | -R] [-f | -F] [-o | -O] [-W N]]
    """

    # argumentos de linha de comando
    # TODO: Mover isso para um função separada
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--readRobot", help="Lê posição do robô por arquivo", 
    action="store_true", dest="readRobot")
    parser.add_argument("-R", "--noRobot", help="Pula input de posição do robô (arquivo e usuário)", 
    action="store_true", dest="noRobot")

    parser.add_argument("-f", "--readFactory", help="Lê posição das fábricas por arquivo", 
    action="store_true", dest="readFactory")
    parser.add_argument("-F", "--noFactory", help="Pula leitura de posição das fábricas (arquivo e usuário)", 
    action="store_true", dest="noFactory")

    parser.add_argument("-o", "--readObstacle", help="Lê posição dos obstáculos por arquivo", 
    action="store_true", dest="readObstacle")
    parser.add_argument("-O", "--noObstacle", help="Não insere obstáculo", 
    action="store_true", dest="noObstacle")

    parser.add_argument("-W", "--waitFor", help="Número de operações inúteis que devem ser feitas entre passos do algoritmo, usado para artificialmente desacelerar a execução. Padrão = 250_000", 
    type=int, metavar='N', dest="waitFor")

    args = parser.parse_args()

    if args.readObstacle and args.noObstacle:
        print("Erro, flags -o e -O são mutuamente exclusivas")
        return

    if args.readRobot and args.noRobot:
        print("Erro, flags -r e -R são mutuamente exclusivas")
        return

    if args.readFactory and args.noFactory:
        print("Erro, flags -f e -F são mutuamente exclusivas")
        return

    Render.init_window() # inicializando a janela do pygame

    simulationMap = FileHandler.load_map()
    robot = None

    if not args.noObstacle: # Se quero obstáculos
        if args.readObstacle: # Se quero ler do arquivo
            FileHandler.get_obstacles(simulationMap, True, False)
        else: # Se quero ler manual
            if get_confirmation("Definir posição dos obstáculos?"):
                if get_confirmation("Ler de um arquivo?"):
                    FileHandler.get_obstacles(simulationMap, True, False)
                else:
                    FileHandler.get_obstacles(simulationMap, False, True)

    cond1   = False
    defined = False

    if args.readRobot: # Se quero ler do arquivo
        cond1   = True
        defined = True
    if not args.readRobot and args.noRobot: # Se quero gerar automaticamente
        cond1   = False
        defined = True

    if defined:
        robot = FileHandler.get_robot(simulationMap, cond1, False)
    else:
        cond1, cond2 = False, False
        if get_confirmation("Definir posição do robô"):
            if get_confirmation("Ler de um arquivo?"):
                cond1 = True # Se quero ler do arquivo
            else:
                cond2 = True # Se quero ler manual
        else:
            cond1, cond2 = False, False # Se quero gerar automaticamente
        robot = FileHandler.get_robot(simulationMap, cond1, cond2)

    robotPos = robot.position

    cond1   = False
    defined = False
    if args.readFactory: # Se quero ler do arquivo
        cond1   = True
        defined = True
    if not args.readFactory and args.noFactory: # Se quero gerar automaticamente
        cond1   = True
        defined = True

    if defined:
        factoryList = FileHandler.get_factories(simulationMap, cond1, False, robotPos)
    else:
        cond1, cond2 = False, False
        if get_confirmation("Definir posição das fábricas"):
            if get_confirmation("Ler de um arquivo?"):
                cond1 = True # Se quero ler do arquivo
            else:
                cond2 = True # Se quero ler manual
        else:
            cond1, cond2 = False, False # Se quero gerar automaticamente
        factoryList = FileHandler.get_factories(simulationMap, cond1, cond2, robotPos)

    if args.waitFor != None:
        global WAITTIME
        WAITTIME  = args.waitFor

    itemList = FileHandler.generate_items(simulationMap, robot.position)

    main_loop(simulationMap, robot, factoryList, itemList)

if __name__ == "__main__":
    main()
