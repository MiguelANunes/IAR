import sys
from random import randint, choice
from typing import Type
import Render

# from Main import DISPLAY

# TODO: Mudar um pouco como é feita a ordem de operações do robô
#       Pelo que eu entendi o robô inicialmente sabe onde estão todas as fábricas e oq querem
#       e anda pelo mapa procurando os itens
#       Quando acha algo que uma fábrica quer, vai até ela e entrega o item para ela


class Item:
    # Tipos de itens:
    # 0: Bateria de carga elétrica;
    # 1: Braço de solda;
    # 2: Bomba de sucção;
    # 3: Dispositivo de refrigeração;
    # 4: Braço pneumático.
    def __init__(self, tipo, pos):
        self.tipo     = tipo
        self.position = pos
    
        if self.tipo == 0:
            self.cor = (32,32,32)

        elif self.tipo == 1:
            self.cor = (200,0,0)

        elif self.tipo == 2:
            self.cor = (240,0,200)

        elif self.tipo == 3:
            self.cor = (0,0,200)
        
        else:
            self.cor = (200,200,0)
    
    def __str__(self) -> str:
        return ">"+str(self.tipo)+" "+str(self.position)+"<"

class Celula:

    # Tipos de Células
    # 0: Plano      (Verde)
    # 1: Montanhoso (Marrom)
    # 2: Pântano    (Azul)
    # 3: Árido      (Vermelho)
    # _: Obstáculo  (Preto)

    def __init__(self, tipo, position=None, contents=None):
        self.tipo     = tipo
        self.contents = contents
        self.position = position

        if self.tipo == 0:
            self.cost = 1
            self.cor  = (0, 128, 0)

        elif self.tipo == 1:
            self.cost = 5
            self.cor  = (96, 48, 12)

        elif self.tipo == 2:
            self.cost = 10
            self.cor  = (0, 0, 128)

        elif self.tipo == 3:
            self.cost = 15
            self.cor  = (128, 0, 0)
        
        else:
            self.cost = -1
            self.cor  = (0, 0, 0)

    def place(self, obj):
        self.contents = obj

    def is_obstacle(self):
        return self.cost == -1

    def remove(self):
        self.contents = None

    def __str__(self) -> str:
        c = f" {self.contents}" if self.contents != None else ""
        return f"{self.tipo}{c}"

class Fabrica:

    # Tipos de industrias e suas necessidades
    # 0: Indústria de melhoramento genético de grãos    | Necessita de 8 baterias
    # 1: Empresa de manutenção de cascos de embarcações | Necessita de 5 braços de solda
    # 2: Indústria petrolífera                          | Necessita de 2 bombas
    # 3: Fábrica de fundição                            | Necessita de 5 refrigeradores
    # 4: Indústria de vigas de aço                      | Necessita de 2 braços pneumáticos

    def __init__(self, tipo, pos, qtd=None, obj=None):
        self.tipo    = tipo
        self.position     = pos
        self.request = (qtd, obj) # request será uma tupla (int, int), segundo int é o tipo do item

        if self.tipo == 0:
            self.cor = (198,0,198)

        elif self.tipo == 1:
            self.cor = (198,198,0)

        elif self.tipo == 2:
            self.cor = (0,198,198)

        elif self.tipo == 3:
            self.cor = (198,0,64)
        
        else:
            self.cor = (0, 198, 78)

    def set_request(self, qtd: int, obj: int):
        self.request = (qtd, obj)

    def deliver(self):
        result = self.request[0]-1
        if result > 0:
            self.request = (result, self.request[1])
        else:
            self.request = (-1,-1)
            # TODO: Tratar o caso em que a request é None

