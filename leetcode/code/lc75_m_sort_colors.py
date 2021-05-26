from typing import List
import random

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        counts = [0] * 3
        for i in nums:
            counts[i] += 1

        k = 0
        for i, c in enumerate(counts):
            for _ in range(c):
                nums[k] = i
                k += 1

def main():
    nums = [random.randint(0, 2) for _ in range(10)]
    sol = Solution()
    sol.sortColors(nums)
    print(nums)

if __name__ == '__main__':
    main()





