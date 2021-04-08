from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n == 0: return 0

        leftmax = [0] * n
        rightmax = [0] * n

        leftmax[0] = height[0]
        rightmax[-1] = height[-1]
        for i in range(1, n):
            leftmax[i] = max(leftmax[i - 1], height[i])

        for i in range(n - 2, -1, -1):
            rightmax[i] = max(rightmax[i + 1], height[i])

        vol = 0
        for i in range(n):
            vol += min(leftmax[i], rightmax[i]) - height[i]

        return vol

def main():
    height = [4,2,0,3,2,5]
    sol = Solution()
    vol = sol.trap(height)
    print(vol)

if __name__ == '__main__':
    main()
