import Dados
from sys import stderr
from contextlib import redirect_stdout
from matplotlib import pyplot

def initialize(size:int) -> tuple:
    """
    Dado o tamanho da instância atual, lê os nós dessa instância
    Retorna uma tupla contendo todos os nós e a matriz de distância euclidiana (representada como dict de dicts)
    """
    nodes = load_nodes(size)

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

    with open(f"outputs/params.txt","w") as f:
        # limpando o arquivo de parametros
        pass

    return (nodes, distancias)

def load_nodes(size:int) -> list: 
    """
    Função que lê de um arquivo os dados de uma dada instância
    Recebe o tamanho a instância, 51 ou 100
    Retorna uma lista de todos os nós
    """
    nodes = []
    try:
        with open(f"inputs/mapa{size}.txt") as f:
            for line in f:
                node = tuple(map(int, (line.replace("\t","").rstrip("\n").split(" "))))
                nodes.append(Dados.Node(node[0], node[1], node[2]))
    except OSError:
        print("Erro ao ler os nós", file=stderr)
        return None
    
    return nodes

def dump_params(params:dict, finalCost:float) -> None:
    """
    Escreve num arquivo de log os parametros de uma execução do SA e o seu custo
    """
    try:
        with open(f"outputs/params.txt","a") as f:
            with redirect_stdout(f):
                for key in params:
                        if key == "func": 
                            # ignoro a função que foi usada
                            continue
                        print(f"{key:<15} {params[key]:>15}")
                print(f"{'Custo':<15} {finalCost:>15.4f}\n")

    except OSError:
        print("Não consegui escrever os parametros", file=stderr)
        exit()

def dump_values(costs: list, temps:list, iters:list) -> None:
    """
    Escreve num arquivo de log os resultados do SA
    """

    try:
        with open(f"outputs/custos.txt","w") as f:
            with redirect_stdout(f):
                for custo, iter in zip(costs, iters):
                    print(iter, custo)

    except OSError:
        print("Não consegui escrever os custos", file=stderr)
        exit()

    try:
        with open(f"outputs/temperaturas.txt","w") as f:
            with redirect_stdout(f):
                for temp, iter in zip(temps, iters):
                    print(iter, temp)

    except OSError:
        print("Não consegui escrever as temperaturas", file=stderr)
        exit()

def dump_probs(probs: list) -> None:
    """
    Função que escreve num arquivo de log os resultados do SA
    """

    try:
        with open(f"outputs/probabilidades.txt","w") as f:
            with redirect_stdout(f):
                for i, prob in enumerate(probs):
                    print(i, prob)

    except OSError:
        print("Não consegui escrever as probabilidades", file=stderr)
        exit()

def plot_costs(index:str) -> None:
    """
    Plota um gráfico contendo os valores de custos gerados pelo SA
    """
    x = []
    y = []

    try:
        with open(f"outputs/custos.txt","r") as f:
            for line in f.readlines():
                line = line.split()
                x.append(int(line[0]))
                y.append(float(line[1]))
    except OSError:
        print("Não consegui ler os custos", file=stderr)
        exit()
    
    pyplot.plot(x,y,label="Custos")

    pyplot.xlabel("Iterações")
    pyplot.ylabel("Custos")

    pyplot.title("Custos")
    pyplot.legend()

    pyplot.savefig(f"images/Custos - {index}.png")
    pyplot.close()

def plot_temps(index:str) -> None:
    """
    Plota um gráfico contendo os valores de temperaturas gerados pelo SA
    """
    x = []
    y = []

    try:
        with open(f"outputs/temperaturas.txt","r") as f:
            for line in f.readlines():
                line = line.split()
                x.append(int(line[0]))
                y.append(float(line[1]))
    except OSError:
        print("Não consegui ler as temperaturas", file=stderr)
        exit()
    
    pyplot.plot(x,y,label="Temperaturas")

    pyplot.xlabel("Iterações")
    pyplot.ylabel("Temperaturas")

    pyplot.title("Temperaturas")
    pyplot.legend()

    pyplot.savefig(f"images/Temperaturas - {index}.png")
    pyplot.close()

def plot_probs(index:str) -> None:
    """
    Plota um gráfico contendo os valores de probabilidades gerados pelo SA
    """
    x = []
    y = []

    try:
        with open(f"outputs/probabilidades.txt","r") as f:
            for line in f.readlines():
                line = line.split()
                x.append(int(line[0]))
                y.append(float(line[1]))
    except OSError:
        print("Não consegui ler as probabilidades", file=stderr)
        exit()
    
    pyplot.plot(x,y,label="Probabilidades")

    pyplot.xlabel("Teste")
    pyplot.ylabel("Probabilidades")

    pyplot.title("Probabilidades")
    pyplot.legend()

    pyplot.savefig(f"images/Probabilidades - {index}.png")
    pyplot.close()