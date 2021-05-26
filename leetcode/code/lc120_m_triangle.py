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

def main():
    sol = Solution()
    triangle = [[2],[3,4],[6,5,7],[4,1,8,3], [7, 1, 2, 4, -99]]
    minsum = sol.minimumTotal(triangle)
    print(minsum)

if __name__ == '__main__':
    main()