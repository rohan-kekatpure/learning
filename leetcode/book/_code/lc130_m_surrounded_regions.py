class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        
        """
        Algorithm
        
        We will do BFS from all boundary cells and mark the 
        all 'O' cells that can be reached from the boundary.
        The remaining 'O' cells can be marked with 'X'
        """
        visited = set()
        queue = []
        
        m = len(board)
        n = len(board[0])
    
        # Initial population of queue
        for i in range(m):
            if board[i][0] == 'O':
                queue.insert(0, (i, 0))
            if board[i][n - 1] == 'O':
                queue.insert(0, (i, n - 1))
        
        for j in range(n):
            if board[0][j] == 'O':
                queue.insert(0, (0, j))
            if board[m - 1][j] == 'O':
                queue.insert(0, (m - 1, j))
            
        while queue:
            i, j = queue.pop()
            nextpos = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
            for ni, nj in nextpos:
                if (0 <= ni < m) and (0 <= nj < n) and board[ni][nj] == 'O':
                    if not (ni, nj) in visited:
                        queue.insert(0, (ni, nj))
            
            visited.add((i, j))
        
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'O' and (not (i, j) in visited):
                    board[i][j] = 'X'
        
            