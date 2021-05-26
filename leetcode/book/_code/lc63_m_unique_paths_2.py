from typing import List

class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])
        T = [[0 for _ in range(n)] for _ in range(m)]

        if obstacleGrid[0][0] != 1:
            T[0][0] = 1

        for i in range(1, m):
            if obstacleGrid[i][0] == 1:
                T[i][0] = 0
            else:
                T[i][0] = T[i - 1][0]

        for j in range(1, n):
            if obstacleGrid[0][j] == 1:
                T[0][j] = 0
            else:
                T[0][j] = T[0][j - 1]

        for i in range(1, m):
            for j in range(1, n):
                if obstacleGrid[i][j] == 1:
                    T[i][j] = 0
                else:
                    T[i][j] = T[i - 1][j] + T[i][j - 1]

        return T[m - 1][n - 1]

