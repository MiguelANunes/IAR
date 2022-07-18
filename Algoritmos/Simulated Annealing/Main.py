import Logic, FileHandler
from Functions import *
from time import time
#from contextlib import redirect_stdout

# TODO: https://stackoverflow.com/questions/68960005/saving-an-animated-matplotlib-graph-as-a-gif-file-results-in-a-different-looking

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

    funcs           = {51: {func6:"func6", func7:"func7", func9:"func9"}, 100: {func6:"func6", func7:"func7", func9:"func9"}}

    bestCosts       = {51: (10**6, "x", -1), 100: (10**6, "x", -1)}
    bestPath        = {51: None, 100: None}
    
    plotTemp        = {(name, size): False for size,funs in funcs.items() for _, name in  funs.items()}
    times           = {(name, size): [] for size in [51, 100] for _,funs in funcs.items() for _, name in  funs.items()}
    finalResults    = {(name, size): [] for size in [51, 100] for _,funs in funcs.items() for _, name in  funs.items()}

    for size in [51, 100]:
        nodes, distances = FileHandler.initialize(size)
        print(f"Tamanho {size}")
        for test in range(10):
            
            print(f"\tTeste {test}")
            for f in funcs[size]:

                print(f"\t\t{funcs[size][f]}:", end=" ")

                params             = get_best_param(size, funcs[size][f])
                params["func"]     = f
                params["funcName"] = funcs[size][f]
                
                start                  = time()
                results                = Logic.simulated_annealing(nodes, distances, params)
                end                    = time()
                costs                  = results["costs"]
                temps                  = results["temps"]
                iters                  = results["iters"]
                bestCost, bestSolution = results["bestResult"]
                # probs                = results["probs"]

                print(f"{bestCost:.3f}")
                print(f"\t\tTempo Gasto: {end-start:.3f}")
                
                times[(funcs[size][f], size)].append(end-start)
                finalResults[(funcs[size][f], size)].append(bestCost)

                if bestCost <= bestCosts[size][0]:
                    bestCosts[size] = (bestCost, funcs[size][f], test)
                    bestPath[size]  = bestSolution

                FileHandler.dump_params(size, params, bestCost)
                FileHandler.dump_values(costs, temps, iters)
                # FileHandler.dump_probs(probs)

                filename = str(size)+funcs[size][f]+"-"+str(test)
                FileHandler.plot_costs(filename, test)
                if not plotTemp[(funcs[size][f], size)]:
                    #plota a temperatura de uma dada função só uma vez
                    FileHandler.plot_temps(filename, funcs[size][f])
                    plotTemp[(funcs[size][f], size)] = True


    FileHandler.dump_times        (times)
    FileHandler.dump_final_results(finalResults)
    FileHandler.dump_best         (bestCosts)

    print(f"Melhor caso 51: {bestCosts[51]}")
    print(f"Melhor caso 100: {bestCosts[100]}")

if __name__ == "__main__":
    main()
