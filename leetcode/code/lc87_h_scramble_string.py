class Solution:
    def __init__(self):
        self.seen = {}

    def scrambler(self, s):
        if len(s) <= 1:
            return [s]

        n = len(s)
        strs = [s]
        for i in range(1, n):
            left = s[:i]
            if left in self.seen:
                sleft = self.seen[left]
            else:
                sleft = self.scrambler(left)
                self.seen[left] = sleft

            right = s[i:]
            if right in self.seen:
                sright = self.seen[right]
            else:
                sright = self.scrambler(right)
                self.seen[right] = sright

            for sl in sleft:
                for sr in sright:
                    strs.append(sl + sr)
                    strs.append(sr + sl)
        return strs

    def isScramble(self, s1: str, s2: str) -> bool:
        strs = self.scrambler(s1)
        for s in strs:
            if s == s2:
                return True

        return False

def main():
    sol = Solution()
    res = sol.isScramble("abcdbdacbdac", "bdacabcdbdac")
    print(res)

if __name__ == '__main__':
    main()
