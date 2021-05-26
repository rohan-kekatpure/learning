from typing import List

class Solution:
    def maximalRectangle(self, matrix) -> int:
        m = len(matrix)
        n = len(matrix[0])
        for i in range(m):
            for j in range(n):
                matrix[i][j] = int(matrix[i][j])

        udcounts = [[0 for _ in range(n)] for _ in range(m)]
        lrcounts = [[0 for _ in range(n)] for _ in range(m)]
        udcounts[0][0] = lrcounts[0][0] = matrix[0][0]
        for j in range(1, n):
            udcounts[0][j] = matrix[0][j]

        for i in range(1, m):
            lrcounts[i][0] = matrix[i][0]

        # Up down
        for i in range(1, m):
            for j in range(n):
                if matrix[i][j] == 0:
                    udcounts[i][j] = 0
                else:
                    udcounts[i][j] = udcounts[i - 1][j] + 1

        # Left right
        for i in range(m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    lrcounts[i][j] = 0
                else:
                    lrcounts[i][j] = lrcounts[i][j - 1] + 1


        maxarea = 0
        for i in range(m):
            for j in range(n):
                cud = udcounts[i][j]
                clr = lrcounts[i][j]
                val = max(cud, clr, cud * clr)
                maxarea = max(maxarea, val)

        from IPython import embed; embed(); exit(0)
        return maxarea

def main():
    matrix = [["1", "0", "1", "0", "0"],
              ["1", "0", "1", "1", "1"],
              ["1", "1", "1", "1", "1"],
              ["1", "0", "0", "1", "0"]]

    sol = Solution()
    ans = sol.maximalRectangle(matrix)
    print(ans)


if __name__ == '__main__':
    main()
