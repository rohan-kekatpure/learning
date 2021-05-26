from typing import List

class Solution:
    def find_closest_elem(self, list_, num):
        n = len(list_)
        left = 0
        right = n - 1
        mid = (left + right) // 2
        while left < right:
            mid = (left + right) // 2
            emid = list_[mid]
            if num == emid:
                return num

            if num > emid:
                left = mid + 1
            elif num < emid:
                right = mid - 1

        if abs(list_[mid] - num) < abs(list_[right] - num):
            return list_[mid]
        else:
            return list_[right]

    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        nums2sum = []
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                nums2sum.append((i, j, nums[i] + nums[j]))
        nums2sum.sort(key=lambda x: x[2])

        best_err = float('inf')
        best_sum = -1
        for i in range(n):
            ni = nums[i]
            sk = self.find_closest_elem(nums2sum, target - ni)
            sum_ = ni + sk
            err = abs(target - sum_)
            if err < best_err:
                best_err = err
                best_sum = sum_

            if err == 0: break

        return best_sum

