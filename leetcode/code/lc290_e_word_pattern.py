class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        p2w = defaultdict(set)
        w2p = defaultdict(set)
        s = s.split(' ')
        if len(pattern) != len(s):
            return False
        
        for p, w in zip(pattern, s):
            p2w[p].add(w)
            w2p[w].add(p)
    
        for p, w in zip(pattern, s):
            if (len(p2w[p]) != 1) or (len(w2p[w]) != 1):
                return False
            
        return True