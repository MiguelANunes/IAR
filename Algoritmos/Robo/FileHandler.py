import Render, Classes

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

def pretty_placer(simulationMap:list, action=None, factories:list=None) -> list:
    """
    Dado o mapa da simulação, gera um cursor para selecionar posições no mapa
    Quando uma posição é selecionada, executa a função action, caso ela tenha sido passada
        action deve ser uma função que recebe uma tupla (x,y) e não retorna nada
    Factories é uma lista opcionalmente vazia de fábricas a serem renderizadas dentro dessa função
    Cas não, coloca todas as células selecionadas numa lista e retorna essa lista
    """

    print("**********")
    print("Aperte as setas do teclado para mover o cursor")
    print("Aperte enter para confirmar a posição do cursor")
    print("Aperte espaço para sair")
    print("**********")

    if factories == None:
        factories = []

    returnList = []
    posX = 0
    posY = 0
    possibleX = [(0, y) for y in range(42)]
    possibleY = [(x, 0) for x in range(42)]
    Render.draw(simulationMap, [], factories)
    Render.draw_colored_border(possibleX, (255,0,0))
    Render.draw_colored_border(possibleY, (255,0,0))
    Render.pygame.display.update()

    while True:

        key = get_keys()
        if key in [1,2]:
            possibleX = []
            if key == 1:
                posX = posX - 1 if posX != 0 else 41
            else:
                posX = posX + 1 if posX != 41 else 0
            for y in range(42):
                possibleX.append((posX, y))        
            Render.draw(simulationMap, [], factories)
            Render.draw_colored_border(possibleX, (255,0,0))
            Render.draw_colored_border(possibleY, (255,0,0))
            Render.pygame.display.update()

        key = get_keys()
        if key in [3,4]:
            possibleY = []
            if key == 3:
                posY = posY - 1 if posY != 0 else 41
            else:
                posY = posY + 1 if posY != 41 else 0
            for x in range(42):
                possibleY.append((x, posY))
            Render.draw(simulationMap, [], factories)
            Render.draw_colored_border(possibleX, (255,0,0))
            Render.draw_colored_border(possibleY, (255,0,0))
            Render.pygame.display.update()
        
        key = get_keys()
        if key == 5:
            if action != None:
                return action((posX,posY))
            print(f"Li a posição ({posX},{posY})")
            returnList.append((posX, posY))
        
        if key == 6:
            if action != None:
                return None
            return returnList

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
                # definindo as posições das células, usando no A*
                simulationMap[i][j].position = (i,j)
    except OSError:
        print("Erro ao carregar o mapa\nNão consegui achar ou abrir o arquivo mapa.txt na pasta inputs")
        exit()
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
        if condition(posX,posY):
            print(f"Posição {(posX,posY)} p/ fábrica Agro é Pop lida de arquivo ou fornecida é inválida!")
            print("Gerando uma nova posição aleatóriamente")
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
            print(f"Posição {(posX,posY)} p/ fábrica Blohm und Voß lida de arquivo ou fornecida é inválida!")
            print("Gerando uma nova posição aleatóriamente")
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
            print(f"Posição {(posX,posY)} p/ fábrica Petrobras lida de arquivo ou fornecida é inválida!")
            print("Gerando uma nova posição aleatóriamente")
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
            print(f"Posição {(posX,posY)} p/ fábrica Fundição Tupy lida de arquivo ou fornecida é inválida!")
            print("Gerando uma nova posição aleatóriamente")
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
            print(f"Posição {(posX,posY)} p/ fábrica Gerdau lida de arquivo ou fornecida é inválida!")
            print("Gerando uma nova posição aleatóriamente")
            posX,posY = (randint(0, 41), randint(0, 41))
            while condition(posX,posY):
                posX,posY = (randint(0, 41), randint(0, 41))

    fabricaVigas = Classes.Fabrica(4, (posX,posY), 2, 4)
    fabricaVigas.set_request(2, 4)
    simulationMap[posX][posY].place(fabricaVigas)
    factoryList.append(fabricaVigas)

    return factoryList

def generate_items(simulationMap:list, robotPos:tuple) -> list:
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

