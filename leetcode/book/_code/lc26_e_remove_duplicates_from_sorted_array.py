from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        n = len(nums)
        i = 1
        while i < n:
            if nums[i - 1] == nums[i]:
                nums.pop(i)
                n -= 1
            else:
                i += 1

        return n

