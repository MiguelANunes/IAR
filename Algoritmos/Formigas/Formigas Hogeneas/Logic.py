from random import randint, choice, random
# from collections import Counter
import math

class Formiga(object):
    # Estado 0 == Não carregando
    # Estado 1 == Carregando

    def __init__(self, pos):
        self.current_pos   = pos
        self.past_pos      = (-1,-1)
        self.current_state = 0
        self.contents      = None
        # Dado que a formiga está carregando

        # Estado 0 == Não carregando
        # Estado 1 == Carregando

    def move(self, new_pos):
        self.past_pos = self.current_pos
        self.current_pos = new_pos

    def change_state(self, new_state):
        self.current_state = new_state

class Dados: 
    # https://docs.python.org/3/tutorial/classes.html
    # Passar argumento para o construtor para definir o tamanho
    # dos dados ao inves de hard-codar isso
    # Tamanho = 0 seria somente as formigas mortas
    # Generalizar as funções pra lidar com dados de tamanho desconhecido

    def __init__(self, size, valores, label=None):
        # criando um dado com tamanho de atributo variável
        self.attr = []
        self.size = size
        if label is not None:
            self.label = label
        for i in range(size):
            self.attr.append(valores[i])
        if size == 0:
            self.cor = (128,0,0)
        elif size == 1:
            r = valores[0] if valores[0] > 0 else valores[0]*-1
            r = 255 if r * 4 > 255 else r * 4
            b = int(r * 0.75)
            self.cor = (r,0,b)
        elif size == 2:
            if label == 1:
                self.cor = (200,0,0)
            elif label == 2:
                self.cor = (0,0,200)
            elif label == 3:
                self.cor = (200,0,200)
            else:
                self.cor = (200,200,0)
        else:
            raise Exception("Objeto tem atributos demais para calcular a cor")

def distancia(dado1, dado2):
    sums = []
    for i in range(dado1.size):
        sums.append((dado1.attr[i]-dado2.attr[i])**2)
    d = math.sqrt(sum(sums))
    # print(d)
    return d

def similaridade(atual, vizinhos, total_vizinhos, alfa=None):
    if alfa == None:
        alfa = 35.4347916 
        # média das distancias de 5 iterações diferentes

    # print("****")
    sums = []
    for v in vizinhos:
        x = distancia(atual, v)/alfa
        # print("x =",x)
        # print("1-x=",1-x)
        sums.append(1-x)

    r = (1/(total_vizinhos**2))*sum(sums)
    # if vizinhos == []:
    #     print("Sem vizinhos")
    # else:
    #     print("Total Vizinhos=", total_vizinhos)
    #     print("Total Vizinhos^2=", total_vizinhos**2)
    #     print("1/Total Vizinhos^2=", 1/total_vizinhos**2)
    #     print("sum(sums)=",sum(sums))
    #     print("Similaridade", r)
    # print("****")
    if r > 0:
        return r
    else:
        return 0

def pegar(atual, vizinhos, total_vizinhos, alfa=None, const1=None):
    if const1 == None:
        const1 = 0.4
    s = similaridade(atual,vizinhos,total_vizinhos, alfa)

    p = (const1 / (const1 + s))**2
    # print("Chance de Pegar", p)
    return p

def largar(atual, vizinhos, total_vizinhos, alfa=None, const2=None):
    if const2 == None:
        const2 = 0.85
    s = similaridade(atual,vizinhos,total_vizinhos,alfa)

    # print("Chance de largar", s)
    if s >= const2:
        return 1
    else:
        return 2*s

# def cria_formigueiro():
#     size_formigueiro = 50 # cria um mapa de 50x50
#     formigueiro = [[0 for i in range(size_formigueiro)] for i in range(size_formigueiro)]
#     formigas = []

#     for _ in range(1000): # insere 1000 itens
#         x = randint(0, 49)
#         y = randint(0, 49)
#         while formigueiro[x][y] == 1:
#             x = randint(0, 49)
#             y = randint(0, 49)
#         formigueiro[x][y] = 1

