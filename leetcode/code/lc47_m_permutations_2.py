from typing import List

class Solution:
    def __init__(self):
        self.seen = set()

    def helper(self, perm, elems):
        if len(elems) == 1:
            yield list(perm + elems)

        n = len(elems)
        for i in range(n):
            newperm = perm + (elems[i], )
            newelems = tuple([elems[j] for j in range(n) if j != i])
            newitem = (newperm, newelems)
            if not (newitem in self.seen):
                self.seen.add(newitem)
                yield from self.helper(*newitem)

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        permgen = self.helper((), tuple(nums))
        answer = []
        for p in permgen:
            answer.append(p)
        return answer

def main():
    sol = Solution()
    nums = [1]
    ans = sol.permuteUnique(nums)
    print(ans)

if __name__ == '__main__':
    main()
