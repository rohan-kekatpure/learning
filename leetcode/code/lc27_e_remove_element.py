from typing import List

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        n = len(nums)
        i = j = 0
        for i in range(n):
            if nums[i] != val:
                nums[j] = nums[i]
                j += 1
        return j

def main():
    nums = [0,1,2,2,3,0,4,2]
    sol = Solution()
    newlen = sol.removeElement(nums, 2)
    from IPython import embed; embed(); exit(0)

if __name__ == '__main__':
    main()

