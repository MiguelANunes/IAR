import Dados
from copy import copy
from random import randint, shuffle, random
from math import exp

def calculate_cost(nodeDict:dict, solution:list, distances:dict) -> int:
    """
    Calcula o custo de uma dada solução (lista de labels), com base nas distâncias dos dados
    Retorna o custo calculado
    """
    cost = 0
    for i in range(len(solution)-1):
        prevNode = nodeDict[solution[i]]
        nextNode = nodeDict[solution[i+1]]
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

def simulated_annealing(nodeDict:list, distances:dict, params:dict) -> list:
    """
    Algoritmo do Simulated Annealing
    Recebe uma solução inicial (uma sequência de nós) para o TSP 
    Retorna uma solução possívelmente ótima
    """

    constMetropolis = params["metropolis"] # constante de equilibrio térmico
    startTemp       = params["startTemp"]  # temperatura inicial
    finalTemp       = params["finalTemp"]
    iteracao        = 0
    maxIter         = params["maxIter"]
    func            = params["func"]

    initialSolution = Dados.get_labels(nodeDict)
    shuffle(initialSolution)
    startingCost    = calculate_cost(nodeDict, initialSolution, distances)
    bestSolution    = initialSolution
    bestCost        = startingCost
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
            newCost     = calculate_cost(nodeDict, newSolution, distances)

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
            
            if currentCost <= bestCost:
                bestCost     = currentCost
                bestSolution = currentSolution
        

        temperature = func(startTemp, iteracao, finalTemp, maxIter)
        iteracao += 1

        costs.append(currentCost)
        temperatures.append(temperature)
        iterations.append(iteracao)
        if temperature == finalTemp:
            break

    return {"costs":costs, "temps":temperatures, "iters":iterations, "probs":probs, "bestResult": (bestCost, bestSolution)}
