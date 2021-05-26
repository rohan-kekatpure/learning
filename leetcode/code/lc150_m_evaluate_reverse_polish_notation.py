class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        op = {'+', '-', '*', '/'}
        while tokens:            
            tok = tokens.pop(0)                
            if not (tok in op):
                stack.append(int(tok))
            else:
                n2 = stack.pop()  # Second operand
                n1 = stack.pop()  # First operand
                
                if tok == '+':
                    stack.append(n1 + n2)
                elif tok == '-':
                    stack.append(n1 - n2)
                elif tok == '*':
                    stack.append(n1 * n2)
                elif tok == '/':
                    stack.append(int(n1 / n2))
                    
        return stack[0]
                    
                
                