class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        wordDict = set(wordDict)
        wordDict.add('')
        n = len(s)
        T = [False] * (n + 1)
        T[0] = True
        for i in range(n + 1):
            for j in range(i):
                if T[j] and (s[j: i] in wordDict):
                    T[i] = True
                    break
        
        print(T)
        return T[-1]
    
        