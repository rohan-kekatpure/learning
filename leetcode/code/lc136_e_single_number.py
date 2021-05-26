class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        Idea:

        Sort the numbers and alternatively add and subtract the
        consecutive numbers from `count`. What remains in the end
        is the single number.        
        """
        nums.sort()
        s = 0
        sign = 1
        for i in nums:
            s += sign * i
            sign *= -1
            
        return s
        