from typing import List

class Solution:
    def findPivot(self, nums):
        n = len(nums)
        left = 0
        right = n - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[left]:
                left = mid
            else:
                right = mid

        return left

    def binarySearch(self, nums, target):
        n = len(nums)
        left = 0
        right = n - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            else:
                return mid
        return -1

    def search(self, nums: List[int], target: int) -> int:
        pivot = self.findPivot(nums) + 1
        left_array = nums[:pivot]
        right_array = nums[pivot:]
        if (idx := self.binarySearch(left_array, target)) != -1:
            return idx
        if (idx := self.binarySearch(right_array, target)) != -1:
            return pivot + idx
        return -1

