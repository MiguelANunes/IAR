from random import randint, choice
import Render
from Classes import *

# TODO: Mudar um pouco como é feita a ordem de operações do robô
#       Pelo que eu entendi o robô inicialmente sabe onde estão todas as fábricas e oq querem
#       e anda pelo mapa procurando os itens
#       Quando acha algo que uma fábrica quer, vai até ela e entrega o item para ela

def load_map():
    simulationMap = []
    with open("inputs/map.txt") as f:
        for line in f:
            line = (line.replace("\t"," ")).replace(",",".")
            cells = [l.rstrip('\n') for l in line.split(" ") if l != '' and l != '\n']
            cell = [Celula(int(c)) for c in cells]
            simulationMap.append(cell)

    for i in range(42):
        for j in range(42):
            # definindo as posições das células, usando no A*
            simulationMap[i][j].position = (i,j)
    return simulationMap

def load_robot():
    """
    Lê um arquivo que contém 2 valores, que são a posição inicial do robô
    """
    try:
        with open("inputs/robo.txt") as f:
            pos = tuple(map(int, (f.readline().rstrip('\n')).split(" ")))
            return pos
    except OSError:
        return None

def load_factories():
    """
    Lê um arquivo que contém várias linhas seguindo o formato
        tipo, x, y
    Define que a fabrica de tipo 'tipo' estará nas coordenadas (x,y)
    """
    try:
        with open("inputs/fabrica.txt") as f:
            factories = []
            for line in f:
                factories.append(tuple(map(int, (line.rstrip('\n').replace(" ","")).split(","))))
            return factories
    except OSError:
        return None

def generate_factories(simulationMap, ignore:list=None):

    factoryList = []

    pos = (randint(0, 41), randint(0, 41))
    while simulationMap[pos[0]][pos[1]].contents != None:
        pos = (randint(0, 41), randint(0, 41))
    fabricaGraos = Fabrica(0, pos, 8, 0)
    fabricaGraos.set_request(8, 0)
    simulationMap[pos[0]][pos[1]].place(fabricaGraos)
    factoryList.append(fabricaGraos)

    pos = (randint(0, 41), randint(0, 41))
    while simulationMap[pos[0]][pos[1]].contents != None:
        pos = (randint(0, 41), randint(0, 41))
    fabricaBarcos = Fabrica(1, pos, 5, 1)
    fabricaBarcos.set_request(5, 1)
    simulationMap[pos[0]][pos[1]].place(fabricaBarcos)
    factoryList.append(fabricaBarcos)

    pos = (randint(0, 41), randint(0, 41))
    while simulationMap[pos[0]][pos[1]].contents != None:
        pos = (randint(0, 41), randint(0, 41))
    fabricaPetrobras = Fabrica(2, pos, 2, 2)
    fabricaPetrobras.set_request(2, 2)
    simulationMap[pos[0]][pos[1]].place(fabricaPetrobras)
    factoryList.append(fabricaPetrobras)

    pos = (randint(0, 41), randint(0, 41))
    while simulationMap[pos[0]][pos[1]].contents != None:
        pos = (randint(0, 41), randint(0, 41))
    fabricaFundicao = Fabrica(3, pos, 5, 3)
    fabricaFundicao.set_request(5, 3)
    simulationMap[pos[0]][pos[1]].place(fabricaFundicao)
    factoryList.append(fabricaFundicao)

    pos = (randint(0, 41), randint(0, 41))
    while simulationMap[pos[0]][pos[1]].contents != None:
        pos = (randint(0, 41), randint(0, 41))
    fabricaVigas = Fabrica(4, pos, 2, 4)
    fabricaVigas.set_request(2, 4)
    simulationMap[pos[0]][pos[1]].place(fabricaVigas)
    factoryList.append(fabricaVigas)

    return factoryList

