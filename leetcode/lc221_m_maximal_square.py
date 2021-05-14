from typing import List 

class Solution:
    def integralImage(self, M):
        m = len(M)
        n = len(M[0])
        A = [[0 for _ in range(n)] for _ in range(m)]
        A [0][0] = M[0][0]
        for i in range(1, n):
            A[0][i] = A[0][i - 1] + M[0][i]
        
        for i in range(1, m):
            A[i][0] = A[i - 1][0] + M[i][0]
        
        for i in range(1, m):
            for j in range(1, n):
                A[i][j] = M[i][j] + A[i - 1][j] + A[i][j - 1] - A[i - 1][j - 1] 
        
        return A
        
    def maximalSquare(self, matrix: List[List[str]]) -> int:        
        M = [[int(s) for s in row] for row in matrix]
        m = len(M)
        n = len(M[0])        
        A = self.integralImage(M) 
        for r in A: print(r)
        sqsum = float('-inf')
        for i in range(m):
            for j in range(n):
                for s in range(min(m - i, n - j)):                    

                    k, l = i + s, j + s      
                    if s == 0:
                        S = M[i][j]
                    elif i == 0 and j == 0:
                        S = A[k][l]                        
                    elif i >= 1 and j >= 1:
                        S = A[k][l] + A[i - 1][j - 1] - A[i - 1][l] - A[k][j - 1]
                    elif i == 0 and j >= 1:
                        S = A[k][l] - A[k][j - 1]
                    elif j == 0 and i >= 1:
                        S = A[k][l] - A[i - 1][l]         
                        
                    if S < (s + 1) ** 2:
                        break                        
                    else:
                        sqsum = max(sqsum, S)
        return 0 if sqsum == float('-inf') else sqsum

def main():
    sol = Solution()
    M = [["1", "1"], ["1", "1"]]
    print(sol.maximalSquare(M))

if __name__ == '__main__':
    main()