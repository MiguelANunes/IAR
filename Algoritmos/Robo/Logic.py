from random import randint

class Item:
    # Tipos de itens:
    # 0: Bateria de carga elétrica;
    # 1: Braço de solda;
    # 2: Bomba de sucção;
    # 3: Dispositivo de refrigeração;
    # 4: Braço pneumático.
    def __init__(self, tipo, pos):
        self.tipo = tipo
        self.pos = pos
    

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

    def __init__(self, tipo, pos, qtd=None, obj=None):
        self.tipo    = tipo
        self.pos     = pos
        self.request = (qtd, obj) # request será uma tupla (int, int), segundo int é o tipo do item

    def set_request(self, qtd: int, obj: int):
        self.request = (qtd, obj)

def load_map():
    simMap = []
    with open(f"inputs/input.txt") as f:
        for line in f:
            line = (line.replace("\t"," ")).replace(",",".")
            cells = [l.rstrip('\n') for l in line.split(" ") if l != '' and l != '\n']
            cell = [Celula(int(c)) for c in cells]
            simMap.append(cell)
    return simMap

def generate_factories():

    factoryList = []

    pos = (randint(0, 41), randint(0, 41))
    fabricaGraos = Fabrica("grao", pos, 8, 0)
    factoryList.append(fabricaGraos)

    pos = (randint(0, 41), randint(0, 41))
    fabricaBarcos = Fabrica("casco", pos, 5, 1)
    factoryList.append(fabricaBarcos)

    pos = (randint(0, 41), randint(0, 41))
    fabricaPetrobras = Fabrica("petroleo", pos, 2, 2)
    factoryList.append(fabricaPetrobras)

    pos = (randint(0, 41), randint(0, 41))
    fabricaFundicao = Fabrica("fundicao", pos, 5, 3)
    factoryList.append(fabricaFundicao)

    pos = (randint(0, 41), randint(0, 41))
    fabricaVigas = Fabrica("vigas", pos, 2, 4)
    factoryList.append(fabricaVigas)

    return factoryList

def generate_items():
    pos = (randint(0, 41), randint(0, 41))