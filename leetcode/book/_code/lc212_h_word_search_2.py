from typing import List 

class Solution:
    def dfs(self, board, word, i, j, k, visited):
        m = len(board)
        n = len(board[0])
        w = len(word)
        if k == w:
            return True

        nbrs = [(i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j)]
        found = False
        for r, c in nbrs:
            if (0 <= r <= m - 1) and (0 <= c <= n - 1):
                if (not (r, c) in visited) and (board[r][c] == word[k]):
                    nv = visited.union({(r, c)})
                    found = found or self.dfs(board, word, r, c, k + 1, nv)

        return found
            
        
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        found_words = []
        m = len(board)
        n = len(board[0])
        
        for word in words:
            if set(word).difference()
            positions = [(i, j) for i in range(m) for j in range(n) if board[i][j] == word[0]]
            for i, j in positions:
                if self.dfs(board, word, i, j, 1, {(i, j)}):
                    found_words.append(word)
                    break
                    
        return found_words                    