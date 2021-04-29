class Solution1:
    def func(self, s1, s2, s3):
        if len(s3) != len(s1) + len(s2):
            return False

        if s1 == '':
            return s2 == s3
        elif s2 == '':
            return s1 == s3

        if len(s1) == 1 and len(s2) == 1:
            return (s3 == s1 + s2) or (s3 == s2 + s1)

        if not s3[0] in [s1[0], s2[0]]:
            return False

        r1 = r2 = False

        if s1[0] == s3[0]:
            r1 = self.func(s1[1:], s2, s3[1:])

        if s2[0] == s3[0]:
            r2 = self.func(s1, s2[1:], s3[1:])

        return r1 or r2

    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        return self.func(s1, s2, s3)


class Solution:
    def isInterleave(self, s1, s2, s3):
        m = len(s1)
        n = len(s2)
        k = len(s3)
        if k != m + n:
            return False

        T = [[False for _ in range(n + 1)] for _ in range(m + 1)]
        T[0][0] = True

        for i in range(1, m + 1):
            T[i][0] = s3[:i] == s1[:i]

        for j in range(1, n + 1):
            T[0][j] = s3[:j] == s2[:j]

        for i in range(1, m + 1):  # Rows
            for j in range(1, n + 1):  # Cols
                c1 = T[i - 1][j] and (s3[i + j - 1] == s1[i - 1])
                c2 = T[i][j - 1] and (s3[i + j - 1] == s2[j - 1])
                T[i][j] = c1 or c2

        return T[m][n]


def main():
    sol = Solution()
    # s1 = "db"
    # s2 = "b"
    # s3 = "cbb"
    s1 = "cbcccbabbccbbcccbbbcabbbabcababbbbbbaccaccbabbaacbaabbbc"
    s2 = "abcbbcaababccacbaaaccbabaabbaaabcbababbcccbbabbbcbbb"
    s3 = "abcbcccbacbbbbccbcbcacacbbbbacabbbabbcacbcaabcbaaacbcbbbabbbaacacbbaaaabccbcbaabbbaaabbcccbcbabababbbcbbbcbb"
    ans = sol.isInterleave(s1, s2, s3)
    print(ans)

if __name__ == '__main__':
    main()