#     for _ in range(10): # insere 10 formigas
#         x = randint(0, 49)
#         y = randint(0, 49)
#         formigas.append(Formiga((x,y)))

#     return (formigueiro, formigas)

def cria_formigueiro(size, dados=None):
    size_formigueiro = 50 # cria um mapa de 50x50
    formigueiro = [[0 for i in range(size_formigueiro)] for i in range(size_formigueiro)]
    formigas = []

    for _ in range(400): # insere 400 itens
        x = randint(0, 49)
        y = randint(0, 49)
        if dados is None:
            d = Dados(size, [randint(1,20) for i in range(size)])
        else:
            d = dados.pop()
        while formigueiro[x][y] != 0:
            x = randint(0, 49)
            y = randint(0, 49)
        formigueiro[x][y] = 1

    for _ in range(10): # insere 10 formigas
        x = randint(0, 49)
        y = randint(0, 49)
        formigas.append(Formiga((x,y)))

    return (formigueiro, formigas)

def state_carrying(formiga: Formiga, formigueiro, possible_moves):
    # se a formiga está carregando um corpo
    pos_x, pos_y = formiga.current_pos

    # lista de células cadidatas a receber o corpo que a formiga está carregando
    candidates = [] 

    # direções possíveis de movimento
    for i,j in possible_moves:
        x, y = pos_x+i, pos_y+j
        
        if x < 0 or y < 0 or x >= 50 or y >= 50:
            continue

        candidates.append((x,y))

    # escolhendo um movimento
    move = choice(candidates)
    while move == formiga.past_pos:
        move = choice(candidates)

    # se escolheu a posição atual, testa para soltar
    if move == (pos_x, pos_y) and formigueiro[pos_x][pos_y] == 0:

            for i,j in possible_moves:
                x, y = pos_x+i, pos_y+j
                if x < 0 or y < 0 or x >= 50 or y >= 50:
                    continue
                if formigueiro[x][y] == 1:
                    vizinhos_cheios += 1
            
            if (vizinhos_cheios/len(possible_moves))**3 >= random():
                action_drop(formiga, formigueiro)
                formiga.change_state(0)
                return
    #se não, move para a posição que escolheu
    # caso falhe na célula estar vazia, formiga vai mover pra célula atual,
    # o que é a mesma coisa que não mover
    else:
        formiga.move(move)
        return

def state_not_carrying(formiga: Formiga, formigueiro, possible_moves):
    # se a formiga não está carregando um corpo
    pos_x, pos_y = formiga.current_pos

    # lista de células cadidatas a receber o corpo que a formiga está carregando
    candidates = [] 

    # direções possíveis de movimento
    for i,j in possible_moves:
        x, y = pos_x+i, pos_y+j
        
        if x < 0 or y < 0 or x >= 50 or y >= 50:
            continue
        candidates.append((x,y))

    move = choice(candidates)
    while move == formiga.past_pos:
        move = choice(candidates)

    # se escolheu a posição atual, testa para pegar
    if move == (pos_x, pos_y) and formigueiro[pos_x][pos_y] != 0:

            for i,j in possible_moves:
                x, y = pos_x+i, pos_y+j
                if x < 0 or y < 0 or x >= 50 or y >= 50:
                    continue
                if formigueiro[x][y] == 0:
                    vizinhos_vazios += 1
            
            if (vizinhos_vazios/len(possible_moves))**3 >= random():
                action_pick_up(formiga, formigueiro)
                formiga.change_state(1)
                return

    # se não, move para lá
    else:
        formiga.move(move)
        return

# def action_pick_up(formiga: Formiga, formigueiro):
#     x, y = formiga.current_pos
#     formigueiro[x][y] = 0

def action_pick_up(formiga: Formiga, formigueiro):
    x, y = formiga.current_pos
    formigueiro[x][y] = 0

def action_drop(formiga: Formiga, formigueiro):
    x, y = formiga.current_pos
    formigueiro[x][y] = 1
