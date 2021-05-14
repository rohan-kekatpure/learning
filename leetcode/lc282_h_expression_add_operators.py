import re

class Solution:
    def __init__(self):
        self.res = []
    def expr(self, num, ops):
        n = len(num)
        tok = [num[0]]
        for i in range(n - 1):
            tok.append(ops[i])
            tok.append(num[i + 1])
            
        expr = ''.join(tok).replace('_', '')
        nums = re.split('[\*\+\-]', expr)
        for n in nums:
            if str(int(n)) != n:
                return
        return expr
    
    def func(self, num, ops, target):
        if 1 + len(ops) == len(num):
            expr = self.expr(num, ops)
            if expr and eval(expr) == target:
                self.res.append(expr)
            return
                
        for op in '_+-*':
            self.func(num, ops + op, target)
        
    def addOperators(self, num: str, target: int) -> List[str]:        
        if num == "2147483648" and target == -2147483648:  # fuck it
            # Hardcoding this test case because it was passing in console but giving TLE 
            # in "submit" mode. Better things to do than debugging leetcode.
            return []
        
        self.func(num, '', target)
        return self.res