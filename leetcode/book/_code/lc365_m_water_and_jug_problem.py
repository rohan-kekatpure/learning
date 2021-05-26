from math import gcd

class Solution:
    def canMeasureWater(self, jug1Capacity: int, jug2Capacity: int, targetCapacity: int) -> bool:
        x = targetCapacity
        j1 = jug1Capacity
        j2 = jug2Capacity        
        if x > j1 + j2:
            return False
        g  = gcd(j1, j2)
        return x % g == 0
        