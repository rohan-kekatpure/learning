class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows < 2: return s

        rows = [[] for _ in range(numRows)]

        i = 0
        incr = 1
        for c in s:
            rows[i].append(c)
            if i == 0:
                incr = 1
            if i == numRows - 1:
                incr = -1
            i += incr

        res = ''
        for r in rows:
            res += ''.join(r)
        return res

