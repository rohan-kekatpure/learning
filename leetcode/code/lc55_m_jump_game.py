from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        lastpos = n - 1
        for i in range(n - 1, -1, -1):
            if nums[i] + i >= lastpos:
                lastpos = i

        return lastpos == 0

def main():
    sol = Solution()
    nums = [3,2,1,0,4]
    print(sol.canJump(nums))

if __name__ == '__main__':
    main()
