import Classes

from random import randint
from contextlib import redirect_stdout

def load_map() -> list:
    """
    Lê um arquivo com 42 linhas, cada uma com 42 caracteres que são as células do mapa
    Processa essas linhas e retorna o mapa
    """

    simulationMap = []
    try:
        with open("inputs/mapa.txt") as f:
            for line in f:
                cell = list(tuple(map(Classes.Celula, (map(int, line.replace("\t"," ").rstrip('\n').split(" "))))))
                simulationMap.append(cell)

        for i in range(42):
            for j in range(42):
                simulationMap[i][j].position = (i,j)
    except OSError:
        return None
    return simulationMap

def load_robot() -> tuple:
    """
    Lê um arquivo que contém 2 valores, que são a posição inicial do robô
    Retorna a posição lida
    """
    try:
        with open("inputs/robo.txt") as f:
            pos = tuple(map(int, (f.readline().rstrip('\n')).split(" ")))
            return pos
    except OSError:
        return None

def dump_robot(robotPosition:tuple) -> None:
    """
    Escreve as coordenadas x,y do robot no arquivo inputs/robo.txt
    Separadas por espaço, sem vírgula
    """
    with open("inputs/robo.txt",'w') as f:
        with redirect_stdout(f):
            print(str(robotPosition).replace("(","").replace(")","").replace(",",""))

def load_factories() -> dict:
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
                if line == "\n": continue
                line = list(map(int, (line.rstrip('\n').replace(" ","")).split(",")))
                factories[line[0]] = (line[1],line[2])
            return factories
    except OSError:
        return None

def dump_factories(factoryPositions:list) -> None:
    """
    Escreve em um arquivo o tipo de uma fábrica e sua posição no formato
        tipo, x, y
    """
    with open("inputs/fabrica.txt",'w') as f:
        with redirect_stdout(f):
            for fItems in factoryPositions:
                print(str(fItems[0]) + ", " + str(fItems[1]).replace("(","").replace(")",""))

def load_items() -> list:
    """
    Lê um arquivo que contém várias linhas seguindo o formato
        tipo, x, y
    Define que o item de tipo 'tipo' estará nas coordenadas (x,y)
    Retorna um dict que associa ints a lista de tuplas da forma: tipo: [(x1,y1),(x2,y2),...]
    """
    try:
        with open("inputs/items.txt") as f:
            items = {}
            temp_list = []
            for line in f:
                if line == "\n": continue
                line = list(map(int, (line.rstrip('\n').replace(" ","")).split(",")))
                if line[0] in items:
                    temp_list.append((line[1],line[2]))
                    items[line[0]] = temp_list
                else:
                    temp_list = [(line[1],line[2])]
                    items[line[0]] = temp_list
            return items
    except OSError:
        return None

def dump_items(itemPositions:list) -> None:
    """
    Escreve em um arquivo o tipo de um item e sua posição no formato
        tipo, x, y
    """
    with open("inputs/items.txt",'w') as f:
        with redirect_stdout(f):
            for fItems in itemPositions:
                print(str(fItems[0]) + ", " + str(fItems[1]).replace("(","").replace(")",""))

