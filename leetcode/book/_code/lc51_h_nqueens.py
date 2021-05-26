from typing import List
from copy import deepcopy

class Solution:
    def check(self, board, row, col, n):
        # Row check
        for c in range(col):
            if board[row][c] == 'Q':
                return False

        for c in range(col):
            for r in range(n):
                # 45 degree diag
                if (r + c == row + col) and (board[r][c] == 'Q'):
                    return False

                # 135 degree diag
                if (r - c == row - col) and (board[r][c] == 'Q'):
                    return False

        return True

    def helper(self, board, col, n):
        if col == n:
            yield deepcopy(board)

        for row in range(n):
            if self.check(board, row, col, n):
                board[row][col] = 'Q'
                yield from self.helper(board, col + 1, n)

            if col < n:
                board[row][col] = '.'

    def solveNQueens(self, n: int) -> List[List[str]]:
        board = [['.' for _ in range(n)] for _ in range(n)]
        gen = self.helper(board, 0, n)
        for sol in gen:
            print(sol)

        # solutions = []
        # for sol in gen:
        #     l = [''.join(r) for r in sol]
        #     solutions.append(l)
        # return solutions

