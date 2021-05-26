from typing import List 

class Solution:
    def quickselect(self, arr, k):        
        if len(arr) == 1:
            return arr[0]

        pivot = arr[-1]
        lows = [e for e in arr if e < pivot]
        highs = [e for e in arr if e > pivot]
        pivots = [e for e in arr if e == pivot]

        if k <= len(lows):
            return self.quickselect(lows, k)
        elif k <= len(lows) + len(pivots):
            return pivots[0]
        else:
            return self.quickselect(highs, k - len(lows) - len(pivots))
        
    def majorityElement(self, nums: List[int]) -> int:
        n = len(nums)
        return self.quickselect(nums, n // 2 + 1)

