from typing import List, Dict

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        MAP = {}
        for i in nums:
            if i in MAP:
                MAP[i] += 1
            else:
                MAP[i] = 1

        n = len(nums)
        result = set()
        seen = set()
        for i in range(n):
            ei = nums[i]

            if ei in seen: continue
            seen.add(ei)

            for j in range(i + 1, n):
                ej = nums[j]
                ek = -ei - ej
                MAP[ei] -= 1
                MAP[ej] -= 1
                if MAP.get(ek, 0) > 0:
                    t = tuple(sorted([ei, ej, ek]))
                    result.add(t)
                MAP[ei] += 1
                MAP[ej] += 1
        result = [list(t) for t in result]
        return result

def main():
    sol = Solution()
    nums = [0]
    res = sol.threeSum(nums)
    print(res)

if __name__ == '__main__':
    main()
