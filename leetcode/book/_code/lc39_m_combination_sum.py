from typing import List
from collections import deque

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        queue = deque()
        combinations = set()
        candidates.sort()

        # Initial setup
        for val in candidates:
            item = (target, val, ())
            queue.appendleft(item)

        # Main BFS loop
        while queue:
            curr_target, curr_val, curr_comb = queue.pop()
            new_target = curr_target - curr_val
            if new_target < 0: continue

            new_comb = curr_comb + (curr_val, )
            new_comb = tuple(sorted(new_comb))

            # Found a solution
            if new_target == 0:
                combinations.add(new_comb)
                continue

            # Continue BFS exploration
            for val in candidates:
                if val > new_target:
                    continue
                new_item = (new_target, val, new_comb)
                queue.appendleft(new_item)

        return [list(c) for c in combinations]

class Solution2:
    def __init__(self):
        self.combinations = set()

    def helper(self, candidates, target, combination):
        # Base cases
        if target < 0: return

        if target == 0:
            self.combinations.add(tuple(sorted(combination)))
            return

        # DFS
        for c in candidates:
            if c <= target:
                self.helper(candidates, target - c, combination + [c])

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        self.helper(candidates, target, [])
        ret = [list(t) for t in self.combinations]
        return ret

