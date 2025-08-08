from pysat.solvers import Glucose3

OBJETIVO = ((0, 1, 2), (3, 4, 5), (6, 7, 8))

class Puzzle8:
    def __init__(self, estado_inicial):
        self.estado_inicial = estado_inicial
        self.solver = Glucose3()
        self.variaveis = {}
        self.contador_variavel = 1

    def nova_variavel(self):
        var = self.contador_variavel
        self.contador_variavel += 1
        return var

    def get_variavel(self, nome):
        if nome not in self.variaveis:
            self.variaveis[nome] = self.nova_variavel()
        return self.variaveis[nome]

    def posicao_vazia(self, estado):
        for i in range(3):
            for j in range(3):
                if estado[i][j] == 0:
                    return i, j

    def mover(self, estado, direcao):
        i, j = self.posicao_vazia(estado)
        novo_estado = [list(linha) for linha in estado]

        if direcao == 'C' and i < 2:
            novo_estado[i][j], novo_estado[i + 1][j] = novo_estado[i + 1][j], novo_estado[i][j]
        elif direcao == 'B' and i > 0:
            novo_estado[i][j], novo_estado[i - 1][j] = novo_estado[i - 1][j], novo_estado[i][j]
        elif direcao == 'E' and j < 2:
            novo_estado[i][j], novo_estado[i][j + 1] = novo_estado[i][j + 1], novo_estado[i][j]
        elif direcao == 'D' and j > 0:
            novo_estado[i][j], novo_estado[i][j - 1] = novo_estado[i][j - 1], novo_estado[i][j]
        else:
            return None
        return tuple(tuple(linha) for linha in novo_estado)

    def codificar_estado(self, estado, passo):
        for i in range(3):
            for j in range(3):
                for k in range(9):
                    nome = f"x_{passo}_{i}_{j}_{k}"
                    var = self.get_variavel(nome)
                    if estado[i][j] == k:
                        self.solver.add_clause([var])
                    else:
                        self.solver.add_clause([-var])

    def decodificar_modelo(self, modelo, passo):
        estado = [[-1] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                for k in range(9):
                    var = self.get_variavel(f"x_{passo}_{i}_{j}_{k}")
                    if var in modelo:
                        estado[i][j] = k
        return tuple(tuple(linha) for linha in estado)

    def resolver(self, maximo_passos=15):
        visitados = {self.estado_inicial}
        caminhos = {self.estado_inicial: []}
        fila = [(self.estado_inicial, 0)]

        while fila:
            estado_atual, passo = fila.pop(0)

            if estado_atual == OBJETIVO:
                return caminhos[estado_atual]

            if passo >= maximo_passos:
                continue

            for direcao in ['C', 'B', 'E', 'D']:
                novo_estado = self.mover(estado_atual, direcao)
                if novo_estado and novo_estado not in visitados:
                    visitados.add(novo_estado)
                    caminhos[novo_estado] = caminhos[estado_atual] + [direcao]
                    fila.append((novo_estado, passo + 1))
        return None
