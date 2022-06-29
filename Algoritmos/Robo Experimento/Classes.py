import sys

import Logic

class Item:
    """
    Tipos de itens:
        0: Bateria de carga elétrica;
        1: Braço de solda;
        2: Bomba de sucção;
        3: Dispositivo de refrigeração;
        4: Braço pneumático.
    """

    def __init__(self, tipo, pos):
        self.tipo     = tipo
        self.position = pos
    
        if self.tipo == 0:
            self.name = "Bateria"
            self.color = (64,0,64) # Roxo Escuro

        elif self.tipo == 1:
            self.name = "Braço de Solda"
            self.color = (100,100,0) # Amarelo Escuro

        elif self.tipo == 2:
            self.name = "Bomba"
            self.color = (0,100,100) # Azul Não Muito Escuro

        elif self.tipo == 3:
            self.name = "Refrigerador"
            self.color = (150,0,100) # Rosa escuro
        
        else:
            self.name = "Braço Pneumatico"
            self.color = (0,100,0) # Verde escuro
    
    def __str__(self) -> str:
        return "{"+self.name+": "+str(self.position)+"}"

    def __repr__(self) -> str:
        return str(self)

class Celula:
    """
    Tipos de Células
        0: Plano      (Verde)
        1: Montanhoso (Marrom)
        2: Pântano    (Azul)
        3: Árido      (Vermelho)
        _: Obstáculo  (Preto)
    """

    def __init__(self, tipo, position=None, contents=None):
        self.tipo     = tipo
        self.contents = contents
        self.position = position

        if self.tipo == 0:
            self.cost = 1
            self.color  = (0, 128, 0) # Verde

        elif self.tipo == 1:
            self.cost = 5
            self.color  = (96, 48, 12) # Marrom

        elif self.tipo == 2:
            self.cost = 10
            self.color  = (0, 0, 128) # Azul

        elif self.tipo == 3:
            self.cost = 15
            self.color  = (128, 0, 0) # Vermelho
        
        else:
            self.cost = -1
            self.color  = (0, 0, 0) # Preto

    def place(self, obj):
        self.contents = obj

    def is_obstacle(self):
        return self.cost == -1

    def set_obstacle(self):
        self.oldTipo  = self.tipo
        self.oldCost  = self.cost
        self.oldColor = self.color
        self.tipo     = -1
        self.cost     = -1
        self.color    = (0, 0, 0) # Preto

    def unset_obstacle(self):
        self.tipo  = self.oldTipo
        self.cost  = self.oldCost
        self.color = self.oldColor

    def remove(self):
        self.contents = None

    def __str__(self) -> str:
        c = f" {self.contents}" if self.contents != None else ""
        return f"{self.tipo}{c}"

class Fabrica:
    """
    Tipos de industrias e suas necessidades
        0: Indústria de melhoramento genético de grãos    | Necessita de 8 baterias
        1: Empresa de manutenção de cascos de embarcações | Necessita de 5 braços de solda
        2: Indústria petrolífera                          | Necessita de 2 bombas
        3: Fábrica de fundição                            | Necessita de 5 refrigeradores
        4: Indústria de vigas de aço                      | Necessita de 2 braços pneumáticos
    """

    def __init__(self, tipo, pos, qtd=None, obj=None):
        self.tipo     = tipo
        self.position = pos
        self.request  = (qtd, obj) # request será uma tupla (int, int), segundo int é o tipo do item

        if self.tipo == 0:
            self.name = "Agro é Pop"
            self.color  = (198,0,198) # Rosa

        elif self.tipo == 1:
            self.name = "Blohm und Voß"
            self.color  = (198,198,0) # Amarelo

        elif self.tipo == 2:
            self.name = "Petrobras"
            self.color = (0,198,198) # Azul Claro

        elif self.tipo == 3:
            self.name = "Fundição Tupy"
            self.color  = (198,0,64) # Bordô
        
        else:
            self.name = "Gerdau"
            self.color  = (0, 198, 78) # Verde Claro

    def __str__(self) -> str:
        return "{"+self.name+": "+str(self.position)+"}"

    def __repr__(self) -> str:
        return str(self)

    def set_request(self, qtd: int, obj: int):
        self.request = (qtd, obj)

    def deliver(self):
        result = self.request[0]-1
        if result > 0:
            self.request = (result, self.request[1])
        else:
            self.request = (0,-1)

    def compare(self, otherFactory) -> bool:
        return self.tipo == otherFactory.tipo and self.position == otherFactory.position and self.name == otherFactory.name

