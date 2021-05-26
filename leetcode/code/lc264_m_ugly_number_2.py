class Solution:
    def nthUglyNumber(self, n: int) -> int:
        p = q = r = 0        
        ans = [1]
        ansset = {1}  # For fast lookup of already seen ugly numbers
        i = 1
        while i < n:
            k2 = ans[p] * 2
            k3 = ans[q] * 3
            k5 = ans[r] * 5
            k = min(k2, k3, k5)
            
            if k == k2:
                p += 1
            elif k == k3:
                q += 1
            else:
                r += 1
            
            if not k in ansset:
                ans.append(k)
                ansset.add(k)
                i += 1
            
        return ans[-1]