class Solution:
    def ispal(self, x):
        return x == x[::-1]


    def palindromeTable(self, s):
        n = len(s)
        ptable = [[0 for _ in range(n)] for _ in range(n)]
        ptable[n - 1][n - 1] = 1

        for i in range(n - 1):
            ptable[i][i] = 1
            ptable[i][i + 1] = int(s[i] == s[i + 1])

        for w in range(2, n):
            for i in range(n - w):            
                j = i + w                
                if (ptable[i + 1][j - 1] == 1) and (s[i] == s[j]):                    
                    ptable[i][j] = 1

        return ptable

    def minCut(self, s: str) -> int:
        """
        Time: O(n^3), Space O(n)

        The main idea is to use a 1D bottom up DP. T[i] is the 
        minimum number of partitions required to get palindromic
        substrings for s[0..i]. We can compute T[i] in the 
        following way:

        x x x x x x x x x x
            j     i

        With reference to the above diagram. If string s[j..i] is 
        a palindrome, then T[i] is one plus T[j - 1]. I.e. if we 
        get a palindromic chunk for j..i, then the number of partitions
        is simply one plus the number required up till j - 1.

        Else, it is simply one plus the number of partitions required
        up to the previous character. 

        Final subtlety is to do this for all j from 0..i and take the
        best answer. 

        The O(n^3) can be reduced to O(n^2) by precomputing the 
        palindromeness for each (i, j)

        """
        n = len(s)
        ptable = self.palindromeTable(s)
        
        T = list(range(n))
        for i in range(1, n):
            if ptable[0][i] == 1:
                T[i] = 0
                continue

            for j in range(i):
                if ptable[j][i] == 1:
                    T[i] = min(T[i], T[j - 1] + 1)
                else:
                    T[i] = min(T[i], T[i - 1] + 1)

        return T[-1]


