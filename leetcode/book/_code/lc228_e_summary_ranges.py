class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        l = r = 0
        n = len(nums)
        ranges = []
        while r < n:
            while (r < n - 1) and (nums[r + 1] - nums[r] == 1):
                r += 1
            
            
            if r > l:
                curr_range = f'{nums[l]}->{nums[r]}'
            else:
                curr_range = f'{nums[l]}'
                
            ranges.append(curr_range)
            l = r = r + 1
            
        return ranges
