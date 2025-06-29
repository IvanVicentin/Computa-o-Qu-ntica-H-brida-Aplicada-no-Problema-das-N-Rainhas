import time
from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        col = set()
        posDiag = set()
        negDiag = set()
        res = []
        board = [["."] * n for _ in range(n)]

        def backtrack(r: int) -> None:
            if r == n:
                copy = ["".join(row) for row in board]
                res.append(copy)
                return

            for c in range(n):
                if c in col or (r + c) in posDiag or (r - c) in negDiag:
                    continue

                col.add(c)
                posDiag.add(r + c)
                negDiag.add(r - c)
                board[r][c] = "Q"

                backtrack(r + 1)

                col.remove(c)
                posDiag.remove(r + c)
                negDiag.remove(r - c)
                board[r][c] = "."

        backtrack(0)
        return res

def main() -> None:
    with open(r'C:\Users\ivana\Documents\Estudo\Quantum Annealing\BK\tempos_execucao_backtracking.txt', 'w') as arquivo:
        arquivo.write("N,Tempo(segundos)\n")
        
        for N in range(4, 20):
            solver = Solution()
            inicio = time.time()
            solutions = solver.solveNQueens(N)  # Armazena as soluções
            fim = time.time()
            
            tempo_execucao = fim - inicio
            num_solucoes = len(solutions)  # Conta as soluções
            
            arquivo.write(f"{N},{tempo_execucao}\n")
            print(f"N = {N}: {num_solucoes} soluções encontradas em {tempo_execucao:.4f} segundos")

if __name__ == "__main__":
    main()