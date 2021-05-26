from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]

        T = [0] * n
        T[0] = nums[0]
        T[1] = max(T[0], nums[1])

        for i in range(2, n):
            T[i] = max(T[i - 1], nums[i] + T[i - 2])

        return T[-1]

