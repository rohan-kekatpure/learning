from operator import ge, le


class Solution:
    def isMonotonic(self, A: List[int]) -> bool:
        n = len(A)
        if n == 1:
            return True
        if A[0] >= A[-1]:
            op = ge
        else:
            op = le

        res = True
        for i in range(n - 1):
            res &= op(A[i], A[i + 1])
        return res
