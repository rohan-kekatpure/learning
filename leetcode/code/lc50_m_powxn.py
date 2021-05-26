class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1
        if n < 0:
            x = 1. / x

        n = abs(n)
        if n % 2 == 0:
            return self.myPow(x * x, n // 2)
        else:
            return x * self.myPow(x * x, (n - 1) // 2)

def main():
    sol = Solution()
    ans = sol.myPow(0.00000001, (1 << 31) - 1)
    print(ans)

if __name__ == '__main__':
    main()
