class Solution:
    def mySqrt(self, x: int) -> int:
        # Establish max
        left, right = 0, x
        while left <= right:
            mid = (left + right) // 2
            sqr = mid * mid
            if sqr < x:
                left = mid + 1
            elif sqr > x:
                right = mid - 1
            else:
                return mid

        return right

