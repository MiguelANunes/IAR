import FileHandler, Dados
from copy import copy
from random import randint, shuffle, random
from math import exp, log, tanh

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

def calculate_cost(nodeList:list, solution:list, distances:dict) -> int:
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

def generate_neighbor(solution:list) -> list:
    """
    Gera um dado vizinho da solução dada
    Isto é, troca dois nós na solução
    Retorna a solução com dois nós trocados
    """
    newSolution = copy(solution)
    first, second = (randint(0, len(solution)-1), randint(0, len(solution)-1))
    # gerando dois números aleatórios entre 0 e o total de nós
    newSolution[first], newSolution[second] = newSolution[second], newSolution[first]
    
    return newSolution

def func0(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """
    Função de decrescimento de temperatura numero 0
    """
    return startTemp - (curIter * ((startTemp - finalTemp)/maxIter))

def func1(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """
    Função de decrescimento de temperatura numero 1
    """
    return startTemp * ((finalTemp/startTemp)**(curIter/maxIter))

def func3(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """
    Função de decrescimento de temperatura numero 3
    """
    a = log(startTemp - finalTemp)/log(maxIter)
    return startTemp - curIter**a

def func6(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """
    Função de decrescimento de temperatura numero 6
    """
    return 0.5*(startTemp-finalTemp)*(1-tanh((10.0*curIter/maxIter)-5.0)) + finalTemp

def simulated_annealing(nodeList:list, distances:dict) -> list:
    """
    Algoritmo do Simulated Annealing
    Recebe uma solução inicial (uma sequência de nós) para o TSP 
    Retorna uma solução possívelmente ótima
    """

    constMetropolis = 5   # constante de equilibrio térmico
    startTemp       = 100 # temperatura inicial
    finalTemp       = 1
    iteracao        = 0
    maxIter         = 40000

    initialSolution = Dados.get_labels(nodeList)
    shuffle(initialSolution)
    startingCost    = calculate_cost(nodeList, initialSolution, distances)
    # gerando uma solução inicial e calculando o custo dessa solução

    currentSolution = initialSolution
    currentCost     = startingCost
    temperature     = startTemp

    temperatures = [temperature]
    iterations   = [0]
    costs        = [currentCost]
    probs        = []

    while iteracao < maxIter:
        
        for _ in range(constMetropolis):
            newSolution = generate_neighbor(currentSolution)
            newCost     = calculate_cost(nodeList, newSolution, distances)

            if newCost < currentCost:
                # se achou uma solução melhor, troca
                currentCost     = newCost
                currentSolution = newSolution
            elif random() < exp((-1*(newCost - currentCost))/temperature):
                probs.append(exp((-1*(newCost - currentCost))/temperature))
                # Testa se a probabilidade gerada é menor que um número aleatório entre 0 e 1
                # Se passar, troca para a solução pior
                currentCost     = newCost
                currentSolution = newSolution
        

        # print(temperature)
        temperature = func6(startTemp, iteracao, finalTemp, maxIter)
        iteracao += 1
        # print(temperature)

        costs.append(currentCost)
        temperatures.append(temperature)
        iterations.append(iteracao)
        if temperature == finalTemp:
            break

    print(f"Custo final {currentCost}")
    return (costs, temperatures, iterations, probs)
