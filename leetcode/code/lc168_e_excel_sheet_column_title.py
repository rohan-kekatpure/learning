class Solution:
    def convertToTitle(self, columnNumber: int) -> str:
        nums = range(1, 27)
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        mapping = dict(zip(nums, letters))
        
        q = 1
        n = columnNumber
        title = []
        while n > 0:
            n, r = n // 26, n % 26
            if r == 0:
                r = 26
                n -= 1
                
            title.insert(0, mapping[r])
        return ''.join(title)
