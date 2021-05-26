class Solution:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)   
        if n == 1:
            return 1 if citations[0] > 0 else 0
        
        left, right = 0, n - 1
        while left < right:
            mid = left + (right - left) // 2
            if citations[mid] >= (n - mid) and citations[mid - 1] < (n - mid + 1):
                return n - mid
            elif citations[mid + 1] >= (n - mid - 1) and citations[mid] < (n - mid):
                return n - mid - 1
            elif citations[mid] >= (n - mid):
                right = mid - 1
            else:
                left = mid + 1
                
        if citations[mid] > 0:
            return n - left
            
        return 0