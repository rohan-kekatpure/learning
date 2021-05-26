from typing import List

class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        numshells = n // 2
        i = 1
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for k in range(numshells):
            startrow = startcol = k
            endrow = endcol = (n - 1) - k  # inclusive

            # Top row
            for c in range(startcol, endcol + 1):
                matrix[startrow][c] = i
                i += 1

            # Right column
            for r in range(startrow + 1, endrow + 1):
                matrix[r][endcol] = i
                i += 1

            # Bottom row
            for c in range(endcol - 1, startcol - 1, -1):
                matrix[endrow][c] = i
                i += 1

            # Left column
            for r in range(endrow - 1, startrow, -1):
                matrix[r][startcol] = i
                i += 1

        # For odd n, fill the single center element
        if n % 2 == 1:
            rmid = cmid = n // 2
            matrix[rmid][cmid] = i

        return matrix

def main():
    sol = Solution()
    m = sol.generateMatrix(1)
    for r in m:
        print(r)

if __name__ == '__main__':
    main()
