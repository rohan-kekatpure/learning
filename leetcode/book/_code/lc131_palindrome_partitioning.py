class Solution:
    def __init__(self):
        self.partitions = []
        
    def func(self, partition, s):
        n = len(s)
        
        # Potentially redundant
        if n == 0:
            self.partitions.append(partition)
            return
        
        if n == 1:
            self.partitions.append(partition + [s])
            return
        
        for i in range(1, n + 1): 
            # We loop from 1 to n + 1, because otherwise, the empty string
            # would always be a palindrome and the recursion wont terminate
            next_partition = s[:i]
            if next_partition == next_partition[::-1]:  # palindrome testing
                self.func(partition + [next_partition], s[i:])
    
    def partition(self, s: str) -> List[List[str]]:
        self.func([], s)
        return self.partitions
    