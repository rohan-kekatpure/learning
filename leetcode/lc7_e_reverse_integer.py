class Solution:
    def greater(self, s1, s2):
        l1 = len(s1)
        l2 = len(s2)
        if l1 != l2:
            return l1 > l2

        # equal lengths
        i = 0
        while s1[i] == s2[i]:
            i += 1
        return s1[i] > s2[i]

    def reverse(self, x: int) -> int:
        MAXN = str(1 << 31)
        MAXP = str((1 << 31) - 1)
        positive = (x >= 0)
        s = str(abs(x))
        r = ''.join(reversed(s))

        val = 0
        if positive:
            if not self.greater(r, MAXP):
                val = int(r)
        else:
            if not self.greater(r, MAXN):
                val = -int(r)
        return val

def main():
    sol = Solution()
    r = sol.reverse(0)
    print(r)

if __name__ == '__main__':
    main()



