from typing import List 

class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        n = len(triangle) - 1        
        tot = triangle[n]
        while n > 0:
            row = triangle[n - 1]
            newtot = []
            for i in range(len(row)):
                newtot.append(row[i] + min(tot[i], tot[i + 1]))
            tot = newtot
            n -= 1
        return tot[0]

