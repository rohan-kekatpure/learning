from typing import List

class Solution:
    def func(self, indices, k, comb):
        if k == 1:
            for i in indices:
                yield comb + [i]

        for i in indices:
            newindices = [j for j in indices if j > i]
            newcomb = comb + [i]
            yield from self.func(newindices, k - 1, newcomb)

    def combine(self, n: int, k: int) -> List[List[int]]:
        indices = list(range(1, n + 1))
        gen = self.func(indices, k, [])

        combinations = []
        for c in gen:
            combinations.append(c)

        return combinations

