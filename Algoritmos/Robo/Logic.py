from random import choice, randint

import Render, Main
from Classes import *

# TODO: Mudar um pouco como é feita a ordem de operações do robô
#       Pelo que eu entendi o robô inicialmente sabe onde estão todas as fábricas e oq querem
#       e anda pelo mapa procurando os itens
#       Quando acha algo que uma fábrica quer, vai até ela e entrega o item para ela

# TODO: Sobre condição de parada do programa
#       Colocar uma lista de fábricas no robô
#       Toda vez que uma fábrica tem sua request satisfeita, ela é removida da lista
#       Programa para quando a lista estiver vazia

# TODO: Printar no terminal que item o robo pegou/para qual fabrica entregou quando o fizer

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
    Retorna um dict da forma tipo: (x, y)
    """
    try:
        with open("inputs/fabrica.txt") as f:
            factories = {}
            for line in f:
                line = list(map(int, (line.rstrip('\n').replace(" ","")).split(",")))
                factories[line[0]] = (line[1],line[2])
            return factories
    except OSError:
        return None

def generate_factories(simulationMap:list, robotPos:tuple, ignore:dict=None) -> list:
    """
    Gera fábricas e dispões elas aleatóriamente pelo mapa
    Opcionalmente recebe um dict de de fábricas que não precisam de posição aleatória
        pois sua posição foi definida num arquivo
    Receba a posição inicial do robô e não coloca nenhuma fábrica naquela célula
    Retorna uma lista contendo todas as fábricas
    """

    if ignore == None:
        ignore = {}

    factoryList = []

    # Condição para uma possível posição ser descartada
    # Já tem algo naquela célula
    # Ou a célula é um obstáculo
    # Ou o robô está lá
    condition = lambda x, y: simulationMap[x][y].contents != None or simulationMap[x][y].is_obstacle() or (x,y) == robotPos

    if not 0 in ignore:
        posX,posY = (randint(0, 41), randint(0, 41))
        while condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
    else:
        posX,posY = ignore[0]

    fabricaGraos = Fabrica(0, (posX,posY), 8, 0)
    fabricaGraos.set_request(8, 0)
    simulationMap[posX][posX].place(fabricaGraos)
    factoryList.append(fabricaGraos)

    if not 1 in ignore:
        posX,posY = (randint(0, 41), randint(0, 41))
        while condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
    else:
        posX,posY = ignore[1]

    fabricaBarcos = Fabrica(1, (posX,posY), 5, 1)
    fabricaBarcos.set_request(5, 1)
    simulationMap[posX][posY].place(fabricaBarcos)
    factoryList.append(fabricaBarcos)

    if not 2 in ignore:
        posX,posY = (randint(0, 41), randint(0, 41))
        while condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
    else:
        posX,posY = ignore[2]

    fabricaPetrobras = Fabrica(2, (posX,posY), 2, 2)
    fabricaPetrobras.set_request(2, 2)
    simulationMap[posX][posY].place(fabricaPetrobras)
    factoryList.append(fabricaPetrobras)

    if not 3 in ignore:
        posX,posY = (randint(0, 41), randint(0, 41))
        while condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
    else:
        posX,posY = ignore[3]

    fabricaFundicao = Fabrica(3, (posX,posY), 5, 3)
    fabricaFundicao.set_request(5, 3)
    simulationMap[posX][posY].place(fabricaFundicao)
    factoryList.append(fabricaFundicao)

    if not 4 in ignore:
        posX,posY = (randint(0, 41), randint(0, 41))
        while condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
    else:
        posX,posY = ignore[4]

    fabricaVigas = Fabrica(4, (posX,posY), 2, 4)
    fabricaVigas.set_request(2, 4)
    simulationMap[posX][posY].place(fabricaVigas)
    factoryList.append(fabricaVigas)

    return factoryList

def generate_items(simulationMap:list, robotPos:tuple):
    """
    Gera os itens para a simulação
    Dado o mapa e a posição do robô, insere os itens pedidos na descrição do trabalho 
        apenas em células de grama que não estão ocupadas pelo robô e que já não tem algo nelas
    Retorna uma lista contendo todos os itens
    """

    itemList = []

    # Condição para uma possível posição ser descartada
    # Ou a célula do mapa naquela posição não é de grama
    # Ou já tem algo naquela célula
    # Ou o robô está lá
    condition = lambda x, y: simulationMap[x][y].tipo != 0 or simulationMap[x][y].contents != None or (x,y) == robotPos

    for _ in range(20):
        posX, posY = (randint(0, 41), randint(0, 41))
        while condition(posX, posY):
            posX, posY = (randint(0, 41), randint(0, 41))
        itemBateria = Item(0, (posX, posY))
        simulationMap[posX][posY].place(itemBateria)
        itemList.append(itemBateria)

    for _ in range(10):
        posX, posY = (randint(0, 41), randint(0, 41))
        while condition(posX, posY):
            posX, posY = (randint(0, 41), randint(0, 41))
        itemBraco = Item(1, (posX, posY))
        simulationMap[posX][posY].place(itemBraco)
        itemList.append(itemBraco)
    
    for _ in range(8):
        posX, posY = (randint(0, 41), randint(0, 41))
        while condition(posX, posY):
            posX, posY = (randint(0, 41), randint(0, 41))
        itemBomba = Item(2, (posX, posY))
        simulationMap[posX][posY].place(itemBomba)
        itemList.append(itemBomba)

    for _ in range(6):
        posX, posY = (randint(0, 41), randint(0, 41))
        while condition(posX, posY):
            posX, posY = (randint(0, 41), randint(0, 41))
        itemRefrigeracao = Item(3, (posX, posY))
        simulationMap[posX][posY].place(itemRefrigeracao)
        itemList.append(itemRefrigeracao)

    for _ in range(4):
        posX, posY = (randint(0, 41), randint(0, 41))
        while condition(posX, posY):
            posX, posY = (randint(0, 41), randint(0, 41))
        itemBracoPneumatico = Item(4, (posX, posY))
        simulationMap[posX][posY].place(itemBracoPneumatico)
        itemList.append(itemBracoPneumatico)

    return itemList

def generate_robot(simulationMap:list, position:tuple=None):
    """
    Gera o robô para a simulação
    Caso uma posição inicial seja fornecida, verifica se ela é válida
    Se não for, ou se nenhuma for fornecida, gera uma posição aleatória
    Retorna o robô, na posição gerada ou fornecida
    """

    if position == None:
        posX,posY = (randint(0, 41), randint(0, 41))
        while simulationMap[posX][posY].contents != None or simulationMap[posX][posY].cost == -1:
            posX,posY = (randint(0, 41), randint(0, 41))
    else:
        posX,posY = position

        if simulationMap[posX][posY].contents != None or simulationMap[posX][posY].cost == -1:
            print("A posição fornecida para o robô é inválida!")
            print("Gerando uma posição aleatória...")

            posX,posY = (randint(0, 41), randint(0, 41))
            while simulationMap[posX][posY].contents != None or simulationMap[posX][posY].cost == -1:
                posX,posY = (randint(0, 41), randint(0, 41))

            print("Robô será colocado em",(posX,posY))

    return Robo((posX,posY))

def is_valid(pos:tuple):
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
                        try:
                            print("Achou um(a)", item.name)
                            print("Custo do Caminho:",cost)
                        except IndexError:
                            print(robot.contents)
                            input()
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

    pause = False

    while fronteira.len() > 0:

        if not pause:
            pause = Main.check_pause()
        else:
            pause = Main.check_resume()

        if pause:
            continue

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
