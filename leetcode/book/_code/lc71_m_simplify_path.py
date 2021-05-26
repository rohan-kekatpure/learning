class Solution:
    def simplifyPath(self, path: str) -> str:
        comps = path.split('/')
        stack = []
        for c in comps:
            if c in ['', '.']:
                continue
            elif c == '..':
                if len(stack) > 0:
                    stack.pop()
            else:
                stack.append(c)

        return '/' + '/'.join(stack)

