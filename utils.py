import random

def embaralhar_tabuleiro(tabuleiro_resolvido, movimentos=100):
    direcoes = ['C', 'B', 'E', 'D']
    atual = tabuleiro_resolvido
    for _ in range(movimentos):
        direcao = random.choice(direcoes)
        novo = mover(atual, direcao)
        if novo:
            atual = novo
    return atual

def mover(estado, direcao):
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                x, y = i, j
                break
    estado_lista = [list(linha) for linha in estado]
    if direcao == 'C' and x < 2:
        estado_lista[x][y], estado_lista[x+1][y] = estado_lista[x+1][y], estado_lista[x][y]
    elif direcao == 'B' and x > 0:
        estado_lista[x][y], estado_lista[x-1][y] = estado_lista[x-1][y], estado_lista[x][y]
    elif direcao == 'E' and y < 2:
        estado_lista[x][y], estado_lista[x][y+1] = estado_lista[x][y+1], estado_lista[x][y]
    elif direcao == 'D' and y > 0:
        estado_lista[x][y], estado_lista[x][y-1] = estado_lista[x][y-1], estado_lista[x][y]
    else:
        return None
    return tuple(tuple(linha) for linha in estado_lista)