def generate_items(simulationMap):

    itemList = []

    for _ in range(20):
        pos = (randint(0, 41), randint(0, 41))
        while simulationMap[pos[0]][pos[1]].tipo != 0 or simulationMap[pos[0]][pos[1]].contents != None:
            pos = (randint(0, 41), randint(0, 41))
        itemBateria = Item(0, pos)
        simulationMap[pos[0]][pos[1]].place(itemBateria)
        itemList.append(itemBateria)

    for _ in range(10):
        pos = (randint(0, 41), randint(0, 41))
        while simulationMap[pos[0]][pos[1]].tipo != 0 or simulationMap[pos[0]][pos[1]].contents != None:
            pos = (randint(0, 41), randint(0, 41))
        itemBraco = Item(1, pos)
        simulationMap[pos[0]][pos[1]].place(itemBraco)
        itemList.append(itemBraco)
    
    for _ in range(8):
        pos = (randint(0, 41), randint(0, 41))
        while simulationMap[pos[0]][pos[1]].tipo != 0 or simulationMap[pos[0]][pos[1]].contents != None:
            pos = (randint(0, 41), randint(0, 41))
        itemBomba = Item(2, pos)
        simulationMap[pos[0]][pos[1]].place(itemBomba)
        itemList.append(itemBomba)

    for _ in range(6):
        pos = (randint(0, 41), randint(0, 41))
        while simulationMap[pos[0]][pos[1]].tipo != 0 or simulationMap[pos[0]][pos[1]].contents != None:
            pos = (randint(0, 41), randint(0, 41))
        itemRefrigeracao = Item(3, pos)
        simulationMap[pos[0]][pos[1]].place(itemRefrigeracao)
        itemList.append(itemRefrigeracao)

    for _ in range(4):
        pos = (randint(0, 41), randint(0, 41))
        while simulationMap[pos[0]][pos[1]].tipo != 0 or simulationMap[pos[0]][pos[1]].contents != None:
            pos = (randint(0, 41), randint(0, 41))
        itemBracoPneumatico = Item(4, pos)
        simulationMap[pos[0]][pos[1]].place(itemBracoPneumatico)
        itemList.append(itemBracoPneumatico)

    return itemList

def is_valid(pos):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < 42 and pos[1] < 42

def state_search(robot, possible_moves, simulationMap, listItems, listFactories):
    # procura por algo, se não acha nada faz um movimento aleatório

    # TODO: Mudar maneira que lido com a busca de itens,
    # Ver como ele quer no pdf

    # TODO: Mudar a maneira que lido com ida até as fábricas
    # Robô deve saber onde ficam as fábricas e ir até elas quando tiver o que precisam

    posX, posY = robot.position
    raio = robot.radius

    for i in range(-raio, raio+1):
        for j in range(-raio, raio+1):
            x, y = posX+i, posY+j
            
            if not is_valid((x,y)):
                continue

            if simulationMap[x][y].is_obstacle(): # ignora os obstaculos
                continue
            
            if simulationMap[x][y].contents != None: # se achou alguma coisa no mapa
                item = simulationMap[x][y].contents

                if item in listItems and not item.tipo in robot.get_contents():
                    # se achou um item que não está carregando, vai buscar ele
                    robot.change_state(1)

                    result = state_find_path(robot, (x,y), possible_moves, simulationMap)

                    if result != None:
                        robot.path = result[0]
                        cost = result[1]
                        print("Custo do Caminho:",cost)

                    robot.change_state(2)
                    return cost
                
                if item in listFactories:
                    # se achou uma fábrica, testa para ver se tem o item que quer
                    if item.request[0] > 0 and item.request[1] in robot.contents:
                        # se tem o que quer, vai entregar
                        robot.change_state(1)

                        result = state_find_path(robot, (x,y), simulationMap, listItems, listFactories)

                        if result != None:
                            robot.path = result[0]
                            cost = result[1]
                            print("Custo do Caminho:",cost)

                        robot.change_state(2)
                        return cost
    
    # se chegou aqui é pq não achou nada, logo faz um movimento aleatório
    random_move(robot, possible_moves, simulationMap)

def state_find_path(robot, targetPos, possible_moves, simulationMap):
    result = AStar(robot.position, targetPos, possible_moves, simulationMap)

    if result != None:
        path, cost = result
    else:
        return None

    return (path, cost)

