from random import choice

import Render, Classes, Main

WAITTIME = None

def set_wait(wait):
    """
    Função que define o tempo de espera
    """
    global WAITTIME
    WAITTIME = wait

def wait(ticks:int=None) -> None:
    """
    Opcionalmente recebe um número e faz operações inúteis para gastar tempo e artificialmente tornar o
    algoritmo mais lento
    Não retorna nada
    """
    ticks = WAITTIME if ticks == None else ticks
    i = 0
    for _ in range(ticks):
        i += 1

def is_valid(pos:tuple):
    """Verifica se uma tupla é uma posição válida do mapa"""
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < 42 and pos[1] < 42

def state_search(robot, possible_moves:list, simulationMap:list, listItems:list):
    """
    Estado de procura do robô, aqui ele procura por itens pelo mapa calcula o caminho até eles e vai até lá, 
        Se o robô já tiver o item que uma fábrica precisa, calcula o caminho até ela e vai até ela
    Se o robô não achar nenhum item, faz um movimento aleatório
    """

    # TODO: Mudar maneira que lido com a busca de itens,
    # Colocar todos numa lista e ir de um em um - talvez colocar essa lista no robô

    posX, posY = robot.position
    raio = robot.radius

    # TODO: Confirmar que ele sempre entrega a ferramenta certa
    # Para cada fábrica que o robô não satisfez, parece que ao final (quando tem request = 1) entrega uma ferramenta mesmo se não tiver ela
    for fabrica in robot.factories:
        x,y = fabrica.position
        for tipoItem in robot.get_content_type():
            # Se o robô tem o item que essa fábrica quer
            if tipoItem == fabrica.request[1] and fabrica.request[0] > 0:
                # Vai entregar ele

                print(f"Indo até a fábrica {fabrica.name} entregar {robot.get_content_name_by_type(tipoItem)}")
                print("contents:",robot.contents)
                print("itemPos:",robot.itemPos)
                robot.change_state(1)
                robot.targetFactory = fabrica
                print("targetFact:",robot.targetFactory)
                result = state_find_path(robot.position, (x,y), possible_moves, simulationMap)

                if result != (None, None):
                    robot.path = result[0]
                    cost = result[1]
                    print("Custo do Caminho:",cost)
                else:
                    print(f"Não achei um caminho de {robot.position} para {(x,y)}!!!")

                robot.change_state(2)
                return cost

    positionList = []
    for i in range(-raio, raio+1):
        for j in range(-raio, raio+1):
            x, y = posX+i, posY+j
            
            if not is_valid((x,y)):
                continue

            if simulationMap[x][y].is_obstacle(): # ignora os obstaculos
                continue
            
            if simulationMap[x][y].contents != None: # se achou alguma coisa no mapa
                item = simulationMap[x][y].contents

                if item in listItems and not item.tipo in robot.get_content_type():
                    # se achou um item que não está carregando, põe ele na lista para ser buscado
                    # positionList.append((x,y))
                    # TODO implementar robô pegar itens da lista um de cada vez, somando seus custos ao total

    # # Para cada item na lista de item a serem buscados
    # # Veja qual o caminho de menor custo entre todos eles
    # pathRobot = dict()
    # # costRobot = dict()
    # pathItems = dict()
    # # costItems = dict()
    # for pos in positionList:
    #     # Calculando caminho e custo p/ o robô ir para uma dada célula
    #     result = state_find_path(robot.position, pos, possible_moves, simulationMap)
    #     if result != (None, None):
    #         pathRobot[pos] = result#[0]
    #         #costRobot      = result[1]
        
    #     tempDist = dict()
    #     tempCost = dict()
    #     # Calculando caminho e custo para ir de uma célula para outra
        
    #     for pos1 in positionList:
    #         if pos == pos1: continue
    #         if pos1 in pathItems:
    #             # Se já calculou o caminho de uma célula para outra, não precisa recalcular,
    #             #   basta inverter o caminho e tomar o mesmo custo
    #             tempDist[pos1] = (pathItems[pos1][0].reverse(), pathItems[pos1][1])
    #             #tempCost[pos1] = pathItems[pos1][1]
    #         else:
    #             result = state_find_path(pos, pos1, possible_moves, simulationMap)
    #             if result != (None, None):
    #                 tempDist[pos1] = result#[0]
    #                 #tempCost[pos1] = result[1]
        
    #     # Para cada item, guardo o caminho e custo dele para todos os outros items que conheço
    #     # Isto é, pathItems é um dict de dicts
    #     pathItems[pos] = tempDist
    #     #costItems[pos] = tempCost

    # # Selecionando o caminho de um item para outro que tem o menor custo
    # # firstItem = pathItems.keys()[0] # keys retorna uma lista de chaves, quero a primeira
    # leastItems = dict()
    # minItem  = None
    # for item in pathItems: 
    #     # para cada item na lista de items que o robô pode acessar
    #     minCost = 1_000_000

    #     for subItem in pathItems[item]: 
    #         # para cada subitem que o item externo pode acessar
    #         if subItem in leastItems: continue # se já está na sequência, ignora
    #         path, cost = pathItems[item][subItem]
    #         if cost < minCost:
    #             # se o custo dele é menor que o menor custo so far, ele se torna o menor custo so far
    #             minCost = cost
    #             minItem = item

    #     leastItems[item] = minItem
        
    #     if minCost == 1_000_000:
    #         # se passou do loop interno sem mudar o custo
    #         pass



        # newDict       = get_all_but_one(costItems, minCosts.keys())
        # minCosts[pos] = min(newDict[pos], key=newDict[pos].get)
        # newDict é um dict de dicts igual a costItems, porém seu dict mais interno não
        # contém nenhuma chave que está em minCosts
        # Isso serve para evitar que caminhos circulares sejam dados para o robô
        # minCosts é um dict que associa tuplas a tuplas
        # isto é, minCost[(x,y)] = (xi,yi) == O caminho de menor custo a partir de (x,y) é para (xi,yi)

    # finalCost[pos] = costItems[pos] + costRobot[pos]

                    robot.change_state(1)

                    print("Achou um(a)", item.name)
                    robot.itemPos.append((x,y))
                    result = state_find_path(robot.position, (x,y), possible_moves, simulationMap)

                    if result != (None, None):
                        robot.path = result[0]
                        cost = result[1]
                        print("Custo do Caminho:",cost)
                    else:
                        print(f"Não achei um caminho de {robot.position} para {(x,y)}!!!")
                    robot.change_state(2)
                    return cost
    
    # se chegou aqui é pq não achou nada, logo faz um movimento aleatório
    random_move(robot, possible_moves, simulationMap)

