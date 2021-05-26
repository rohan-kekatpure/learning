from typing import List


class Solution:
    def find(self, nums, target, kind):
        n = len(nums)
        left, right = 0, n - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            else:  # nums[mid] == target

                if kind == 'left':  # Leftmost bound requested
                    if (mid == 0) or (nums[mid - 1] < target):
                        return mid
                    right = mid - 1

                if kind == 'right':  # rightmost bound requested
                    if (mid == n - 1) or (nums[mid + 1] > target):
                        return mid
                    left = mid + 1

        return -1

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        leftlim = self.find(nums, target, 'left')
        if leftlim == -1:
            return [-1, -1]
        rightlim = self.find(nums, target, 'right')

        return [leftlim, rightlim]

