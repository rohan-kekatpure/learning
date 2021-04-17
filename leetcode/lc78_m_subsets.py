from typing import List

class Solution:
    def func(self, indices, subset):
        n = len(indices)
        for i in range(n):
            newindices = [indices[k] for k in range(n) if k > i]
            newsubset = subset + [indices[i]]
            yield newsubset
            if len(newindices) > 0:
                yield from self.func(newindices, newsubset)

    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        gen = self.func(nums, [])
        powerset = [[]] + list(gen)
        return powerset

def main():
    sol = Solution()
    powerset = sol.subsets([1, 2, 3])
    from IPython import embed; embed(); exit(0)
    print(powerset)

if __name__ == '__main__':
    main()
