class Solution:
    def numDecodings(self, s: str) -> int:
        mapping = set([str(x) for x in range(1, 27)])
        n = len(s)
        if n == 1:
            return int(s[0] in mapping)

        T = [0] * n
        T[0] = int(s[0] in mapping)
        T[1] = (s[0] in mapping and s[1] in mapping) + (s[:2] in mapping)
        for i in range(2, n):
            T[i] = (s[i] in mapping) * T[i - 1] + (s[i-1:i+1] in mapping) * T[i - 2]

        return T[-1]



