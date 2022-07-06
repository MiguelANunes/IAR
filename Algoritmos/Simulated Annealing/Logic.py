from copy import copy
import FileHandler, Dados
from random import randint, shuffle

def initialize(size:int) -> tuple:
    """
    Dado o tamanho da instância atual, lê os nós dessa instância
    Retorna uma tupla contendo todos os nós e a matriz de distância euclidiana (representada como dict de dicts)
    """
    nodes = FileHandler.load_nodes(size)

    if nodes == None:
        return
    
    distancias = dict()

    for node in nodes:
        tempDict = dict()
        for node1 in nodes:
            if node == node1: 
                # não calcula distância de um nó para ele mesmo
                continue
            if node1 in distancias:
                # se já está lá, não precisa recalcular
                tempDict[node1] = distancias[node1][node]
                continue
            tempDict[node1] = Dados.dist_euclidiana(node, node1)
        distancias[node] = tempDict

    # for key in distancias:
    #     for key1 in distancias[key]:
    #         print(f"distancias[{key.label}][{key1.label}]={distancias[key][key1]}")

    return (nodes, distancias)

def calculate_cost(nodeList:list, solution:list, distances:dict):
    """
    Calcula o custo de uma dada solução, com base nas distâncias dos dados
    Retorna o custo calculado
    """
    cost = 0
    for i in range(len(solution)-1):
        prevNode = Dados.get_node_from_label(nodeList, solution[i])
        nextNode = Dados.get_node_from_label(nodeList, solution[i+1])
        cost += distances[prevNode][nextNode]
    
    return cost

def generate_neighbor(solution:list):
    """
    Gera um dado vizinho da solução dada
    Isto é, troca dois nós na solução
    Retorna a solução com dois nós trocados
    """
    newSolution = copy(solution)
    first, second = (randint(0, len(solution)), randint(0, len(solution)))
    # gerando dois números aleatórios entre 0 e o total de nós
    newSolution[first], newSolution[second] = newSolution[second], newSolution[first]
    
    return newSolution

def simulated_annealing(nodeList:list, distances:dict) -> list:
    """
    Algoritmo do Simulated Annealing
    Recebe uma solução inicial (uma sequência de nós) para o TSP 
    Retorna uma solução possívelmente ótima
    """

    constMetropolis = 5   # constante de equilibrio térmico
    # temperature     = 100 # temperatura inicial
    iteracoes       = 100_000

    initialSolution = Dados.get_labels(nodeList)
    shuffle(initialSolution)
    startingCost    = calculate_cost(nodeList, initialSolution, distances)
    # gerando uma solução inicial e calculando o custo dessa solução

    currentSolution = initialSolution
    currentCost     = startingCost
    while iteracoes > 0:
        
        for _ in range(constMetropolis):
            newSolution = generate_neighbor(currentSolution)
            newCost     = calculate_cost(newSolution)

            if newCost < currentCost:
                currentCost = newCost
                currentSolution = newSolution
            else: # TODO: fazer a função de probabilidade de pegar a solução ruim
                pass

        iteracoes -= 1