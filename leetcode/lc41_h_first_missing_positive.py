from typing import List

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        table = [-1] * 301
        # create list of positives
        for i in nums:
            if 0 < i < 301:
                table[i] = 1
        for j in range(1, 301):
            if table[j] == -1:
                return j

class Solution2:
    def firstMissingPositive(self, nums: List[int]) -> int:
        B = 0
        # create list of positives
        for i in nums:
            if 0 < i < 301:
                B |= (1 << i)

        for i in range(1, 301):
            if B & (1 << i) == 0:
                return i

def main():
    nums = [1, 2, 3, 400]
    sol = Solution2()
    p = sol.firstMissingPositive(nums)
    print(p)

if __name__ == '__main__':
    main()
