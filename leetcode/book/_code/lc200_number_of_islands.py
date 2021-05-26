from typing import List

class Solution:
    def bfs(self, grid, r, c, visited):
        m = len(grid)
        n = len(grid[0])        
        queue = [(r, c)]        
        while queue:
            i, j = queue.pop()
            visited.add((i, j))            
            nbrs = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]
            for p, q in nbrs:
                if (0 <= p < m ) and (0 <= q < n):
                    if (grid[p][q] == '1') and (not (p, q) in visited):                        
                        queue.append((p, q))
        
                    
    def numIslands(self, grid: List[List[str]]) -> int:
        m = len(grid)
        n = len(grid[0])
        visited = set()
        num_islands = 0
        for i in range(m):
            for j in range(n):
                if (grid[i][j] == '1') and (not (i, j) in visited):
                    self.bfs(grid, i, j, visited)
                    num_islands += 1
                    
        return num_islands

