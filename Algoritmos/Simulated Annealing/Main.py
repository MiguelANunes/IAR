import Logic, FileHandler
from Functions import *
#from contextlib import redirect_stdout


def print_solution(nodeDict:dict, solution:list) -> None:
    """
    Printa na tela os nós da melhor solução encontrada
    """
    for i in range(len(solution)-1):
        if i != 0: print(" -> ",end="")
        prevNode = nodeDict[solution[i]]
        nextNode = nodeDict[solution[i+1]]
        print(prevNode.__repr__(), end=" -> ")
        print(nextNode.__repr__(), end="")
    print()

def main() -> None:
    """
    Função principal do SA
    Gera os nós e suas distâncias e inicia o loop principal do SA
    """
    print("Valor ótimo para 51:   426")
    print("Valor ótimo para 100:  21_282")

    funcs    = {51: {func6:"func6", func7:"func7", func9:"func9"}, 100: {func6:"func6", func7:"func7", func9:"func9"}}
    plotTemp = {(name, size): False for size,funs in funcs.items() for _, name in  funs.items()}

    for size in [51, 100]:
        nodes, distances = FileHandler.initialize(size)
        print(f"Tamanho {size}")
        for index in range(10):
            
            print(f"\tTeste {index}")
            for f in funcs[size]:

                print(f"\t\t{funcs[size][f]}:", end=" ")

                params             = get_best_param(size, funcs[size][f])
                params["func"]     = f
                params["funcName"] = funcs[size][f]

                results                = Logic.simulated_annealing(nodes, distances, params)
                costs                  = results["costs"]
                temps                  = results["temps"]
                iters                  = results["iters"]
                bestCost, bestSolution = results["bestResult"]
                # probs = results["probs"]

                print(f"{bestCost:.3f}")
                
                # with open(f"outputs/best.txt","a") as f:
                #     with redirect_stdout(f):
                #         print(f"{bestCost}")
                #         print_solution(nodes, bestSolution)

                FileHandler.dump_params(size, params, bestCost)
                FileHandler.dump_values(costs, temps, iters)
                # FileHandler.dump_probs(probs)

                filename = str(size)+funcs[size][f]+"-"+str(index)
                FileHandler.plot_costs(filename, index)
                if not plotTemp[(funcs[size][f], size)]:
                    #plota a temperatura de uma dada função só uma vez
                    FileHandler.plot_temps(filename, funcs[size][f])
                    plotTemp[(funcs[size][f], size)] = True

if __name__ == "__main__":
    main()
