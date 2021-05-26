from typing import List

def checkvalid(board, row, col, digit):
    for i in range(9):
        if (board[i][col] == digit) or (board[row][i] == digit): return False
    r0 = (row // 3) * 3
    c0 = (col // 3) * 3
    block = [board[r0 + i][c0 + j] for i in range(3) for j in range(3)]
    if digit in block: return False
    return True

class Solution1:
    def __init__(self):
        self.solved = False

    def sudokuHelper(self, board, positions, idx, digit):
        i, j = positions[idx]
        if not checkvalid(board, i, j, digit):
            return
        board[i][j] = digit

        # Base case
        if idx == len(positions) - 1:
            self.solved = True
            return

        d = 1
        while d <= 9 and (not self.solved):
            self.sudokuHelper(board, positions, idx + 1, str(d))
            d += 1

        if not self.solved:
            pi, pj = positions[idx + 1]
            board[pi][pj] = '.'

    def solveSudoku(self, board):
        positions = [(row, col) for row in range(9) for col in range(9) if board[row][col] == '.']
        for d in range(1, 10):
            if not self.solved:
                self.sudokuHelper(board, positions, 0, str(d))

class Solution2:
    def __init__(self):
        self.solved = False

    def sudokuHelper(self, board, positions, idx):
        if idx == len(positions):
            self.solved = True
            return

        i, j = positions[idx]
        for d in list('123456789'):
            if self.solved: return
            if not checkvalid(board, i, j, d): continue
            board[i][j] = d
            self.sudokuHelper(board, positions, idx + 1)

        if not self.solved:
            board[i][j] = '.'

    def solveSudoku(self, board):
        positions = [(row, col) for row in range(9) for col in range(9) if board[row][col] == '.']
        self.sudokuHelper(board, positions, 0)


def printboard(board):
    print('\n')
    for r in board:
        print(r)

def main():
    board = [
        ["4",".",".",".",".",".",".",".","7"],
        [".","1",".",".","6",".",".","3","."],
        [".",".","5","4",".","2","1",".","."],
        [".",".","8","1",".","3","7",".","."],
        [".","3",".",".",".",".",".","8","."],
        [".",".","4","9",".","8","2",".","3"],
        [".",".","7","3",".","9","6",".","."],
        [".","4",".",".","1",".",".","9","."],
        ["3",".",".",".",".",".",".",".","2"]
    ]

    sol = Solution1()
    sol.solveSudoku(board)
    printboard(board)

if __name__ == '__main__':
    main()