def state_find_path(originPos:tuple, targetPos:tuple, possible_moves:list, simulationMap:list) -> tuple:
    """
    Executa o algoritmo A* e retorna o caminho calculado e o custo desse caminho, se ele existir
    """
    result = AStar(originPos, targetPos, possible_moves, simulationMap)

    if result != None:
        path, cost = result
    else:
        return (None, None)

    return (path, cost)

def state_fetch(robot, simulationMap:list, listItems:list, listFactories:list) -> None:
    """
    Executa o path que o robô calculou, movendo de célula em célula até chegar no seu objetivo
    """

    if not isinstance(robot.path, list) or robot.path == []:
        robot.path = []
        robot.change_state(0)
        return

    Render.draw_colored_border(robot.path, (255,0,0))
    Render.pygame.display.update()

    new_pos = robot.path.pop(0)

    wait()

    robot.move_to(new_pos)
    
    cell = simulationMap[new_pos[0]][new_pos[1]]
    if robot.position in robot.itemPos: 
        # Se o robô está numa célula que tem um item na lista de itens que tem pra pegar, pega ele
        del listItems[listItems.index(cell.contents)]
        del robot.itemPos[robot.itemPos.index(cell.contents.position)]
        robot.pick_up(cell)
        if robot.path == []:
            # Se pegou todos os items que tinha pra pegar, volta pro estado 0
            robot.path = None
            robot.change_state(0)

    if cell.contents in listFactories and robot.targetFactory != None:
        if robot.targetFactory.compare(cell.contents):
            # Se o robô achou a fábrica para qual tenho que entregar o item que está carregando, entrega

            # Tenho que printar o request com -1 pois esse print é feito antes de entregar
            # É feito antes de entregar pois depois de entregar eu talvez não tenha mais o nome do item que foi entrege
            # Visto que ele é deletado
            print(f"A fábrica {cell.contents.name} agora precisa de {cell.contents.request[0]-1} {robot.get_content_name_by_type(cell.contents.request[1])}(s)\n")
            robot.deliver(cell.contents)
            robot.targetFactory = None

            # Se entregou, volta para o estado 0, não faz várias entregas de uma vez
            robot.change_state(0)

    if robot.path == []:
        robot.path = None

