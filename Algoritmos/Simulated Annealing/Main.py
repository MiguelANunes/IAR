import Logic, Dados

def main() -> None:
    """
    Função principal do SA
    Gera os nós e suas distâncias e inicia o loop principal do SA
    """
    size = 51

    nodes, distances = Logic.initialize(size)
    Logic.simulated_annealing(nodes, distances)

if __name__ == "__main__":
    main()


# Solução é uma permutação de nós
# Uma perturbação é trocar dois nós da sequência
# Exemplo:
    # 2 4 3 5 1
    # É uma solução possível para um caso de 5 itens
    # 2 1 3 5 4
    # É uma perturbação da solução