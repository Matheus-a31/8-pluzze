import tkinter as tk
from tkinter import font
from puzzle import Puzzle8
from utils import embaralhar_tabuleiro

OBJETIVO = ((0, 1, 2), (3, 4, 5), (6, 7, 8))

class InterfacePuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle com SAT")
        self.tabuleiro = embaralhar_tabuleiro(OBJETIVO)
        self.botoes = [[None for _ in range(3)] for _ in range(3)]
        self.fonte = font.Font(size=20, weight='bold')
        self.criar_interface()
        self.atualizar_tabuleiro()

    def criar_interface(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, width=4, height=2, font=self.fonte)
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.botoes[i][j] = btn

        self.botao_resolver = tk.Button(self.root, text="Resolver", command=self.resolver_puzzle)
        self.botao_resolver.grid(row=3, column=0, columnspan=3, pady=10)

    def atualizar_tabuleiro(self):
        for i in range(3):
            for j in range(3):
                valor = self.tabuleiro[i][j]
                btn = self.botoes[i][j]
                btn.config(text=str(valor) if valor != 0 else "", bg="white")

    def resolver_puzzle(self):
        puzzle = Puzzle8(self.tabuleiro)
        passos = puzzle.resolver(maximo_passos=30)
        if passos:
            self.mostrar_passos(passos)
        else:
            print("Sem solução encontrada.")

    def mostrar_passos(self, passos):
        def proximo_passo():
            nonlocal passos
            if not passos:
                return
            direcao = passos.pop(0)
            self.tabuleiro = self.mover_interface(self.tabuleiro, direcao)
            self.atualizar_tabuleiro()
            self.root.after(500, proximo_passo)

        self.root.after(500, proximo_passo)

    def mover_interface(self, estado, direcao):
        for i in range(3):
            for j in range(3):
                if estado[i][j] == 0:
                    x, y = i, j
        estado_lista = [list(linha) for linha in estado]
        if direcao == 'C' and x < 2:
            estado_lista[x][y], estado_lista[x+1][y] = estado_lista[x+1][y], estado_lista[x][y]
        elif direcao == 'B' and x > 0:
            estado_lista[x][y], estado_lista[x-1][y] = estado_lista[x-1][y], estado_lista[x][y]
        elif direcao == 'E' and y < 2:
            estado_lista[x][y], estado_lista[x][y+1] = estado_lista[x][y+1], estado_lista[x][y]
        elif direcao == 'D' and y > 0:
            estado_lista[x][y], estado_lista[x][y-1] = estado_lista[x][y-1], estado_lista[x][y]
        return tuple(tuple(linha) for linha in estado_lista)
