from typing import List

class Solution:
    def __init__(self):
        self.plist = []

    def helper(self, s, nl, nr):
        if (nl == 0) and (nr == 0):
            self.plist.append(s)
            return

        # No matter what state, the parens are valid
        # if you open one more.
        if nl > 0:
            self.helper(s + '(', nl - 1, nr)


        # If the last paren is '(', then closing it
        # is always valid
        if s[-1] == '(':
            if nr > 0:
                self.helper(s + ')', nl, nr - 1)

        # If last paren is ')', then you can close
        # one more if number of open parens is > 
        # number of closed parens
        if s[-1] == ')':
            if nl < nr:
                self.helper(s + ')', nl, nr - 1)                

    def generateParenthesis(self, n: int) -> List[str]:
        self.helper('(', n - 1, n)
        return self.plist

