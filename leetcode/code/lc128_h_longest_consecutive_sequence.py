class Solution:
    # time: O(n log n), space O(n)
    def longestConsecutive(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0: 
            return 0
        
        nums.sort()  # n log n        
        count = 1
        for i in range(1, n):
            if nums[i] - nums[i - 1] == 1:
                count += 1
            elif nums[i] == nums[i - 1]:
                pass
            else:
                count = 1
        return count
