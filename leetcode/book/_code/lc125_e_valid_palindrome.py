class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()
        l = [c for c in s if 48 <= ord(c) <= 57 or 97 <= ord(c) <= 122]
        t = ''.join(l)
        return t == t[::-1]
    
        