def generate_robot(simulationMap:list):
    """
    Gera o robô para a simulação
    Retorna o robô, numa posição gerada aleatóriamente
    """

    # Condição para uma possível posição ser descartada
    # Já tem algo naquela célula
    # Ou a célula tem um obstáculo
    condition = lambda x, y: simulationMap[x][y].contents != None or simulationMap[x][y].is_obstacle()

    posX,posY = (randint(0, 41), randint(0, 41))
    while condition(posX,posY):
        posX,posY = (randint(0, 41), randint(0, 41))

    return Classes.Robo((posX,posY))

def get_robot(simulationMap:list, file:bool, manual:bool):
    """
    Define a posição do robô no mapa, de acordo com input do usuário ou do que foi lido de um arquivo

    Não posso anotar tipo de retorno pois isso pode gerar conflito de modulos
    É complicado
    """

    if file:
        position = load_robot()
        return Classes.Robo(position)
    
    if manual:
        robot = Classes.Robo((-1,-1))
        confirm = False

        print("Escolhendo posição para o robo...\n")
        while not confirm:
            pretty_placer(simulationMap, robot.move_to)

            if robot.position == (-1,-1):
                print("Nenhuma posição foi escolhida")
                print("Lidar com esse edge case vai ser uma dor de cabeça, então não farei isso")
                print("Bye bye")
                exit()
            
            print("Robo foi colocado na posição", robot.position,"isso está certo? (y/n)",end=" ")
            choice = input()
            Render.draw(simulationMap, [], [], robot)
            Render.pygame.display.update()
            if choice.casefold() == 'y'.casefold() or choice.casefold() == 's'.casefold():
                confirm = True
            else:
                print("Escolhendo outra posição...")
        
        return robot

    if not file and not manual:
        return generate_robot(simulationMap)

def get_factories(simulationMap:list, file:bool, manual:bool, robotPos) -> list:
    """
    Define as posições das fábricas no mapa, de acordo com input do usuário ou do que foi lido de um arquivo
    """

    if file:
        return generate_factories(simulationMap, robotPos, load_factories())
    
    if manual:
        placed = []
        ignore = dict()
        for i in range(5):
        
            if i == 0:
                name = "Agro é Pop"
            elif i == 1:
                name = "Blohm und Voß"
            elif i == 2:
                name = "Petrobras"
            elif i == 3:
                name = "Fundição Tupy"
            elif i == 4: 
                name = "Gerdau"

            print(f"\nEscolhendo posição para a fábrica {name}...")
            print("Aperte espaço (dentro da janela do pygame) para pular essa fábrica\n")
            confirm = False

            while not confirm:
                ignore[i] = pretty_placer(simulationMap, lambda n: n, placed)
                if ignore[i] == None:
                    print(f"Pulando fábrica {name}...")
                    del ignore[i]
                    break
                
                # Não posso colocar isso como argumento de draw pois append me retorna None
                temp = Classes.Fabrica(i, ignore[i])
                placed.append(temp)
                Render.draw(simulationMap, [], placed)
                Render.pygame.display.update()

                print(f"Fábrica {name} foi colocada na posição {ignore[i]} isso está certo? (y/n)",end=" ")
                choice = input()

                if choice.casefold() == 'y'.casefold() or choice.casefold() == 's'.casefold():
                    confirm = True
                else:
                    del placed[placed.index(temp)]
                    print("Escolhendo outra posição...")
        
        return generate_factories(simulationMap, robotPos, ignore)

    if not file and not manual:
        return generate_factories(simulationMap, robotPos)

def get_obstacles(simulationMap:list, file:bool, manual:bool) -> None:
    """
    Insere obstáculos mapa, de acordo com input do usuário ou do que foi lido de um arquivo
    """
    if file:
        obstaculos = load_obstacles()
        for x,y in obstaculos:
            simulationMap[x][y].set_obstacle()
        return
    
    if manual:
        confirm = False

        print("Escolhendo posições para os obstáculos...\n")

        while not confirm:
            x, y = pretty_placer(simulationMap, lambda n: n)

            if not simulationMap[x][y].is_obstacle():
                simulationMap[x][y].set_obstacle()
            else:
                simulationMap[x][y].unset_obstacle()
            
            print(f"Obstáculo colocado/removido na posição {(x,y)}. Adicionar mais? (y/n)",end=" ")
            choice = input()
            Render.draw(simulationMap, [], [])
            Render.pygame.display.update()
            if choice.casefold() != 'y'.casefold() and choice.casefold() != 's'.casefold():
                confirm = True
            else:
                print("Escolhendo outra posição...")
        
        return