class Robo:
    """
    position => posição atual do robô
    pastPos => ultima posição do robô
    path => caminho que o robô calculou com o A*
    contents => o que o robô está carregando, lista de ints, cada int é um tipo de item
    radius => raio de visão do robô
    """

    def __init__(self, pos:tuple):
        self.position      = pos     # tupla (x,y)
        self.pastPos       = (-1,-1) # tupla (x,y)
        self.path          = []      # lista de tuplas (x,y)
        self.contents      = []      # lista de items
        self.state         = 0  
        self.radius        = 4  
        self.factories     = []      # lista de fábricas
        self.itemPos       = []      # lista de tuplas (x,y)
        self.targetFactory = None    # qual fábrica o robô quer chegar

    def pick_up(self, cell: Celula) -> None:
        self.contents.append(cell.contents)
        cell.remove()

    def get_content_type(self) -> list:
        return [x.tipo for x in self.contents]

    def get_content_names(self) -> list:
        l = []
        for x in self.contents:
            l.append(x.name)
        return l

    def get_content_name_by_type(self, type):
        return [x.name for x in self.contents if x.tipo == type][0]

    def remove_content_by_type(self, type):
        """
        Remove um item dos conteúdos do robô, dado seu tipo
        """
        done = False
        l = []
        for item in self.contents:
            if item.tipo == type and not done:
                done = True
                continue
            l.append(item)
        self.contents = l

    def move_to(self, newPos) -> None:
        self.pastPos  = self.position
        self.position = newPos

    def change_state(self, newState) -> None:
        self.state = newState

    def set_factories(self, factoryList:list) -> None:
        self.factories = factoryList

    def get_necessary_items(self) -> list:
        """
        Retorna uma lista contendo todos os tipos de itens que as fábricas
        que o robô vê precisam
        """
        return [x.request[1] for x in self.factories]

    def deliver(self, factory:Fabrica) -> int:
        """
        Dado uma fábrica, entrega todos os items que o robô tem que essa fábrica precisa para a fábrica
        Retorna o total de itens entregue
        """
        count = 0
        for item in self.contents:
            if item.tipo in factory.request:
                factory.deliver()
                del self.contents[self.contents.index(item)]
                count += 1
                if factory.request == (0,-1): 
                    # se satisfez a necessidade de uma fábrica, tira ela da lista de fábricas acessíveis
                    for index, fact in enumerate(self.factories):
                        # como eu tenho uma cópia da lista de fábricas global, não posso
                        # verificar se uma dada fábrica está nessa lista, pois apenas sua cópia está nela
                        # isto é, não tenho um objeto Fábrica dentro da minha lista, tenho apenas cópias deles
                        if factory.tipo == fact.tipo:
                            self.factories.pop(index)
                            return (count, True)
            if factory.request == (0,-1):
                return (count, False)
        return (count, True)

class PriorityQueue:
    """
    Uma implementação boba porém simples de fila de prioridade minima
    """
    def __init__(self, startcell=None, startWeight=None):
        weight    = startWeight if startWeight != None else -1
        temp_cell = startcell if startcell != None else (-1,-1)

        if Logic.is_valid(temp_cell) and weight >= 0:
            self.queue = [(weight, temp_cell)]
        else:
            self.queue = []

    def __str__(self) -> str:
        return str(self.queue)

    def __repr__(self) -> str:
        return str(self)

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