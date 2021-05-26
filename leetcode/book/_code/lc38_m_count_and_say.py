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

