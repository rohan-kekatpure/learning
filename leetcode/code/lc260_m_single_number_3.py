class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:
        # O(n)/O(n)
        map_ = {}
        for n in nums:
            map_[n] = map_.get(n, 0) + 1
        
        ans = [k for k, v in map_.items() if v == 1]
        return ans