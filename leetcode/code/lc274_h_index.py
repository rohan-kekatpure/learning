class Solution:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)
        citations.sort(reverse=True)
        i = 0        
        while (i < n)  and (citations[i] >= (i + 1)):            
            i += 1
        return i                        