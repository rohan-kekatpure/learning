class Solution:
    def insertInSortedArray(self, nums, a):
        n = len(nums)
        if a >= nums[-1]:
            nums.insert(n - 1, a)
            return n - 1

        if a <= nums[0]:
            nums.insert(0, a)
            return 0

        left, right = 0, n - 1
        while left <= right:
            mid = left + (right - left) // 2 
            if nums[mid] == a:
                nums.insert(mid, a)
                return
            elif nums[mid - 1] < a and nums[mid] > a:
                nums.insert(mid, a)
                return mid
            elif nums[mid] < a and nums[mid + 1] > a:
                nums.insert(mid + 1, a)
                return mid + 1
            elif nums[mid] > a:
                right = mid - 1            
            else:
                left = mid + 1
        
    def removeFromSortedArray(self, nums, a):
        n = len(nums)
        left, right = 0, n - 1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == a:
                nums.pop(mid)
                return
            elif a < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1                
                
    def containsNearbyAlmostDuplicate(self, nums, k, t):
        n = len(nums)
        if (n == 1) or (k < 1): 
            return False

        k = min(k, n - 1)
        kblock = sorted(nums[:k + 1])  # O(k log k)        
        # Test the first chunk exhaustively
        for i in range(1, k + 1):
            if abs(kblock[i - 1] - kblock[i]) <= t:
                return True
        
        for i in range(n - k - 1):
            self.removeFromSortedArray(kblock, nums[i])
            p = self.insertInSortedArray(kblock, nums[i + k + 1])
            if p == 0:
                diff = abs(kblock[0] - kblock[1])
            elif p == n - 1:
                diff = abs(kblock[n - 1] - kblock[n - 2])
            if 1 <= p < n - 1:
                r = abs(kblock[p] - kblock[p + 1])
                l = abs(kblock[p - 1] - kblock[p])
                diff = min(l, r)
            if diff <= t:
                return True
            
        return False


def main():
    import random
    nums = [-3, 3]
    k, t = 2, 4
    sol = Solution()
    ans = sol.containsNearbyAlmostDuplicate(nums, k, t)
    print(ans)

if __name__ == '__main__':
    main()