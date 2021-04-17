from typing import List

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m = len(matrix)
        n = len(matrix[0])

        # row matrix
        if m == 1:
            return [matrix[0][j] for j in range(n)]

        # Column matrix
        if n == 1:
            return [matrix[i][0] for i in range(m)]

        K = min(m, n)
        if K % 2 == 0:
            numshells = K // 2
        else:
            numshells = (K + 1) // 2

        elems = []
        mincol, maxcol = 0, n - 1
        minrow, maxrow = 0, m - 1
        k = 0
        while k < numshells:
            # l -> r
            for j in range(mincol, maxcol + 1):
                elems.append(matrix[minrow][j])

            # t -> b
            for i in range(minrow + 1, maxrow + 1):
                elems.append(matrix[i][maxcol])

            # l <- r
            if maxrow > minrow:
                for j in range(maxcol - 1, mincol - 1, -1):
                    elems.append(matrix[maxrow][j])

            # b to t
            if maxcol > mincol:
                for i in range(maxrow - 1, minrow, -1):
                    elems.append(matrix[i][mincol])

            k += 1
            minrow += 1
            maxrow -= 1
            mincol += 1
            maxcol -= 1

        return elems

def main():
    matrix = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15], [16,17,18,19,20], [21,22,23,24,25]]
    sol = Solution()
    elems = sol.spiralOrder(matrix)
    print(elems)

if __name__ == '__main__':
    main()
