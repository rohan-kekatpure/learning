from typing import List

class Solution:
    def isvalid(self, block):
        dct = dict.fromkeys(range(1, 10), 0)
        for digit in block:
            if digit == '.':
                continue
            try:
                digit = int(digit)
            except ValueError:
                return False

            if not (1 <= digit <= 9):
                return False

            dct[digit] += 1
            if dct[digit] > 1:
                return False

        return True

    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # Rows
        for row in board:
            if not self.isvalid(row):
                return False

        # Columns
        for col in range(9):
            column = [row[col] for row in board]
            if not self.isvalid(column):
                return False

        # 3x3 blocks
        for row in [0, 3, 6]:
            for col in [0, 3, 6]:
                block = [board[row + i][col + j] for i in range(3) for j in range(3)]
                if not self.isvalid(block):
                    return False
        return True


