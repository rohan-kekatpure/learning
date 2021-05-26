class Solution1:
    """ backtracking """
    def __init__(self):
        self.num_solutions = 0

    def helper(self, row, col, m, n):
        if (row == m - 1) and (col == n - 1):
            self.num_solutions += 1

        if row < m - 1:
            self.helper(row + 1, col, m, n)
        if col < n - 1:
            self.helper(row, col + 1, m, n)

    def uniquePaths(self, m: int, n: int) -> int:
        self.helper(0, 0, m, n)
        return self.num_solutions

class Solution2:
    def uniquePaths(self, m, n):
        T = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            T[i][0] = 1
        for j in range(n):
            T[0][j] = 1

        for i in range(1, m):
            for j in range(1, n):
                T[i][j] = T[i - 1][j] + T[i][j - 1]

        return T[m - 1][n - 1]

