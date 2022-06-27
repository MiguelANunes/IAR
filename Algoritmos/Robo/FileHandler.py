import Render
from Classes import *

import pygame
from pygame.locals import *
from random import randint

def get_keys() -> int:
    """
    Usa funções do pygame para verificar as setas foram apertadas
    Retorno:
        1 = esquerda
        2 = direita
        3 = cima
        4 = baixo
        5 = enter
        6 = espaço
        0 = nenhuma
    Esc mata o programa
    """

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return 1
            elif event.key == pygame.K_RIGHT:
                return 2
            elif event.key == pygame.K_UP:
                return 3
            elif event.key == pygame.K_DOWN:
                return 4
            elif event.key == pygame.K_RETURN:
                return 5
            elif event.key == pygame.K_SPACE:
                return 6
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    return 0

def pretty_placer(simulationMap:list) -> list:

    print("Aperte as setas do teclado para mover o cursor")
    print("Aperte enter para confirmar a posição do cursor")
    print("Aperte espaço para sair")

    returnList = []
    posX = 0
    posY = 0
    possibleX = [(0, y) for y in range(42)]
    possibleY = [(x, 0) for x in range(42)]
    Render.draw(simulationMap, [], [])
    Render.draw_colored_border(possibleX, (255,0,0))
    Render.draw_colored_border(possibleY, (255,0,0))
    Render.pygame.display.update()

    while True:

        key = get_keys()
        if key in [1,2]:
            possibleX = []
            if key == 1:
                posX -= 1
            else:
                posX += 1
            for y in range(42):
                possibleX.append((posX, y))        
            Render.draw(simulationMap, [], [])
            Render.draw_colored_border(possibleX, (255,0,0))
            Render.draw_colored_border(possibleY, (255,0,0))
            Render.pygame.display.update()

        key = get_keys()
        if key in [3,4]:
            possibleY = []
            if key == 3:
                posY -= 1
            else:
                posY += 1
            for x in range(42):
                possibleY.append((x, posY))
            Render.draw(simulationMap, [], [])
            Render.draw_colored_border(possibleX, (255,0,0))
            Render.draw_colored_border(possibleY, (255,0,0))
            Render.pygame.display.update()
        
        key = get_keys()
        if key == 5:
            print(f"Li a posição ({posX},{posY})")
            returnList.append((posX, posY))
        
        if key == 6:
            return returnList

def load_map():
    """
    Lê um arquivo com 42 linhas, cada uma com 42 caracteres que são as células do mapa
    Processa essas linhas e retorna o mapa
    """

    simulationMap = []
    try:
        with open("inputs/mapa.txt") as f:
            for line in f:
                cell = list(tuple(map(Celula, (map(int, line.replace("\t"," ").rstrip('\n').split(" "))))))
                simulationMap.append(cell)

        for i in range(42):
            for j in range(42):
                # definindo as posições das células, usando no A*
                simulationMap[i][j].position = (i,j)
    except OSError:
        print("Erro ao carregar o mapa\nNão consegui achar ou abrir o arquivo mapa.txt na pasta inputs")
        exit()
    return simulationMap

def load_robot():
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

def load_obstacles() -> list:
    """
    Lê um arquivo que contém várias linhas seguindo o formato
        x, y
    Define que há um obstaculo no ponto (x,y)
    Retona uma lista de tuplas (x,y)
    """
    try:
        with open("inputs/obstaculo.txt") as f:
            obstacles = []
            for line in f:
                line = tuple(map(int, line.rstrip('\n').split(" ")))
                obstacles.append(line)
            return obstacles
    except OSError:
        return None

