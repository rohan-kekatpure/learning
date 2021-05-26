class Solution:
    def findMin(self, nums):
        n = len(nums)
        
        if nums[0] < nums[n - 1]:
            return nums[0]
        
        if n == 1:
            return nums[0]
        
        left, right = 0, n - 1

        # Note that in a standrd binary sear
        while left < right:            
            mid = (left + right) // 2
            if nums[mid] > nums[left]:
                left = mid
            else:
                right = mid
                
        return nums[left + 1]        


# Official solution
class Solution(object):
    def findMin(self, nums):
        if len(nums) == 1:
            return nums[0]

        left, right = 0, len(nums) - 1

        # Array not rotated
        if nums[right] > nums[0]:
            return nums[0]

        while right >= left:
            mid = left + (right - left) / 2
            if nums[mid] > nums[mid + 1]:
                return nums[mid + 1]
            if nums[mid - 1] > nums[mid]:
                return nums[mid]

            if nums[mid] > nums[0]:
                left = mid + 1
            else:
                right = mid - 1