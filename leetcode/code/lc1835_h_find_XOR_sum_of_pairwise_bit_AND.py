from typing import List
class Solution:
    def getXORSum(self, arr1: List[int], arr2: List[int]) -> int:
        xor1 = arr1[0]
        for a in arr1[1:]:
            xor1 ^= a

        xor2 = arr2[0]
        for b in arr2[1:]:
            xor2 ^= b

        return xor1 ^ xor2

