class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        if num in [1, 4]:
            return True
        
        if num in [2, 3, 5]:
            return False
        
        left, right = 0, num // 2
        while left <= right:
            mid = left + (right - left) // 2
            sqr = mid * mid
            if sqr == num:
                return True
            elif sqr > num:
                right = mid - 1
            else:
                left = mid + 1
                
        return False
    