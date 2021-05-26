class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        if numRows == 1:
            return [[1]]
        
        if numRows == 2:
            return [[1], [1, 1]]
        
        res = [[1], [1, 1]]
        for n in range(2, numRows):
            r = res[-1]
            s = [r[i] + r[i + 1] for i in range(len(r) - 1)]
            s = [1] + s + [1]
            res.append(s)
        return res