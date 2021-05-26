from typing import List 

class Solution:
    def quickselect(self, nums, k):
        if len(nums) == 1:
            return nums[0]
        
        n = len(nums)        
        pivot = nums[n - 1]
        lows = [e for e in nums if e < pivot]
        highs = [e for e in nums if e > pivot]
        pivots = [e for e in nums if e == pivot]
        
        nl = len(lows)
        np = len(pivots)
        nh = len(highs)
        if k < nl:
            return self.quickselect(lows, k)
        elif k < nl + np:
            return pivots[0]
        else:
            return self.quickselect(highs, k - nl - np)
                    
    def findKthLargest(self, nums: List[int], k: int) -> int:
        ek = self.quickselect(nums, k)
        return ek

