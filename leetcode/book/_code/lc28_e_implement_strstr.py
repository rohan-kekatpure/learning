class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        n = len(haystack)
        m = len(needle)

        if m == 0: return 0

        i = 0
        while i <= n - m:
            j = 0
            idx = i
            while (i < n) and (j < m) and (haystack[i] == needle[j]):
                print(i, j, haystack[i], needle[j])
                i += 1
                j += 1

            if j == m:
                return idx

            i = idx + 1

        return -1


