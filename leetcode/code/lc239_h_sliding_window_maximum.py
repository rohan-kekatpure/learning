class Heap:
    def __init__(self, arr):
        self.arr = sorted(arr)
        
    def insert(self, x):        
        arr = self.arr
        n = len(arr)
        if n == 0:
            self.arr.append(x)
            return
        
        if x >= arr[-1]:
            arr.append(x)
            return
        
        if x <= arr[0]:
            arr.insert(0, x)
            return 
        
        left, right = 0 , n - 1
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == x:
                arr.insert(mid, x)
                return
            elif arr[mid] < x and arr[mid + 1] > x:
                arr.insert(mid + 1, x)
                return
            elif arr[mid] > x and arr[mid - 1] < x:
                arr.insert(mid, x)
                return
            elif x < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        
    def remove(self, x):
        arr = self.arr
        n = len(arr)
        if n == 0:
            return
        
        left, right = 0, n - 1
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == x:
                arr.pop(mid)
                return
            elif x < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
                
    def top(self):
        return self.arr[-1]
    
class Solution:                        
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """
        O(n log n)
        """
        n = len(nums)
        heap = Heap(nums[:k])  # O(k log k) sort, one time        
        maxvals = [heap.top()]        
        for i in range(n - k):            
            heap.remove(nums[i])
            heap.insert(nums[i + k])            
            maxvals.append(heap.top())                        
        return maxvals
            

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """
        O(n)
        """
        q  = MonoQue()
        res = []
        for i, n in enumerate(nums):
            if i<k: 
                # initialize the queue:
                q.append(n)
            else:
                res.append(q.max())
                q.append(n) # move window right edge 
                q.popleft(nums[i-k]) # move window left edge
        res.append(q.max())
        return res
    
class MonoQue:
    """A monotonic queue object. It has the following property:
        (1) Items inside the queue preserve the order of appending.
        (2) Items inside the queue is non-increasing.
    """
    
    def __init__(self):
        from collections import deque
        self.q = deque()
        
    def append(self, n):
        while self.q and self.q[-1]<n:
            self.q.pop() # pop all elements that are smaller than n
        self.q.append(n)
    
    def popleft(self, n):
        # if the first element of the queue equals to n, pop it.
        if self.q[0]==n:
            self.q.popleft()
    
    def max(self):
        # the max of the queue is the first element.
        return self.q[0]