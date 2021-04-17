from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m = len(matrix)
        n = len(matrix[0])

        if (target < matrix[0][0]) or (target > matrix[m - 1][n - 1]):
            return False

        # search row
        rtop, rbot = 0, m - 1
        rmid = 0
        while rtop <= rbot:
            rmid = (rtop + rbot) // 2
            if (matrix[rmid][0] == target) or (matrix[rmid][n - 1] == target):
                return True
            elif matrix[rmid][0] < target < matrix[rmid][n - 1]:
                break
            elif matrix[rmid][0] > target:
                rbot = rmid - 1
            elif matrix[rmid][n - 1] < target:
                rtop = rmid + 1

        # Search column
        cleft, cright = 0, n - 1
        while cleft <= cright:
            cmid = (cleft + cright) // 2
            if matrix[rmid][cmid] == target:
                return True
            elif matrix[rmid][cmid] > target:
                cright = cmid - 1
            else:
                cleft = cmid + 1

        return False

    def searchMatrix2(self, matrix: List[List[int]], target: int) -> bool:
        m = len(matrix)
        n = len(matrix[0])
        arr = [matrix[i][j] for i in range(m) for j in range(n)]
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return True
            elif arr[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        return False

def main():
    sol = Solution()
    res = sol.searchMatrix([[1]], 2)
    print(res)

if __name__ == '__main__':
    main()
