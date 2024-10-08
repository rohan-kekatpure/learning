class Solution:
    def repeatchar(self, substr):
        seen = {}
        for c in substr:
            if c in seen:
                return True
            else:
                seen[c] = 1
        return False

    def lengthOfLongestSubstring_bruteforce(self, s: str) -> int:
        n = len(s)
        best = 0
        for i in range(n):
            for j in range(i + 1, n + 1):
                if j - i <= best: continue
                substr = s[i: j]
                if self.repeatchar(substr):
                    break
                length = j - i
                if length > best:
                    best = length
        return best

    def lengthOfLongestSubstring(self, s: str) -> int:
        chars = [0] * 128
        left = right = 0
        res = 0
        while right < len(s):
            r = s[right]
            chars[ord(r)] += 1

            while chars[ord(r)] > 1:
                l = s[left]
                chars[ord(l)] -= 1
                left += 1

            res = max(res, right - left + 1)

            right += 1
        return res



def main():
    s = 'aab'
    sol = Solution()
    best = sol.lengthOfLongestSubstring(s)
    print(best)

if __name__ == '__main__':
    main()