def get_all_but_one(myDicts:dict, ignore:list) -> dict:
    """
    Essa função era útil no passado, mas agora não é mais
    Ainda assim, vai ficar aqui, pois pode ser útil no futuro

    myDicts é um dict de dicts
    as chaves de myDicts são tuplas

    os valores de myDicts[chave1] são dicts
    as chaves de  myDicts[chave1] são tuplas

    os valores de myDicts[chave1][chave2] são ints

    quero garantir que myDicts[key].get vai retornar um dict de dicts
    onde myDicts[<chave>] irá retornar um dict que não tem uma chave que está em ignore
    """

    outerDict = dict()
    #   || dict     || dict de dicts
    #   \/          \/
    for outerKey in myDicts:
        innerDict = dict()
            # || tupla   || dict
            # \/         \/      
        for innerKey in myDicts[outerKey]:
            if innerKey in ignore: continue
            #     /\         /\
            #     || tupla   || lista de tuplas

            #           || tupla    || int
            #           \/          \/
            innerDict[innerKey] = myDicts[outerKey][innerKey]
        outerDict[outerKey] = innerDict
        # /\         /\        /\
        # ||         || dict   || dict
        # || dict de dicts
    
    return outerDict

def generate_factories(simulationMap:list, robotPos:tuple, ignore:dict=None) -> list:
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

    fabricaGraos = Fabrica(0, (posX,posY), 8, 0)
    fabricaGraos.set_request(8, 0)
    simulationMap[posX][posY].place(fabricaGraos)
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

    # Condição para uma possível posição ser descartada
    # Já tem algo naquela célula
    # Ou a célula tem um obstáculo
    condition = lambda x, y: simulationMap[x][y].contents != None or simulationMap[x][y].is_obstacle()

    if position == None:
        posX,posY = (randint(0, 41), randint(0, 41))
        while condition(posX,posY):
            posX,posY = (randint(0, 41), randint(0, 41))
    else:
        posX,posY = position

        if simulationMap[posX][posY].contents != None or simulationMap[posX][posY].cost == -1:
            print("A posição fornecida para o robô é inválida!")
            print("Gerando uma posição aleatória...")

            posX,posY = (randint(0, 41), randint(0, 41))
            while condition(posX,posY):
                posX,posY = (randint(0, 41), randint(0, 41))

            print("Robô será colocado em",(posX,posY))

    return Robo((posX,posY))

def generate_obstacles(simulationMap:list, file:bool) -> None:
    """
    Insere obstáculo no mapa pedindo para o usário dar as coordenadas x,y do obstáculo
    Após cada inserção, pede para o usuário confirmar que está correto
    Desenha no mapa linhas referentes a células que tem x ou y igual ao valor fornecido
    Repete esse processo quantas vezes o usuário quiser
    Não retorna nada, altera o mapa durante a execução da função
    """
    # TODO: Generalizar isso pra poder usar em todas as funções de inserir alguma coisa (robo, fábrica) no mapa 
    while True and not file:

        confirm = False

        Render.draw(simulationMap, [], [])
        Render.pygame.display.update()

        while not confirm:
            Render.draw(simulationMap, [], [])
            Render.pygame.display.update()

            possibleX = []
            posX = int(input("Digite a coordenada X de onde quer inserir/remover o obstáculo: "))
            for y in range(42):
                possibleX.append((posX, y))        

            Render.draw_colored_border(possibleX, (255,0,0))
            Render.pygame.display.update()
            
            choice = input("Essa posição está correta? (y/n) ")
            if choice.casefold() == 'y'.casefold() or choice.casefold() == 's'.casefold():
                confirm = True
        
        confirm = False

        while not confirm:
            Render.draw(simulationMap, [], [])
            Render.draw_colored_border(possibleX, (255,0,0))
            Render.pygame.display.update()

            possibleY = []
            posY = int(input("Digite a coordenada Y de onde quer inserir/remover o obstáculo: "))
            for x in range(42):
                possibleY.append((x, posY))
            
            Render.draw_colored_border(possibleY, (255,0,0))
            Render.pygame.display.update()

            choice = input("Essa posição está correta? (y/n) ")
            if choice.casefold() == 'y'.casefold() or choice.casefold() == 's'.casefold():
                confirm = True

        if not simulationMap[posX][posY].is_obstacle():
            simulationMap[posX][posY].set_obstacle()
        else: # ao remover obstáculo, célula se torna grama, independente doq era antes
            simulationMap[posX][posY] = Celula(0, (posX,posY))

        Render.draw(simulationMap, [], [])
        Render.pygame.display.update()

        choice = input("Adicionar mais um obstáculo? (y/n) ")
        if choice.casefold() == 'y'.casefold() or choice.casefold() == 's'.casefold():
            continue
        else:
            return