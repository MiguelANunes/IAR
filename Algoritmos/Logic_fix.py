from random import randint
import math

class Formiga(object):
    current_pos   = (-1,-1)
    past_pos      = (-1,-1)
    current_state = -1
    # Estado 0 == Não carregando
    # Estado 1 == Carregando

    def __init__(self, pos):
        self.current_pos   = pos
        self.past_pos      = (-1,-1)
        self.current_state = 0

    def move(self, new_pos):
        self.past_pos = self.current_pos
        self.current_pos = new_pos

    def change_state(self, new_state):
        self.current_state = new_state

def cria_formigueiro():
    size_formigueiro = 50 # cria um mapa de 50x50
    formigueiro = [[0 for i in range(size_formigueiro)] for i in range(size_formigueiro)]
    formigas = []

    for _ in range(1000): # insere 1000 itens
        x = randint(0, 49)
        y = randint(0, 49)
        while formigueiro[x][y] == 1:
            x = randint(0, 49)
            y = randint(0, 49)
        formigueiro[x][y] += 1

    for _ in range(10): # insere 10 formigas
        x = randint(0, 49)
        y = randint(0, 49)
        formigas.append(Formiga((x,y)))

    return (formigueiro, formigas)

def state_carrying(formiga: Formiga, formigueiro):
    # se a formiga está carregando um corpo
    pos_x, pos_y = formiga.current_pos
    old_x, old_y = formiga.past_pos
    
    # lista de células cadidatas a receber o corpo que a formiga está carregando
    candidates = [] 

    # direções possíveis de movimento
    dir_x = [1, -1, 0, 0, 1, 1, -1, -1, 0]
    dir_y = [0, 0, 1, -1, 1, -1, 1, -1, 0]
    for i,j in zip(dir_x, dir_y):
        x, y = pos_x+i, pos_y+j
        total = 0

        if (old_x, old_y) == (x, y):
            continue
        
        outside_borders = x < 0 or y < 0 or x >= 50 or y >= 50
        if outside_borders:
            continue

        # se uma célula está vazia
        if formigueiro[x][y] == 0:
            # veja quantos vizinhos ocupados ela tem
            for i1,j1 in zip(dir_x, dir_y):
                if formigueiro[x+i1][y+j1] == 1:
                    total += 1
            for _ in range(total):
                candidates.append((x,y))
                # quanto mais vizinhos ocupados ao redor da célula, maior a chance dela ser selecionada
    
    # se não achou nenhuma célula válida
    if candidates == []:
        # -2 pois não quero o ultimo elemento (não mover)
        x = dir_x[randint(0,len(dir_x)-2)]
        y = dir_y[randint(0,len(dir_x)-2)]
        while (pos_x+x,pos_y+y) == (old_x, old_y):
            x = dir_x[randint(0,len(dir_x)-2)]
            y = dir_y[randint(0,len(dir_x)-2)]
        # escolhe um movimento aleatório
        move = (pos_x+x, pos_y+y)
    else:
        move = candidates[randint(0,len(candidates)-1)]

    # se escolheu a posição atual, solta
    if move == (pos_x, pos_y):
        action_drop(formiga, formigueiro)
        formiga.change_state(0)
        return
    
    #  se não, move para a posição que escolheu
    formiga.move(move)
    return

def state_not_carrying(formiga: Formiga, formigueiro):
    # se a formiga não está carregando um corpo
    pos_x, pos_y = formiga.current_pos
    old_x, old_y = formiga.past_pos
    
    # lista de células cadidatas ao movimento da formiga
    candidates = [] 

    # direções possíveis de movimento
    dir_x = [1, -1, 0, 0, 1, 1, -1, -1, 0]
    dir_y = [0, 0, 1, -1, 1, -1, 1, -1, 0]

    for i,j in zip(dir_x, dir_y):
        x, y = pos_x+i, pos_y+j
        total = 0

        if (x,y) == (old_x, old_y):
            continue

        outside_borders = x < 0 or y < 0 or x >= 50 or y >= 50
        if outside_borders:
            continue
        
        # se uma célula está ocupada
        if formigueiro[x][y] == 1:
            # veja quantos vizinho vazios ela tem
            for i1,j1 in zip(dir_x, dir_y):
                if formigueiro[x+i1][y+j1] == 0:
                    total += 1
            for _ in range(total):
                candidates.append((formigueiro[x][y],(x,y)))
            # quanto mais vizinhos vazios ao redor da célula, maior a chance dela ser selecionada


    # se não achou nenhuma célula válida
    if candidates == []:
        # -2 pois não quero o ultimo elemento (não mover)
        x = dir_x[randint(0,len(dir_x)-2)]
        y = dir_y[randint(0,len(dir_x)-2)]
        while (pos_x+x,pos_y+y) == (old_x, old_y):
            x = dir_x[randint(0,len(dir_x)-2)]
            y = dir_y[randint(0,len(dir_x)-2)]
        # escolhe um movimento aleatório
        move = (pos_x+x, pos_y+y)
    else:
        move = candidates[randint(0,len(candidates)-1)]

    # se escolheu a posição atual, pega
    if move == (pos_x, pos_y)  and formigueiro[x][y] != 0:
        # não pega se não tem nada
        action_pick_up(formiga, formigueiro)
        formiga.change_state(1)
        return

    #  se não, move para a posição que escolheu
    formiga.move(move)
    return

def action_pick_up(formiga: Formiga, formigueiro):
    x, y = formiga.current_pos
    formigueiro[x][y] -= 1
    if formigueiro[x][y] < 0:
        formigueiro[x][y] = 0

def action_drop(formiga: Formiga, formigueiro):
    x, y = formiga.current_pos
    formigueiro[x][y] += 1