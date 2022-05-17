from random import randint, choice, random
# from collections import Counter
import math

class Formiga:
    # current_pos   = (-1,-1)
    # past_pos      = (-1,-1)
    # current_state = -1
    # contents      = None

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

    def __init__(self, size, valores, label):
        self.attr = []
        self.size = size
        self.label = label
        for i in range(size):
            self.attr.append(valores[i])
        if label % 2 == 0:
            r  = 20*label if 20*label < 255 else 255
            bg = 10*label if 10*label < 255 else 200
            if r < 50:
                r += 30
            self.cor = (r,int(2*bg/5),int(3*bg/5))
        elif label % 5 == 0:
            g  = 20*label if 20*label < 255 else 255
            rb = 10*label if 10*label < 255 else 200
            if g < 50:
                g += 30
            self.cor = (int(3*rb/5),g,int(2*rb/5))
        else:
            b  = 20*label if 20*label < 255 else 255
            rg = 10*label if 10*label < 255 else 200
            if b < 50:
                b += 30
            self.cor = (int(2*rg/5),int(3*rg/5),b)

def distancia(dado1, dado2):
    sums = []
    for i in range(dado1.size):
        sums.append((dado1.attr[i]-dado2.attr[i])**2)
    d = math.sqrt(sum(sums))
    # print(d)
    return d

def similaridade(atual, vizinhos, total_vizinhos, alfa=None):
    if alfa == None:
        alfa = 5.651564006570254

    sums = []
    for v in vizinhos:
        x = distancia(atual, v)/alfa
        sums.append(1-x)

    r = (1/(total_vizinhos**2))*sum(sums)
    if r > 0:
        return r
    else:
        return 0

def pegar(atual, vizinhos, total_vizinhos, alfa=None, const1=None):
    if const1 == None:
        const1 = 0.4
    s = similaridade(atual,vizinhos,total_vizinhos, alfa)

    p = (const1 / (const1 + s))**2
    return p

def largar(atual, vizinhos, total_vizinhos, alfa=None, const2=None):
    if const2 == None:
        const2 = 0.8
    s = similaridade(atual,vizinhos,total_vizinhos,alfa)

    if s >= const2:
        return 1
    else:
        return 2*s

def cria_formigueiro(size, dados=None):
    size_formigueiro = 50 
    formigueiro = [[0 for i in range(size_formigueiro)] for i in range(size_formigueiro)]
    formigas = []

    for _ in range(600):
        x = randint(0, 49)
        y = randint(0, 49)
        if dados is None:
            d = Dados(size, [randint(1,20) for _ in range(size)])
        else:
            d = dados.pop()
                
        while formigueiro[x][y] != 0:
            x = randint(0, 49)
            y = randint(0, 49)
        formigueiro[x][y] = d

    for _ in range(10): # insere 10 formigas
        x = randint(0, 49)
        y = randint(0, 49)
        formigas.append(Formiga((x,y)))

    return (formigueiro, formigas)

def read_formigueiro(size, filename):
    valores = []
    with open(f"input/{filename}") as f:
        for line in f:
            line = (line.replace("\t"," ")).replace(",",".")
            cell = [l.rstrip('\n') for l in line.split(" ") if l != '' and l != '\n']
            d = Dados(2,[float(cell[0]),float(cell[1])],int(cell[2]))
            valores.append(d)

    return cria_formigueiro(size, valores)
    
def state_carrying(formiga: Formiga, formigueiro, possible_moves, a=None, k2=None):
    # se a formiga está carregando um corpo
    pos_x, pos_y = formiga.current_pos
    
    # lista de células cadidatas a receber o corpo que a formiga está carregando
    candidates = [] 

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

        vizinhos = []
        for x,y in candidates:
            if formigueiro[x][y] != 0 and (x,y) != (pos_x, pos_y):
                vizinhos.append(formigueiro[x][y])

        if vizinhos != []:
            chance = largar(formiga.contents, vizinhos, len(candidates),a,k2)
        
            if chance >= random():
                action_drop(formiga, formigueiro)
                formiga.change_state(0)
                return
    #se não, move para a posição que escolheu
    # caso falhe na célula estar vazia, formiga vai mover pra célula atual,
    # o que é a mesma coisa que não mover
    else:
        formiga.move(move)
        return

def state_not_carrying(formiga: Formiga, formigueiro, possible_moves, a=None, k1=None):
    # se a formiga não está carregando um corpo
    pos_x, pos_y = formiga.current_pos
    
    # lista de células cadidatas ao movimento da formiga
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

        vizinhos = []
        for x,y in candidates:
            if formigueiro[x][y] != 0 and (x,y) != (pos_x, pos_y):
                vizinhos.append(formigueiro[x][y])

        chance = pegar(formigueiro[pos_x][pos_y], vizinhos, len(candidates),a,k1)
        
        if chance >= random():
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
    formiga.contents = formigueiro[x][y]
    formigueiro[x][y] = 0

# def action_drop(formiga: Formiga, formigueiro):
#     x, y = formiga.current_pos
#     formigueiro[x][y] = 1

def action_drop(formiga: Formiga, formigueiro):
    x, y = formiga.current_pos
    formigueiro[x][y] = formiga.contents
    formiga.contents = None