def generate_factories(simulationMap:list, ignore:dict=None, robotPos=None) -> list:
    """
    Gera fábricas e dispões elas aleatóriamente pelo mapa
    Opcionalmente recebe um dict de de fábricas que não precisam de posição aleatória
        pois sua posição foi definida anteriormente
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
        if condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
            while condition(posX,posY):
                posX,posY = (randint(0, 41), randint(0, 41))

    fabricaGraos = Classes.Fabrica(0, (posX,posY), 8, 0)
    fabricaGraos.set_request(8, 0)
    simulationMap[posX][posY].place(fabricaGraos)
    factoryList.append(fabricaGraos)

    if not 1 in ignore:
        posX,posY = (randint(0, 41), randint(0, 41))
        while condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
    else:
        posX,posY = ignore[1]
        if condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
            while condition(posX,posY):
                posX,posY = (randint(0, 41), randint(0, 41))

    fabricaBarcos = Classes.Fabrica(1, (posX,posY), 5, 1)
    fabricaBarcos.set_request(5, 1)
    simulationMap[posX][posY].place(fabricaBarcos)
    factoryList.append(fabricaBarcos)

    if not 2 in ignore:
        posX,posY = (randint(0, 41), randint(0, 41))
        while condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
    else:
        posX,posY = ignore[2]
        if condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
            while condition(posX,posY):
                posX,posY = (randint(0, 41), randint(0, 41))

    fabricaPetrobras = Classes.Fabrica(2, (posX,posY), 2, 2)
    fabricaPetrobras.set_request(2, 2)
    simulationMap[posX][posY].place(fabricaPetrobras)
    factoryList.append(fabricaPetrobras)

    if not 3 in ignore:
        posX,posY = (randint(0, 41), randint(0, 41))
        while condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
    else:
        posX,posY = ignore[3]
        if condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
            while condition(posX,posY):
                posX,posY = (randint(0, 41), randint(0, 41))

    fabricaFundicao = Classes.Fabrica(3, (posX,posY), 5, 3)
    fabricaFundicao.set_request(5, 3)
    simulationMap[posX][posY].place(fabricaFundicao)
    factoryList.append(fabricaFundicao)

    if not 4 in ignore:
        posX,posY = (randint(0, 41), randint(0, 41))
        while condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
    else:
        posX,posY = ignore[4]
        if condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
            while condition(posX,posY):
                posX,posY = (randint(0, 41), randint(0, 41))

    fabricaVigas = Classes.Fabrica(4, (posX,posY), 2, 4)
    fabricaVigas.set_request(2, 4)
    simulationMap[posX][posY].place(fabricaVigas)
    factoryList.append(fabricaVigas)

    return factoryList

def generate_items(simulationMap:list, ignore:dict=None, robotPos=None) -> list:
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

    if ignore != None: # se eu tenho items já carregados
        for i in ignore[0]:
            posX, posY = i
            itemBateria = Classes.Item(0, (posX, posY))
            simulationMap[posX][posY].place(itemBateria)
            itemList.append(itemBateria)

        for i in ignore[1]:
            posX, posY = i
            itemBraco = Classes.Item(1, (posX, posY))
            simulationMap[posX][posY].place(itemBraco)
            itemList.append(itemBraco)

        for i in ignore[2]:
            posX, posY = i
            itemBomba = Classes.Item(2, (posX, posY))
            simulationMap[posX][posY].place(itemBomba)
            itemList.append(itemBomba)

        for i in ignore[3]:
            posX, posY = i
            itemRefrigeracao = Classes.Item(3, (posX, posY))
            simulationMap[posX][posY].place(itemRefrigeracao)
            itemList.append(itemRefrigeracao)

        for i in ignore[4]:
            posX, posY = i
            itemBracoPneumatico = Classes.Item(4, (posX, posY))
            simulationMap[posX][posY].place(itemBracoPneumatico)
            itemList.append(itemBracoPneumatico)
        
        return itemList

    else:

        for _ in range(20):
            posX, posY = (randint(0, 41), randint(0, 41))
            while condition(posX, posY):
                posX, posY = (randint(0, 41), randint(0, 41))
            itemBateria = Classes.Item(0, (posX, posY))
            simulationMap[posX][posY].place(itemBateria)
            itemList.append(itemBateria)

        for _ in range(10):
            posX, posY = (randint(0, 41), randint(0, 41))
            while condition(posX, posY):
                posX, posY = (randint(0, 41), randint(0, 41))
            itemBraco = Classes.Item(1, (posX, posY))
            simulationMap[posX][posY].place(itemBraco)
            itemList.append(itemBraco)
        
        for _ in range(8):
            posX, posY = (randint(0, 41), randint(0, 41))
            while condition(posX, posY):
                posX, posY = (randint(0, 41), randint(0, 41))
            itemBomba = Classes.Item(2, (posX, posY))
            simulationMap[posX][posY].place(itemBomba)
            itemList.append(itemBomba)

        for _ in range(6):
            posX, posY = (randint(0, 41), randint(0, 41))
            while condition(posX, posY):
                posX, posY = (randint(0, 41), randint(0, 41))
            itemRefrigeracao = Classes.Item(3, (posX, posY))
            simulationMap[posX][posY].place(itemRefrigeracao)
            itemList.append(itemRefrigeracao)

        for _ in range(4):
            posX, posY = (randint(0, 41), randint(0, 41))
            while condition(posX, posY):
                posX, posY = (randint(0, 41), randint(0, 41))
            itemBracoPneumatico = Classes.Item(4, (posX, posY))
            simulationMap[posX][posY].place(itemBracoPneumatico)
            itemList.append(itemBracoPneumatico)

    return itemList

def generate_robot():
    """
    Gera o robô para a simulação
    Retorna o robô, numa posição gerada aleatóriamente
    """
    posX,posY = load_robot()
    return Classes.Robo((posX,posY))

def write_result(filename:str, cost:int, expanded:int, moves:int):
    with open(f"outputs/{filename}.txt",'w') as f:
        with redirect_stdout(f):
            print(f"Cost={cost}, Expanded={expanded}, RandomMoves={moves}")