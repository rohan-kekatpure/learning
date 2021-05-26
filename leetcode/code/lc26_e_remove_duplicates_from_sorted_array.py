from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        n = len(nums)
        i = 1
        while i < n:
            if nums[i - 1] == nums[i]:
                nums.pop(i)
                n -= 1
            else:
                i += 1

        return n

def main():
    sol = Solution()
    nums = [1, 2, 2]
    from IPython import embed; embed(); exit(0)
    sol.removeDuplicates(nums)

if __name__ == '__main__':
    main()
