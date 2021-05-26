class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        if rowIndex == 0: return [1]
        if rowIndex == 1: return [1, 1]
        row = [1, 1]
        n = 2
        while n <= rowIndex:
            newrow = [row[i] + row[i + 1] for i in range(len(row) - 1)]
            newrow = [1] + newrow + [1]            
            n += 1
            row = newrow
        return row
        