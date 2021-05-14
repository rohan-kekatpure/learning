class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        nums.sort()
        for i, n in enumerate(nums):  # Can be replaced by Binary search 
            if n < i + 1:
                return n
            