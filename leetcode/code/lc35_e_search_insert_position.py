from typing import List

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        n = len(nums)
        left, right = 0, n - 1
        mid = -1
        found = False
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            else:
                found = True
                break

        if found:
            return mid

        if left == n - 1:
            if target > nums[n - 1]:
                return n
            else:
                return n - 1

        if right == 0:
            if target < nums[0]:
                return 0
            else:
                return 1

        if right < mid:
            return mid
        elif left > mid:
            return left


def main():
    nums = [1, 3, 5, 6]
    sol = Solution()
    idx = sol.searchInsert(nums, )
    print(idx)


if __name__ == '__main__':
    main()



