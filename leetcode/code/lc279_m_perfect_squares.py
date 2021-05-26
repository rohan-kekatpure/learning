from math import sqrt
class Solution:
    def numSquares(self, n: int) -> int:
        s = int(sqrt(n))
        coins = [k * k for k in range(1, s + 1)]
        T = [float('inf') for _ in range(n + 1)]
        for c in coins:
            T[c] = 1
                
        for i in range(1, n + 1):
            for c in coins:
                if c <= i:
                    T[i] = min(T[i], T[i - c] + 1)

        return T[n]