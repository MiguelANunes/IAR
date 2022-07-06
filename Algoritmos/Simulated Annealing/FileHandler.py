import Dados
from sys import stderr

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