from collections import defaultdict, Counter

class Solution:
    def test(self, hmap, cdict):
        for c, v in cdict.items():
            if hmap[c] < v:
                return False
        return True

    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t): return ''

        n = len(s)
        st = Counter(t)  # Len(st) is <= 52
        hmap = defaultdict(int)
        left = right = 0
        minlen = float('inf')
        window = ''
        while right < n:
            hmap[s[right]] += 1

            while self.test(hmap, st):
                if right - left < minlen:
                    minlen = right - left
                    window = s[left: right + 1]

                hmap[s[left]] -= 1
                left += 1

            right += 1

        return window

def main():
    s = 'ADOBECODEBANC'
    t = 'ABC'

    sol = Solution()
    window = sol.minWindow(s, t)
    print(window)

if __name__ == '__main__':
    main()
