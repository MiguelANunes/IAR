from random import randint

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

class Celula:

# Tipos de Células
# 0: Plano      (Verde)
# 1: Montanhoso (Marrom)
# 2: Pântano    (Azul)
# 3: Árido      (Vermelho)
# _: Obstáculo  (Preto)

    def __init__(self, tipo, contents=None):
        self.tipo     = tipo
        self.contents = contents

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

    def is_obstaculo(self):
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

class Robo:
    
    # pos => posição atual do robô
    # target => onde o robô quer chegar
    # contents => o que o robô está carregando, lista de ints, cada int é um tipo de item
    # lookingAt => célula que o robô está olhando enquanto executa o A*, usado para representar a decisão dele
    def __init__(self, pos, target=None, contents=None, lookingAt=None):
        self.position  = pos
        self.pastPos   = (-1,-1)
        self.target    = target if target != None else (-1,-1)
        self.lookingAt = lookingAt if lookingAt != None else (-1,-1)
        self.path      = []
        self.contents  = contents if contents != None else []
        self.radius    = 4

    def pick_up(self, cell: Celula):
        # retorna True se pegou um item

        if cell.contents in self.contents:
            return False
        else:
            self.contents = cell.contents
            cell.remove()
            return True

    def move(self, newPos):
        self.pastPos  = self.position
        self.position = newPos

    def follow_path(self):
        self.move(self.path.pop(0))

def load_map():
    simulationMap = []
    with open(f"inputs/input.txt") as f:
        for line in f:
            line = (line.replace("\t"," ")).replace(",",".")
            cells = [l.rstrip('\n') for l in line.split(" ") if l != '' and l != '\n']
            cell = [Celula(int(c)) for c in cells]
            simulationMap.append(cell)
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

def move_robot(robot, simulationMap, listItems, listFactories):
    pass
    # procura por itens que ainda não tem
    # move aleatóriamente até achar algo
    # tendo algo, continua movendo aleatório
    # se achar uma fábrica que precisa de algo e tem, entrega
    # se todas as fábricas estiverem satisfeitas, termina simulação