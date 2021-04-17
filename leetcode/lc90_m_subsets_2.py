from typing import List

class Solution:
    def func(self, nums, subset):
        n = len(nums)
        for i in range(n):
            newindices = [nums[k] for k in range(n) if k > i]
            newsubset = subset + [nums[i]]
            yield newsubset
            if len(newindices) > 0:
                yield from self.func(newindices, newsubset)

    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        subsets = set()
        subsets.add(())
        subset_gen = self.func(nums, [])
        for s in subset_gen:
            t = tuple(sorted(s))
            subsets.add(tuple(t))
        return [list(s) for s in subsets]


def main():
    sol = Solution()
    powerset = sol.subsetsWithDup([1, 1, 1])
    print(powerset)

if __name__ == '__main__':
    main()
