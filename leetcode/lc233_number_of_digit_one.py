import math

def bruteforce(n):
    res = 0
    for k in range(n + 1):
        res += sum(1 for x in str(k) if x == '1')
    return res


class Solution:
    def countOnes(self, N):
        if N == 0:
            return 0
        
        p = int(math.log10(N))
        x = 10 ** p
        k = p * x // 10
        if N == x:
            return k + 1
        else:
            return x + (N // x) * k 
    
    def countDigitOne(self, n: int) -> int:
        m = n
        p = 10
        res = 0
        dsum = 0
        while m > 0:
            d = m % p            
            res += self.countOnes(d)

            # Whenever the most significant digit of the remainder (`d`) is 1,
            # the number of 1's in the answer increases by whatever was the 
            # sum of previous remainders. For example, if N = 2121, then
            # we cant simply break it as 2000 + 100 + 20 + 1. Because of
            # that 1 in the hundreds place, 21 more ones would be added to the
            # answer. We have to account for those
            MSD = 10 * d / p  # Most significant digit; can also be computed as str(d)[0]
            if MSD == 1:
                res += dsum

            dsum += d                
            m -= d
            p *= 10
        return res

def main():
    sol = Solution()
    n = 21121
    # from IPython import embed; embed(); exit(1)    
    ans1 = sol.countDigitOne(n)
    ans2 = bruteforce(n)
    print(ans1, ans2)
if __name__ == '__main__':
    main()
