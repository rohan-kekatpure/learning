from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]

        T = [0] * n
        T[0] = nums[0]
        T[1] = max(T[0], nums[1])

        for i in range(2, n):
            T[i] = max(T[i - 1], nums[i] + T[i - 2])

        return T[-1]

def main():
    sol = Solution()
    # nums = [1,2,3,1]
    # nums = [2, 7, 9, 3, 1]
    nums = [1, 0]
    money = sol.rob(nums)
    print(money)

if __name__ == '__main__':
    main()
