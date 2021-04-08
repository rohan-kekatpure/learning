from typing import List

class Solution:
    def __init__(self):
        self.plist = []

    def helper(self, s, nl, nr):
        if (nl == 0) and (nr == 0):
            self.plist.append(s)
            return

        if len(s) == 0:
            self.helper(s + '(', nl - 1, nr)
            return

        if s[-1] == '(':
            if nl > 0:
                self.helper(s + '(', nl - 1, nr)
            if nr > 0:
                self.helper(s + ')', nl, nr - 1)

        if s[-1] == ')':
            if nl > 0:
                self.helper(s + '(', nl - 1, nr)
            if nl < nr:
                self.helper(s + ')', nl, nr - 1)

    def generateParenthesis(self, n: int) -> List[str]:
        self.helper('', n, n)
        return self.plist

def main():
    sol = Solution()
    plist = sol.generateParenthesis(2)
    print(plist)

if __name__ == '__main__':
    main()
