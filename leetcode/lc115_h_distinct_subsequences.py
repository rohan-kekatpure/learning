class Solution:
    def __init__(self):
        self.count = 0
        self.memo = {}

    def func(self, s, t):
        if (s, t) in self.memo:
            self.count += self.memo[(s, t)]           
            return self.memo[(s, t)]

        if t == '':
            self.count += 1
            return 1

        if s == '':
            return 0

        val1 = val2 = 0
        if s[0] == t[0]:
            val1 = self.func(s[1:], t[1:])


        val2 = self.func(s[1:], t)
        self.memo[(s, t)] = val1 + val2
        return val1 + val2



    def numDistinct(self, s: str, t: str) -> int:
        self.func(s, t)
        return self.count
    
def main():
    sol = Solution()
    s = "aabdbaabeeadcbbdedacbbeecbabebaeeecaeabaedadcbdbcdaabebdadbbaeabdadeaabbabbecebbebcaddaacccebeaeedababedeacdeaaaeeaecbe"
    t = "bddabdcae"    
    count = sol.numDistinct('babgbag', 'bag')
    print(count)


if __name__ == '__main__':
    main()
