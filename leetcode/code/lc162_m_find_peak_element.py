class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return 0
    
        if nums[0] > nums[1]:
            return 0
        if nums[n - 1] > nums[n - 2]:
            return n - 1

        left, right = 0, n - 1
        while left < right:
            mid = (left + right) // 2
            
            if nums[mid - 1] < nums[mid] and nums[mid + 1] < nums[mid]:
                return mid

            if nums[mid - 1] < nums[mid]:
                left = mid
            else:
                right = mid
