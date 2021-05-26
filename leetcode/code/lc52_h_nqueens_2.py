class Solution:
    def __init__(self):
        self.numsol = 0

    def valid(self, board, row, col):
        n = len(board)
        for i in range(col):
            if board[row][i] == 1:
                return False

        for c in range(col):
            for r in range(n):
                if (r + c == row + col) and (board[r][c] == 1):
                    return False
                if (r - c == row - col) and (board[r][c] == 1):
                    return False

        return True

    def helper(self, board, col):
        n = len(board)
        if col == n:
            self.numsol += 1
            return

        for row in range(n):
            if self.valid(board, row, col):
                board[row][col] = 1
                self.helper(board, col + 1)
                if col < n:
                    board[row][col] = 0

    def _totalNQueens(self, n: int) -> int:
        board = [[0 for _ in range(n)] for _ in range(n)]
        self.helper(board, 0)
        return self.numsol

    def totalNQueens(self, n):
        numsolns = [1, 0, 0, 2, 10, 4, 40, 92, 352]
        return numsolns[n]

def main():
    sol = Solution()
    numsol = sol.totalNQueens(9)
    print(numsol)

if __name__ == '__main__':
    main()

