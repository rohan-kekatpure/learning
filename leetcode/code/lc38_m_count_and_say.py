class Solution:
    def helper(self, s):
        s += '_'
        n = len(s)
        digit_counts = []
        i = 0
        while i < n - 1:
            count = 1
            while s[i] == s[i + 1]:
                count += 1
                i += 1

            digit_counts.append((s[i], count))
            i += 1
        out = ''
        for digit, count in digit_counts:
            out += f'{count}{digit}'
        return out

    def countAndSay(self, n: int) -> str:
        css = '1'
        for i in range(1, n):
            css = self.helper(css)
        return css

def main():
    sol = Solution()
    for i in range(10):
        print(sol.countAndSay(i))

    from IPython import embed; embed(); exit(0)

if __name__ == '__main__':
    main()
