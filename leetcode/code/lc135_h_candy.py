class Solution:
    def candy(self, ratings: List[int]) -> int:
        """
        Need forward and reverse pass. The rest of the 
        logic should be clear from code.
        """
        n = len(ratings)
        T = [1] * n  # One candy to each child initially
        
        # backward looking pass
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                T[i] = T[i - 1] + 1
        
        # forward looking pass
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                T[i] = max(T[i], T[i + 1] + 1)
        
        return sum(T)
        