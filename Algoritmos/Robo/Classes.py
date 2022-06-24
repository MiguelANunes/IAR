import sys
import Logic

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
            self.cor = (64,0,64) # Roxo Escuro

        elif self.tipo == 1:
            self.cor = (100,100,0) # Amarelo Escuro

        elif self.tipo == 2:
            self.cor = (0,100,100) # Azul Não Muito Escuro

        elif self.tipo == 3:
            self.cor = (150,0,100) # Rosa escuro
        
        else:
            self.cor = (0,100,0) # Verde escuro
    
    def __str__(self) -> str:
        return "{"+str(self.tipo)+";"+str(self.position)+"}"

    def __repr__(self) -> str:
        return str(self)

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
            self.cor  = (0, 128, 0) # Verde

        elif self.tipo == 1:
            self.cost = 5
            self.cor  = (96, 48, 12) # Marrom

        elif self.tipo == 2:
            self.cost = 10
            self.cor  = (0, 0, 128) # Azul

        elif self.tipo == 3:
            self.cost = 15
            self.cor  = (128, 0, 0) # Vermelho
        
        else:
            self.cost = -1
            self.cor  = (0, 0, 0) # Preto

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
        self.tipo     = tipo
        self.position = pos
        self.request  = (qtd, obj) # request será uma tupla (int, int), segundo int é o tipo do item

        if self.tipo == 0:
            self.cor = (198,0,198) # Rosa

        elif self.tipo == 1:
            self.cor = (198,198,0) # Amarelo

        elif self.tipo == 2:
            self.cor = (0,198,198) # Azul Claro

        elif self.tipo == 3:
            self.cor = (198,0,64) # Bordô
        
        else:
            self.cor = (0, 198, 78) # Verde Claro

    def set_request(self, qtd: int, obj: int):
        self.request = (qtd, obj)

    def deliver(self):
        result = self.request[0]-1
        if result > 0:
            self.request = (result, self.request[1])
        else:  # TODO: Tratar o caso em que a request é None
            self.request = (-1,-1)

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

    def get_contents(self) -> list:
        return [x.tipo for x in self.contents]

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

        if Logic.is_valid(temp_cell) and weight >= 0:
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