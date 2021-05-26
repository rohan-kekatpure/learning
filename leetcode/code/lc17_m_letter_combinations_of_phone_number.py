from typing import List

class Solution:
    def __init__(self):
        self.strs = []
        self.MAP = {
            '2': ['a', 'b', 'c'],
            '3': ['d', 'e', 'f'],
            '4': ['g', 'h', 'i'],
            '5': ['j', 'k', 'l'],
            '6': ['m', 'n', 'o'],
            '7': ['p', 'q', 'r', 's'],
            '8': ['t', 'u', 'v'],
            '9': ['w', 'x', 'y', 'z']
        }

    def _func(self, digits, str_):
        if digits == '':
            self.strs.append(str_)
            return

        d = digits[0]
        for c in self.MAP[d]:
            self._func(digits[1:], str_ + c)

    def letterCombinations(self, digits: str) -> List[str]:
        digits = digits.strip()
        if digits == '': return []

        self._func(digits, '')
        return self.strs


def main():
    sol = Solution()
    strs = sol.letterCombinations('')
    print(strs)

if __name__ == '__main__':
    main()
