from contextlib import redirect_stdout

with redirect_stdout(None):
    # Omitindo a mensagem de boas vindas do pygame
    import pygame #pip install pygame
    from pygame.locals import *

width, height = 756, 672
DISPLAY = None

def init_window(ALGORITHM:str, index:int):
    """
    Inicializa a janela do pygame
    """
    pygame.init()
    global DISPLAY
    DISPLAY = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption(f"{ALGORITHM} Execução {index+1}")

def draw(simulationMap:list, itemList:list, factoryList:list, robot=None):
    """
    Desenha o mapa da simulação, os itens, as fábricas e o robô, se estes foram fornecidos
    """
    pos_x = 0 # linha onde vai desenhar
    for x in range(42):
        pos_y = 0 # coluna onde vai desenhar
        for y in range(42):
            Color = simulationMap[x][y].color
            # desenhando as células do mapa)
            pygame.draw.rect(DISPLAY, Color, (18*pos_x, 16*pos_y, 18, 16))
            pos_y += 1
        pos_x += 1

    for item in itemList: # desenhando os itens
        pygame.draw.circle(DISPLAY, item.color, ((18*item.position[0])+9, (16*item.position[1])+8), 5)
        pygame.draw.circle(DISPLAY, (0,0,0),    ((18*item.position[0])+9, (16*item.position[1])+8), 5, 1)

    for factory in factoryList: # desenhando as fábricas
        pygame.draw.rect(DISPLAY, factory.color, ((18*factory.position[0])+3, (16*factory.position[1])+2, 14, 12))
        pygame.draw.rect(DISPLAY, (0,0,0),       ((18*factory.position[0])+3, (16*factory.position[1])+2, 14, 12), 1)

    # desenhando o robô, se ele foi fornecido
    if robot != None:
        pygame.draw.rect(DISPLAY, (255,255,255), ((18*robot.position[0])+3, (16*robot.position[1])+2, 14, 12))
        pygame.draw.rect(DISPLAY, (0,0,0),       ((18*robot.position[0])+3, (16*robot.position[1])+2, 14, 12), 2)
        
    for x in range(0,756,18): # desenhando linhas verticais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (x, 0), (x, height))
    for y in range(0,672,16): # desenhando linhas horizontais separadoras
        pygame.draw.line(DISPLAY, (64,64,64), (0, y), (width, y))

def draw_colored_border(border:list, color:tuple=None):
    """
    Desenha uma borda de cor fornecida ao redor das células na lista fornecida
    Caso nenhuma cor seja fornecida, desenha uma borda branca
    """
    color = (255,255,255) if color == None else color
    for target in border:
        pygame.draw.line(DISPLAY, color, ((18*target[0])+18, (16*target[1])+16), ((18*target[0]),    (16*target[1])+16))
        pygame.draw.line(DISPLAY, color, ((18*target[0])+18, (16*target[1])+16), ((18*target[0])+18, (16*target[1])))
        pygame.draw.line(DISPLAY, color, ((18*target[0])+18, (16*target[1])),    ((18*target[0]),    (16*target[1])))
        pygame.draw.line(DISPLAY, color, ((18*target[0]),    (16*target[1])+16), ((18*target[0]),    (16*target[1])))

def save(filename:str) -> None:
    pygame.image.save(DISPLAY , "Imagens/"+filename)