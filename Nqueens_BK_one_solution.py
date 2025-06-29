import time
from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        # Cols, positive and negative diagonals used for O(1) checks
        col = set()
        posDiag = set()
        negDiag = set()
        board = [["."] * n for _ in range(n)]
        res: List[List[str]] = []

        def backtrack(r: int) -> bool:
            # If all rows are placed, capture solution and stop
            if r == n:
                res.append(["".join(row) for row in board])
                return True

            for c in range(n):
                if c in col or (r + c) in posDiag or (r - c) in negDiag:
                    continue

                # Place queen
                col.add(c)
                posDiag.add(r + c)
                negDiag.add(r - c)
                board[r][c] = "Q"

                # Recurse; if found, unwind immediately
                if backtrack(r + 1):
                    return True

                # Remove queen (backtrack)
                board[r][c] = "."
                col.remove(c)
                posDiag.remove(r + c)
                negDiag.remove(r - c)

            return False

        backtrack(0)
        return res


def main() -> None:
    with open(r'tempos_execucao_backtracking_unico1.txt', 'w') as arquivo:
        arquivo.write("N,Tempo(segundos)\n")
        for N in range(4, 50):
            solver = Solution()
            inicio = time.time()
            sol = solver.solveNQueens(N)
            fim = time.time()

            tempo_execucao = fim - inicio
            arquivo.write(f"{N},{tempo_execucao:.6f}\n")
            print(f"N = {N}: {len(sol)} solução encontrada em {tempo_execucao:.4f} segundos")

if __name__ == "__main__":
    main()
