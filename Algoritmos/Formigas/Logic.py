from random import randint, choice, random
from collections import Counter
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
        self.last_action = 2

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
    raio = 1

    for i in range(-raio, raio+1):
        for j in range(-raio, raio+1):
            x, y = pos_x+i, pos_y+j

            if (old_x, old_y) == (x, y):
                continue
            
            if x < 0 or y < 0 or x >= 50 or y >= 50:
                continue

            candidates.append((pos_x+i, pos_y+j))

    # escolhendo um movimento
    move = choice(candidates)
    while move == formiga.past_pos:
        move = choice(candidates)

    # se escolheu a posição atual, testa para soltar
    if move == (pos_x, pos_y):
        vizinhos_cheios = 0
        if formigueiro[pos_x][pos_y] == 0:

            for i in range(-raio, raio+1):
                for j in range(-raio, raio+1):
                    x, y = pos_x+i, pos_y+j
                    if x < 0 or y < 0 or x >= 50 or y >= 50:
                        continue
                    if formigueiro[x][y] == 1:
                        vizinhos_cheios += 1
            
            if (vizinhos_cheios/8) >= random():
                action_drop(formiga, formigueiro)
                formiga.change_state(0)
                return
    #se não, move para a posição que escolheu
    else:
        formiga.move(move)
        return

def state_not_carrying(formiga: Formiga, formigueiro):
    # se a formiga não está carregando um corpo
    pos_x, pos_y = formiga.current_pos
    old_x, old_y = formiga.past_pos
    
    # lista de células cadidatas ao movimento da formiga
    candidates = [] 

    # direções possíveis de movimento
    raio = 1
    for i in range(-raio, raio+1):
        for j in range(-raio, raio+1):
            x, y = pos_x+i, pos_y+j

            if (old_x, old_y) == (x, y):
                continue
            
            if x < 0 or y < 0 or x >= 50 or y >= 50:
                continue
            
            candidates.append((x,y))

    move = choice(candidates)
    while move == formiga.past_pos:
        move = choice(candidates)

    # se escolheu a posição atual, testa para pegar
    if move == (pos_x, pos_y):
        vizinhos_vazios = 0
        if formigueiro[pos_x][pos_y] == 1:

            for i in range(-raio, raio+1):
                for j in range(-raio, raio+1):
                    x, y = pos_x+i, pos_y+j
                    if x < 0 or y < 0 or x >= 50 or y >= 50:
                        continue
                    if formigueiro[x][y] == 0:
                        vizinhos_vazios += 1
            
            if (vizinhos_vazios/8) >= random():
                action_pick_up(formiga, formigueiro)
                formiga.change_state(1)
                return

    # se não, move para lá
    else:
        if move != (old_x,old_y):
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