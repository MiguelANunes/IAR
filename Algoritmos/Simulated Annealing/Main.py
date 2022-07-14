import Logic, FileHandler
from Functions import *

def main() -> None:
    """
    Função principal do SA
    Gera os nós e suas distâncias e inicia o loop principal do SA
    """

    funcs = {func6:"func6", func2: "func2"}
    for size in [51]:
        # TODO: Melhorar a lista de nós para ser mais eficiente buscar nela
        nodes, distances = FileHandler.initialize(size)
        for f in funcs:

            for index in range(10):

                print(f"Tamanho {size}, teste {index}, função: {funcs[f]}")
                # TODO: Lidar com parametros diferentes dinamicamente
                params = {"metropolis":5, "startTemp":100, "finalTemp":0, "maxIter":40000, "func":f, "funcName":funcs[f]}

                results   = Logic.simulated_annealing(nodes, distances, params)
                costs     = results["costs"]
                temps     = results["temps"]
                iters     = results["iters"]
                finalCost = results["finalCost"]
                # probs = results["probs"]

                print(f"Custo final {finalCost}")

                FileHandler.dump_params(params, finalCost)
                FileHandler.dump_values(costs, temps, iters)
                # FileHandler.dump_probs(probs)

                FileHandler.plot_costs("Tamanho: "+str(size)+": Função:"+funcs[f]+": Teste"+str(index))
                FileHandler.plot_temps("Tamanho: "+str(size)+": Função:"+funcs[f]+": Teste"+str(index))
                # FileHandler.plot_probs("Tamanho: "+str(size)+": Função:"+funcs[f]+": Teste"+str(index))

if __name__ == "__main__":
    main()
