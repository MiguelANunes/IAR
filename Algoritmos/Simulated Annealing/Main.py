import Logic, FileHandler
from Functions import *

# TODO: Passar definição de parametros para uma outra função
#   Recebe o nome da função que vai executar, retornar os parametros ideais dessa função
#   Já tenhos os ideias para a função 6, arranjar outras duas para fazer isso

# TODO: Lidar com o caso de 100 nós

def main() -> None:
    """
    Função principal do SA
    Gera os nós e suas distâncias e inicia o loop principal do SA
    """
    print("Valor ótimo para 51:   426")
    print("Valor ótimo para 100:  21_282")

    funcs    = {func6:"func6", func3:"func3"}
    plotTemp = {"func6": False, "func3":False}

    for size in [51]:
        nodes, distances = FileHandler.initialize(size)
        print(f"Tamanho {size}")
        for index in range(10):
            
            print(f"\tTeste {index}")
            for f in funcs:

                print(f"\t\t{funcs[f]}:", end=" ")

                params             = get_best_param(size, funcs[f])
                params["func"]     = f
                params["funcName"] = funcs[f]

                results   = Logic.simulated_annealing(nodes, distances, params)
                costs     = results["costs"]
                temps     = results["temps"]
                iters     = results["iters"]
                finalCost = results["finalCost"]
                # probs = results["probs"]

                print(f"{finalCost}")

                FileHandler.dump_params(params, finalCost)
                FileHandler.dump_values(costs, temps, iters)
                # FileHandler.dump_probs(probs)

                filename = str(size)+funcs[f]+"-"+str(index)
                FileHandler.plot_costs(filename)
                if not plotTemp[funcs[f]]:
                    # vai plotar a temperatura de uma dada função só uma vez
                    FileHandler.plot_temps(filename)
                    plotTemp[funcs[f]] = True
                # FileHandler.plot_probs(filename)

if __name__ == "__main__":
    main()
