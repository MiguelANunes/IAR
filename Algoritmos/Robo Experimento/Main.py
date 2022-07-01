from contextlib import redirect_stdout

with redirect_stdout(None):
    # Omitindo a mensagem de boas vindas do pygame
    import pygame #pip install pygame
    from pygame.locals import *

import argparse, copy, sys
import Render, Logic, FileHandler

WAITTIME = 250_000
ALGORITHM = ""

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

def simulate(robot, possible_moves:list, simulationMap:list, itemList:list, factoryList:list, algorithm) -> int:
    """
    Executa um passo da simulação, de acordo com o estado atual do robô
    Retorna o custo do último caminho calculado pelo robô
    """

    if robot.state == 0: # estado procurando
        return Logic.state_search(robot, possible_moves, simulationMap, itemList, factoryList, algorithm)
    elif robot.state == 1: # estado calculando path
        pass # se o robô está calculando o path, não há nada para fazer aqui
    else: # estado executando path
        Logic.state_fetch(robot, simulationMap, itemList, factoryList)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-A", "--AStar", help="Executa o experimento com o Algoritmo A*", 
    action="store_true", dest="AStar")
    parser.add_argument("-D", "--Dijkstra", help="Executa o experimento com o Algoritmo de Dijkstra (sem heurística)", 
    action="store_true", dest="Dijkstra")
    parser.add_argument("-G", "--GDFS", help="Executa o experimento com o Algoritmo de Greedy (sem custo)", 
    action="store_true", dest="Greedy")
    parser.add_argument("-I", "--index", help="Indica qual o número dessa execução", 
    type=int, metavar='N', dest="index")
    parser.add_argument("-W", "--waitFor", help="Número de operações inúteis que devem ser feitas entre passos do algoritmo, usado para artificialmente desacelerar a execução. Padrão = 250_000", 
    type=int, metavar='N', dest="waitFor")

    return parser.parse_args()

def parse(args):

    algorithm = None
    index = -1

    global ALGORITHM
    global WAITTIME

    if (args.AStar and args.Dijkstra) or (args.AStar and args.Greedy) or (args.Dijkstra and args.Greedy):
        # Não posso executar dois algoritmos ao mesmo tempo
        exit()

    if args.AStar or (not args.AStar and not args.Dijkstra and not args.Greedy):
        # Se falou pra usar o A*, ou se não forneceu nenhum alg, usa o A*
        ALGORITHM = "AStar"
        algorithm = Logic.AStar

    if args.Dijkstra:
        ALGORITHM = "Dijkstra"
        algorithm = Logic.Dijkstra

    if args.Greedy:
        ALGORITHM = "Greedy"
        algorithm = Logic.Greedy

    if args.waitFor != None:
        WAITTIME  = args.waitFor

    if args.index != None:
        index = args.index
    else:
        print("Erro, é necessário forncer o número da simulação",file=sys.stderr)
        exit()
    
    return (algorithm, index)

def main_loop(simulationMap, robot, factoryList:list, itemList:list, algorithm, index):
    """
    Loop principal da simulação
    Cria o mapa, fábrica, itens, robô, janela do pygame e roda a simulação em loop
    """
    
    totalCost     = 0
    totalExpanded = 0
    randomMoves   = 0

    # passando uma cópia da lista de fábricas para o robô
    # caso eu não faça isso, toda vez que mudar a lista do robô, também mudo a lista global
    # e isso é muito ruim
    robot.set_factories(copy.deepcopy(factoryList)) 

    possible_moves = [(0,-1),(0,1),(-1,0),(1,0)]
    # apenas se move esq/dir cima/baixo

    Logic.set_wait(WAITTIME)

    Render.init_window(ALGORITHM, index)
    Render.draw(simulationMap, itemList, factoryList, robot)
    pygame.display.update()

    if ALGORITHM == "AStar":
        # Como toda execução tem o mesmo estado inicial, basta salvar apenas
        # o estado inicial quando rodo o A*, visto que esse sempre é o primeiro alg de
        # toda a bateria de testes
        Render.save(f"Start {str(index)}")

    path  = False
    pause = False
    while(True):
        
        if not pause:
            pause = check_pause()
            path = False
        else:
            if not path and robot.path != None: # garantindo que vai desenhar o path do robô quando estiver pausado
                Render.draw_colored_border(robot.path,(255,0,0))
                pygame.display.update()
                path = True
            pause = check_resume()
        
        if pause == None:
            return totalCost

        if not pause:
            result = simulate(robot, possible_moves, simulationMap, itemList, factoryList, algorithm)
            if result != None and result != 1:
                totalCost     += result[0]
                totalExpanded += result[1]
            elif result == 1:
                randomMoves += 1

            Render.draw(simulationMap, itemList, factoryList, robot)
            pygame.display.update()

        if robot.factories == []:
            Render.save(ALGORITHM+"_"+str(index)+" end")
            return (totalCost, totalExpanded, randomMoves)

def main():
    """
    Função principal da simulação
    Gera o mapa, o robô, as fábricas e os obstáculos e manda isso pro loop principal
    No loop principal, os itens são gerados e a simulação começa
    Sobre os argumentos de linha de comando definidos a baixo:

        -A Executa o experimento com o algoritmo A*

        -D Executa o experimento com o algoritmo de Dijkstra, isto é, sem a heurística de distância

        -G Executa o experimento com o Algoritmo de Best-First Search, isto é, sem custo nas células do mapa

        -W N define que N operações inúteis são feitas entre passos do algoritmo, usado para desacelerar a execução

        -I N define que essa é a N-ésima execução desse experimento, N \in {0,1,2,3,4}

    Uso dos argumentos:
        python3 Main.py [-h | [-A | -D | -G] -W N -I N]
    """

    # argumentos de linha de comando

    args = parse_args()
    algorithm, index = parse(args)

    simulationMap = FileHandler.load_map()
    robot         = FileHandler.generate_robot(simulationMap)
    itemList      = FileHandler.generate_items(simulationMap, ignore=FileHandler.load_items())
    factoryList   = FileHandler.generate_factories(simulationMap, ignore=FileHandler.load_factories())

    cost, expanded, randomMoves = main_loop(simulationMap, robot, factoryList, itemList, algorithm, index)

    FileHandler.write_result(ALGORITHM+"_"+str(index), cost, expanded, randomMoves)

if __name__ == "__main__":
    main()