def random_move(robot, possible_moves:list, simulationMap:list) -> None:
    """
    Faz um movimento aleatório pelo mapa
    """
    posX, posY = robot.position
    candidates = []

    for i,j in possible_moves:
        x, y = posX+i, posY+j

        if not is_valid((x,y)):
            continue
        candidates.append((x,y))
    
    move = choice(candidates)

    if len(candidates) == 1:
        # se o robô só tem um movimento possível, faz ele, mesmo que isso leve a posição anterior
        # ou a atual
        while simulationMap[move[0]][move[1]].is_obstacle():
            move = choice(candidates)
                    
        wait()
        return robot.move_to(move)
    elif len(candidates) == 2:
        # se tem dois movimentos possíveis, faz qualquer um que não leve a posição anterior
        while move == robot.position or simulationMap[move[0]][move[1]].is_obstacle():
            move = choice(candidates)
        
        wait()
        return robot.move_to(move)
    
    while move == robot.pastPos or move == robot.position or simulationMap[move[0]][move[1]].is_obstacle():
        move = choice(candidates)
    
    wait()
    return robot.move_to(move)

def distancia(pos1, pos2): 
    """Distância de Manhattan"""
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

def AStar(startingPos:tuple, target:tuple, possible_moves:list, simulationMap):
    """
    Algoritmo A*
    Dadas duas células quaisquer, calcula o caminho de menor custo entre elas, se ele existir
    Retorna uma tupla contendo o caminho em forma de lista de tuplas (x,y) e o custo dele
    """

    fronteira = Classes.PriorityQueue(startingPos, 0) # fila de células que o robô vai checar e custo para chegar lá
    caminho = dict() # dict de célula p/ células, caminho[(x,y)] = (x1,y1) ==> melhor caminho para (x,y) é de (x1,y1)
    caminho[startingPos] = None # não há caminho para a célula inicial
    custos = dict() # custo p/ chegar em celulas, custos[(x,y)] = n ==> custo para chegar em (x,y) é n
    custos[startingPos] = 0

    pause = False

    while fronteira.len() > 0:

        if not pause:
            pause = Main.check_pause()
        else:
            pause = Main.check_resume()

        if pause:
            continue

        wait()

        Render.draw_colored_border(fronteira.to_list())
        Render.pygame.display.update()
        _, posicao_atual = fronteira.pop()

        if posicao_atual == target:
            # se achou o alvo, sai do loop e retorna uma tupla contendo o path e o custo total desse path
            return (rebuildPath(caminho, target, startingPos), custos[posicao_atual] + simulationMap[target[0]][target[1]].cost)

        vizinhos = []
        for i in possible_moves: # gerando todos os vizinhos do nó atual
            v = posicao_atual[0]+i[0],posicao_atual[1]+i[1]
            if not is_valid(v):
                continue
            if not simulationMap[v[0]][v[1]].is_obstacle():
                vizinhos.append(v) # não insere vizinhos que são obstáculos nem vizinho inválidos
        
        for vizinho in vizinhos:
            novo_custo = custos[posicao_atual] + simulationMap[vizinho[0]][vizinho[1]].cost
            swap = False

            # .get retorna o valor associado a chave vizinho, caso ela exista, -1 caso não
            if novo_custo < custos.get(vizinho, -1): 
                swap = True

            if vizinho not in custos or swap:
                custos[vizinho] = novo_custo
                fronteira.push((novo_custo + distancia(target, vizinho)), vizinho)
                caminho[vizinho] = posicao_atual

    return None

def rebuildPath(path:dict, orig:tuple, dest:tuple) -> list:   
    """
    Reconstrói o caminho gerado pelo A*, indo da última célula do 
        caminho (primeira na lista retornada pelo alg) até a primeira (última na lista retornada pelo alg)
    Retorna uma lista de tuplas
    """

    if orig == dest:
        return [orig]

    target = path[orig]
    finalPath = [orig]

    if orig == target:
        return finalPath

    i, j = target
    finalPath.append(target)
    while path[(i,j)] != dest:
        finalPath.append(path[(i,j)])
        if path[(i,j)] == None:
            break
        i, j = path[(i,j)]

    finalPath.append(dest)
    finalPath.reverse()

    finalPath = [x for x in finalPath if x != None] # sanity check

    return finalPath
