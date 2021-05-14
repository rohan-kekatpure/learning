class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        min_length = float('inf')
        n = len(nums)
        tot = 0
        for right in range(n):
            tot += nums[right]
            
            while tot >= target:
                min_length = min(min_length, right - left + 1)
                tot -= nums[left]
                left += 1
        
        ans = 0 if min_length == float('inf') else min_length
        return ans

    
            