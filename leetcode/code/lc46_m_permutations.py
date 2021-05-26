from typing import List

class Solution:
    def helper(self, perm, indices):
        if len(indices) == 1:
            yield perm + indices

        for i in indices:
            newperm = perm + [i]
            newindices = [j for j in indices if j != i]
            yield from self.helper(newperm, newindices)

    def permute(self, nums: List[int]) -> List[List[int]]:
        indices = list(range(len(nums)))
        permgenerator = self.helper([], indices)

        # Construct permuted lists from permutation indices
        ans = []
        for idx in permgenerator:
            perm = [nums[i] for i in idx]
            ans.append(perm)
        return ans

def main():
    nums = list(range(9))
    sol = Solution()
    perms = sol.permute(nums)
    for row in perms:
        print(row)
if __name__ == '__main__':
    main()


