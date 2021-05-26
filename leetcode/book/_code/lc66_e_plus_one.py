from typing import List

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        if digits == [0]:
            return [1]
        carry = 0
        ans = []
        num = 1
        for d in reversed(digits):
            tot = d + num + carry
            rem = tot % 10
            carry = tot // 10
            ans.append(rem)
            num = 0

        if carry > 0:
            ans.append(carry)

        return list(reversed(ans))
