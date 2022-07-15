from math import sqrt

class Node:

    def __init__(self, label, posX, posY) -> None:
        self.label    = label
        self.position = (posX, posY)
    
    def __repr__(self) -> str:
        return f"({str(self.label)}; {str(self.position[0])}, {str(self.position[1])})"
    
    def __str__(self) -> str:
        return f"Nó {str(self.label)}: {str(self.position)}"

def dist_euclidiana(node, otherNode) -> float:
    """Calcula a distância euclidiana entre dois nós"""
    return sqrt((otherNode.position[0]-node.position[0])**2 + (otherNode.position[1]-node.position[1])**2)

def get_labels(nodeDict:dict) -> list:
    """
    Dada um dict de nós, retorna uma lista contendo todas as labels dos nós
    """
    labelList = []
    for label in nodeDict:
        labelList.append(label)

    return labelList

def get_node_from_label(nodeList:list, label:int):
    """
    Dado uma lista de nós, retornar o nó cuja label é igual a label passada de argumento
    """
    for node in nodeList:
        if node.label == label:
            return node