# The isBadVersion API is already defined for you.
# @param version, an integer
# @return an integer
# def isBadVersion(version):

class Solution:
    def firstBadVersion(self, n):
        left, right = 0, n
        while left <= right:
            mid = left + (right - left) // 2
            isbad_m = isBadVersion(mid)
            isbad_mnext = isBadVersion(mid + 1)
            isbad_mprev = isBadVersion(mid - 1)
            if isbad_m and (not isbad_mprev):
                return mid
            elif (not isbad_m) and (isbad_mnext):
                return mid + 1
            elif isbad_m:
                right = mid - 1
            else:
                left = mid + 1
            
                
class Solution:
    def firstBadVersion(self, n):
        left, right = 0, n
        while left < right - 1:
            mid = left + (right - left) // 2            
            if isBadVersion(mid):
                right = mid
            else:
                left = mid
                
        return right
            