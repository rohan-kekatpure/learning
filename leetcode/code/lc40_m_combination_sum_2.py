from typing import List


class Solution:
    def __init__(self):
        self.combinations = set()
        self.visited = set()

    def helper(self, candidates, target, combination):
        if target < 0: return
        if target == 0:
            self.combinations.add(combination)
            return

        n = len(candidates)
        for i in range(n):
            c = candidates[i]
            if c <= target:
                newcandidates = tuple(candidates[k] for k in range(n) if (k != i and candidates[k] < target))
                new_combination = tuple(sorted(combination + (c, )))
                item = (newcandidates, target - c, new_combination)
                if not (item in self.visited):
                    self.visited.add(item)
                    self.helper(*item)

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        self.helper(candidates, target, ())
        return [list(t) for t in self.combinations]

def main():
    candidates = [10,1,2,7,6,1,5]
    sol = Solution()
    combinations = sol.combinationSum2(candidates, 27)
    print(combinations)

if __name__ == '__main__':
    main()
