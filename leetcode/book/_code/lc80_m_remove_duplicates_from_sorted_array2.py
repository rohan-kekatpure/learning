from typing import List
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        n = len(nums)
        i = 1
        twice = False
        while i < n:
            if nums[i - 1] == nums[i]:
                if twice:
                    nums.pop(i)
                    n -= 1
                else:
                    twice = True
                    i += 1
            else:
                twice = False
                i += 1

        return n