class Robo:
    
    # TODO: Salvar no robô as informações das fábricas

    # position => posição atual do robô
    # pastPos => ultima posição do robô
    # target => onde o robô quer chegar
    # lookingAt => célula que o robô está olhando enquanto executa o A*, usado para representar a decisão dele
    # path => caminho que o robô calculou com o A*
    # contents => o que o robô está carregando, lista de ints, cada int é um tipo de item
    # radius => raio de visão do robô

    # estado:
    #   0: movendo aleatóriamente, procurando por algo (0 -> 1, 0 -> 2)
    #   1: calculando path pra algum objeto (1 -> 0)
    #   2: path calculado, seguindo ele até o objeto (2 -> 0)
    def __init__(self, pos):
        self.position  = pos
        self.pastPos   = (-1,-1)
        self.path      = None
        self.contents  = []
        self.state     = 0
        self.radius    = 4

    def pick_up(self, cell: Celula):
        # retorna True se pegou um item

        if cell.contents in self.contents:
            return False
        else:
            self.contents.append(cell.contents)
            cell.remove()
            return True

    def move_to(self, newPos):
        self.pastPos  = self.position
        self.position = newPos

    def change_state(self, newState):
        self.state = newState
    
    def drop(self, item):
        del self.contents[self.contents.index(item)]

class PriorityQueue:
    # uma implementação boba porém simples de fila de prioridade minima
    def __init__(self, startcell=None, startWeight=None):
        weight    = startWeight if startWeight != None else -1
        temp_cell = startcell if startcell != None else (-1,-1)

        if is_valid(temp_cell) and weight >= 0:
            self.queue = [(weight, temp_cell)]
        else:
            self.queue = []

    def __str__(self) -> str:
        return str(self.queue)

    def to_list(self) -> list:
        returnList = []
        for q in self.queue:
            returnList.append(q[1])
        return returnList

    def push(self, weight, cell):
        self.queue.append((weight, cell))

    def len(self):
        return len(self.queue)

    def pop(self):
        try:
            minCost = 0
            for i in range(len(self.queue)):
                if self.queue[i][0] <= self.queue[minCost][0]:
                    minCost = i
            result = self.queue[minCost] # retorna o par (custo, célula)
            del self.queue[minCost]
            return result

        except IndexError:
            sys.stderr.write("Erro, tentando dar pop em fila vazia")
            sys.exit()

def load_map():
    simulationMap = []
    with open(f"inputs/input.txt") as f:
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

def generate_factories(simulationMap):

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
        while simulationMap[pos[0]][pos[1]].tipo != 0 and simulationMap[pos[0]][pos[1]].contents != None:
            pos = (randint(0, 41), randint(0, 41))
        itemBateria = Item(0, pos)
        simulationMap[pos[0]][pos[1]].place(itemBateria)
        itemList.append(itemBateria)

    for _ in range(10):
        pos = (randint(0, 41), randint(0, 41))
        while simulationMap[pos[0]][pos[1]].tipo != 0 and simulationMap[pos[0]][pos[1]].contents != None:
            pos = (randint(0, 41), randint(0, 41))
        itemBraco = Item(1, pos)
        simulationMap[pos[0]][pos[1]].place(itemBraco)
        itemList.append(itemBraco)
    
    for _ in range(8):
        pos = (randint(0, 41), randint(0, 41))
        while simulationMap[pos[0]][pos[1]].tipo != 0 and simulationMap[pos[0]][pos[1]].contents != None:
            pos = (randint(0, 41), randint(0, 41))
        itemBomba = Item(2, pos)
        simulationMap[pos[0]][pos[1]].place(itemBomba)
        itemList.append(itemBomba)

    for _ in range(6):
        pos = (randint(0, 41), randint(0, 41))
        while simulationMap[pos[0]][pos[1]].tipo != 0 and simulationMap[pos[0]][pos[1]].contents != None:
            pos = (randint(0, 41), randint(0, 41))
        itemRefrigeracao = Item(3, pos)
        simulationMap[pos[0]][pos[1]].place(itemRefrigeracao)
        itemList.append(itemRefrigeracao)

    for _ in range(4):
        pos = (randint(0, 41), randint(0, 41))
        while simulationMap[pos[0]][pos[1]].tipo != 0 and simulationMap[pos[0]][pos[1]].contents != None:
            pos = (randint(0, 41), randint(0, 41))
        itemBracoPneumatico = Item(4, pos)
        simulationMap[pos[0]][pos[1]].place(itemBracoPneumatico)
        itemList.append(itemBracoPneumatico)

    return itemList

def is_valid(pos):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < 42 and pos[1] < 42

# procura por itens que ainda não tem
# move aleatóriamente até achar algo
# tendo algo, continua movendo aleatório
# se achar uma fábrica que precisa de algo e tem, entrega
# se todas as fábricas estiverem satisfeitas, termina simulação

