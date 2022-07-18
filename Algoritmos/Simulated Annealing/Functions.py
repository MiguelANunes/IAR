from math import exp, log, cos, cosh, tanh, pi

def func0(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """Função de resfriamento 0"""
    return startTemp - (curIter * ((startTemp - finalTemp)/maxIter))

def func1(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """Função de resfriamento 1"""
    return startTemp * ((finalTemp/startTemp)**(curIter/maxIter))

def func2(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """Função de resfriamento 2"""
    a = ((startTemp - finalTemp) * (maxIter + 1))/maxIter
    return (a/(curIter+1))+ (startTemp - a)

def func3(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """Função de resfriamento 3"""
    a = log(startTemp - finalTemp)/log(maxIter)
    return startTemp - curIter**a

def func4(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """Função de resfriamento 4"""
    return ((startTemp-finalTemp)/(1+exp(0.3*(curIter-(maxIter/2))))) + finalTemp

def func5(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """Função de resfriamento 5"""
    return (0.5*(startTemp-finalTemp)*(1+cos((curIter*pi)/maxIter))) + finalTemp

def func6(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """Função de resfriamento 6"""
    return 0.5*(startTemp-finalTemp)*(1-tanh((10.0*curIter/maxIter)-5.0)) + finalTemp

def func7(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """Função de resfriamento 7"""
    return ((startTemp-finalTemp)/cosh((10*curIter)/maxIter))+finalTemp

def func8(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """Função de resfriamento 8"""
    a = -1*((curIter/maxIter)*log(startTemp/finalTemp))
    return startTemp*exp(a*curIter)

def func9(startTemp: int, curIter: int, finalTemp:int, maxIter:int) -> float:
    """Função de resfriamento 9"""
    a = -1*((1/maxIter**2)*log(startTemp/finalTemp))
    return startTemp*exp(a*curIter**2)

def get_best_param(size:int, funcName:str) -> dict:
    """
    Dado o tamanho de uma instância 
    """
    bestParams = dict()

    if size == 51:
        # Caso 51 nós
        # bestParams["func3"] = {"metropolis":5, "startTemp":200_000,  "finalTemp":0, "maxIter":100}
        # bestParams["func4"] = {"metropolis":5, "startTemp":1_000_00, "finalTemp":0, "maxIter":4730}
        bestParams["func6"] = {"metropolis":10, "startTemp":100,       "finalTemp":0, "maxIter":30_000}
        bestParams["func7"] = {"metropolis":10, "startTemp":1000,      "finalTemp":0, "maxIter":30_000}
        bestParams["func9"] = {"metropolis":20, "startTemp":1_000_000, "finalTemp":1, "maxIter":20_000}
    else:   
        # Caso 100 nós
        bestParams["func6"] = {"metropolis":30, "startTemp":15_000,    "finalTemp":0, "maxIter":200_000}
        bestParams["func7"] = {"metropolis":30, "startTemp":100_000,   "finalTemp":0, "maxIter":200_000}
        bestParams["func9"] = {"metropolis":30, "startTemp":1_000_000, "finalTemp":1, "maxIter":200_000}
    
    return bestParams[funcName]