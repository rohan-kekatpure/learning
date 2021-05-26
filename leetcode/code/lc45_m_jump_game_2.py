from typing import List

class Solution:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        MAX = 1001
        T = [MAX] * n
        T[0] = 0

        # Main loop
        for i in range(1, n):
            for j in range(i):
                if nums[j] >= i - j:
                    T[i] = min(T[i], T[j] + 1)

        return T[-1]

def main():
    nums = [1, 3, 6, 3, 2, 3, 6, 8, 9, 5]
    sol = Solution()
    steps = sol.jump(nums)
    print(steps)

if __name__ == '__main__':
    main()
