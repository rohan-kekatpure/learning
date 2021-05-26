from typing import List

class Solution:
    def walk(self, board, word, i, j, k, visited):
        m = len(board)
        n = len(board[0])
        w = len(word)
        if k == w:
            return True

        nbrs = [(i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j)]
        found = False
        for r, c in nbrs:
            if (0 <= r <= m - 1) \
               and (0 <= c <= n - 1) \
               and (not (r, c) in visited) \
               and (board[r][c] == word[k]):
                found = found or self.walk(board, word, r, c, k + 1, visited + [(r, c)])

        return found

    def exist(self, board: List[List[str]], word: str) -> bool:
        m = len(board)
        n = len(board[0])

        for i in range(m):
            for j in range(n):
                if board[i][j] == word[0]:
                    if self.walk(board, word, i, j, 1, [(i, j)]):
                        return True
        return False

