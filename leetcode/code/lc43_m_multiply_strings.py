from typing import List

class Solution:
    def add(self, L1: List, L2: List):
        assert len(L1) == len(L2), 'Lists have unequal length'
        n = len(L1)
        carry = 0
        ret = [0] * n
        for i in range(n):
            tot = L1[i] + L2[i] + carry
            carry = tot // 10
            unit = tot % 10
            ret[i] = unit
        return ret

    def multiply(self, num1: str, num2: str) -> str:
        if (num1 == '0') or (num2 == '0'): return '0'
        n1 = len(num1)
        n2 = len(num2)
        n = n1 + n2 + 1
        ans = [0] * n

        num1 = num1[::-1]
        num2 = num2[::-1]
        for power, c2 in enumerate(num2):
            carry = 0
            buf = [0] * n
            for i, c1 in enumerate(num1):
                d1 = int(c1)
                d2 = int(c2)
                # if (d1 == 0) or (d2 == 0): continue

                v = d1 * d2 + carry
                carry = v // 10  # new carry
                unit = v % 10
                idx = power + i
                buf[idx] = unit
                buf[idx + 1] = carry
            ans = self.add(ans, buf)

        # Strip leading zeros from answer
        ans.reverse()
        i = 0
        while ans[i] == 0:
            i += 1
        ans = ans[i:]

        # Create string and return
        return ''.join([str(c) for c in ans])