def state_fetch(robot, simulationMap, listItems, listFactories):
    if not isinstance(robot.path, list) or robot.path == []:
        robot.change_state(0)
        return

    Render.draw_path(robot)
    Render.pygame.display.update()

    new_pos = robot.path.pop(0)

    i = 0
    while i < 4_000_000:
        i += 1

    robot.move_to(new_pos)

    if robot.path == []:
        robot.path = None
        cell = simulationMap[new_pos[0]][new_pos[1]]
        if cell.contents in listFactories:
            factory = listFactories.index(cell.contents)
            factory.deliver()
            robot.drop()
            robot.change_state(0)
        else:
            del listItems[listItems.index(cell.contents)]
            robot.pick_up(cell)
            robot.change_state(0)

def random_move(robot, possible_moves, simulationMap):
    posX, posY = robot.position
    candidates = []

    for i,j in possible_moves:
        x, y = posX+i, posY+j

        if not is_valid((x,y)):
            continue
        candidates.append((x,y))
    
    # escolhendo um movimento
    move = choice(candidates)
    while move == robot.pastPos or move == robot.position:
        move = choice(candidates)
    
    i = 0
    while i < 1_000_000:
        i += 1

    robot.move_to(move)

def distancia(pos1, pos2): # distância de Manhattan
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

def AStar(startingPos:tuple, target:tuple, possible_moves:list, simulationMap):
    # implementação do A*
    # Dada duas células quaisquer, calcula o caminho de menor custo entre elas, se ele existir
    # TODO: Melhorar esse A*, ele de fato não calcula o caminho de menor custo entre duas células quaisquer

    fronteira = PriorityQueue(startingPos, 0) # fila de células que o robô vai checar e custo para chegar lá
    caminho = dict() # dict de célula p/ células, caminho[(x,y)] = (x1,y1) ==> melhor caminho para (x,y) é de (x1,y1)
    caminho[startingPos] = None # não há caminho para a célula inicial
    custos = dict() # custo p/ chegar em celulas, custos[(x,y)] = n ==> custo para chegar em (x,y) é n
    custos[startingPos] = 0

    # testa_limite = lambda n, p : p - robot.radius < n < p + robot.radius
    while fronteira.len() > 0:

        i = 0 # artificalmente atrasando o algoritmo para ficar mais visivel
        while i < 2_000_000:
            i += 1

        Render.draw_border(fronteira.to_list())
        Render.pygame.display.update()
        _, posicao_atual = fronteira.pop()

        if posicao_atual == target:
            # se achou o alvo, sai do loop e retornar uma tupla contendo o path e o custo total desse path
            return (rebuildPath(caminho, target, startingPos), custos[posicao_atual] + simulationMap[target[0]][target[1]].cost)

        vizinhos = []
        for i in possible_moves: # gerando todos os vizinhos do nó atual
            v = posicao_atual[0]+i[0],posicao_atual[1]+i[1]
            if not is_valid(v):
                continue
            if not simulationMap[v[0]][v[1]].is_obstacle():
                vizinhos.append(v) # não insere vizinhos mais distantes que 4 células ou vizinhos que são obstáculos
        
        for vizinho in vizinhos:
            novo_custo = custos[posicao_atual] + simulationMap[vizinho[0]][vizinho[1]].cost
            swap = False

            if vizinho in custos: 
                # não posso deixar a condição do if da linha de baixo no if vizinhos not in custos
                # pois isso pode causar um KeyError caso vizinho de fato não esteja em custos
                # pelo mesmo motivo, não posso juntar esses dois if's num só
                if novo_custo < custos[vizinho]: 
                    swap = True

            if vizinho not in custos or swap:
                custos[vizinho] = novo_custo
                fronteira.push((novo_custo + distancia(target, vizinho)), vizinho)
                caminho[vizinho] = posicao_atual

    return None

def rebuildPath(path, orig, dest):   
    # começando pela célula onde o A* terminou, reconstrói o caminho do robo no mapa
    target = path[orig]
    i, j = target
    finalPath = [orig,target]

    if orig == target:
        return finalPath

    noPath = False
    while path[(i,j)] != dest: # TODO: Limpar essa bagunça
        finalPath.append(path[(i,j)])
        if path[(i,j)] == None:
            # print(orig, dest)
            # for p in path:
            #     print(p,"->",path[p])
            # for f in finalPath:
            #     print(f)
            # input()
            noPath = True
        if noPath:
            break
        i, j = path[(i,j)]

    finalPath.append(dest)

    finalPath.reverse()

    finalPath = [x for x in finalPath if x != None]

    return finalPath
