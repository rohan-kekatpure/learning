class Solution:
    def __init__(self):
        self.combinations = set()
    def func(self, nums, target, path, k):
        if len(path) == k and target == 0:
            self.combinations.add(tuple(sorted(path)))
        
        for n in nums:
            if (n <= target) and (len(path) < k):
                newnums = [e for e in nums if e != n and e <= target]
                self.func(newnums, target - n, path + [n], k)
        
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        nums = list(range(1, 10))
        self.func(nums, n, [], k)
        return list(self.combinations)