def state_search(robot, possible_moves, simulationMap, listItems, listFactories):
    # procura por algo, se não acha nada faz um movimento aleatório

    # TODO: Mudar maneira que lido com a busca de itens,
    # Colocar todos numa lista e então fazer 

    posX, posY = robot.position
    raio = robot.radius

    for i in range(-raio, raio+1):
        for j in range(-raio, raio+1):
            x, y = posX+i, posY+j
            
            if not is_valid((x,y)):
                continue

            if simulationMap[x][y].is_obstacle():
                # ignora os obstaculos
                continue
            
            if simulationMap[x][y].contents != None:
                # se achou alguma coisa no mapa
                item = simulationMap[x][y].contents

                if item in listItems and not item in robot.contents:
                    # se achou um item que não está carregando, vai buscar ele
                    robot.change_state(1)
                    pathCost = state_find_path(robot, (x,y), possible_moves, simulationMap)
                    robot.change_state(2)
                    return pathCost
                    # continue
                
                if item in listFactories:
                    # se achou uma fábrica, testa para ver se tem o item que quer
                    if item.request[0] > 0 and item.request[1] in robot.contents:
                        # se tem o que quer, vai entregar
                        # robot.change_state(1)
                        # robot.path = state_find_path(robot, (x,y), simulationMap, listItems, listFactories)
                        # robot.change_state(2)
                        # return
                        continue
    
    # se chegou aqui é pq não achou nada, logo faz um movimento aleatório
    random_move(robot, possible_moves, simulationMap)

def state_find_path(robot, targetPos, possible_moves, simulationMap):
    result = AStar(robot.position, targetPos, possible_moves, simulationMap)

    if result != None:
        path, cost = result
    else:
        return None

    robot.path = path
    return cost

def state_fetch(robot, simulationMap, listItems, listFactories):
    if not isinstance(robot.path, list) or robot.path == []:
        robot.change_state(0)
        return

    Render.draw_path(robot)
    Render.pygame.display.update()

    new_pos = robot.path.pop(0)

    i = 0
    while i < 5_000_000:
        i += 1

    robot.move_to(new_pos)

    if robot.path == []:
        robot.path = None
        cell = simulationMap[new_pos[0]][new_pos[1]]
        if cell.contents in listFactories: # se achou uma fábrica
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
    while i < 2_000_000:
        i += 1

    robot.move_to(move)

# fazer funções para desenhar as células que estão sendo avaliadas 
# e chamar elas de dentro desta função

def distancia(pos1, pos2): # distância de Manhattan
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

def AStar(startingPos:tuple, target:tuple, possible_moves:list, simulationMap):
    # implementação do A*
    # Dada duas células quaisquer, calcula o caminho de menor custo entre elas, se ele existir

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
            # testa_limite(v[0], inicialX) and testa_limite(v[1], inicialY) and
            if not simulationMap[v[0]][v[1]].is_obstacle():
                vizinhos.append(v) # não insere vizinhos mais distantes que 4 células ou vizinhos que são obstáculos
        
        for vizinho in vizinhos:

            # if ultimoVizinho != None:
            #     Render.erase_looking_at(ultimoVizinho)
            #     Render.pygame.display.update()

            # Render.draw_looking_at(vizinho)
            # Render.pygame.display.update()
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

    # caminho = dict() # dict de célula p/ células, caminho[(x,y)] = (x1,y1) ==> melhor caminho para (x,y) é de (x1,y1)
    # caminho[posicaoInicial] = None # não há caminho para a célula inicial

    target = path[orig]
    i, j = target
    finalPath = [orig,target]

    if orig == target:
        return finalPath

    while path[(i,j)] != dest:
        finalPath.append(path[(i,j)])
        if path[(i,j)] == None:
            continue
        i, j = path[(i,j)]
        # try: #Creio que isso foi arrumado
        #     i, j = path[(i,j)]
        # except TypeError:
        #     print(orig, dest)
        #     for p in path:
        #         print(p,"->",path[p])
        #     for f in finalPath:
        #         print(f)
        #     input()
    finalPath.append(dest)

    finalPath.reverse()

    return finalPath
    

# O robô tem a informação da posição das fábricas
# As ferramentas devem sempre estar em locais de grama