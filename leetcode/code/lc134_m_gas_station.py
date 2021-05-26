class Solution:
    def circuit(self, gas, cost, i, n):
        tank = gas[i]
        for _ in range(n + 1): 
            i1 = (i + 1) % n
            if tank < cost[i]:
                return False
            tank = tank - cost[i] +  gas[i1]
            i = i1
            
        return True
        
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        n = len(gas)
        if n == 1:
            if gas[0] >= cost[0]:
                return 0
            else:
                return -1
            
        startpoints = []
        for i in range(n):
            if cost[i] < gas[i]:
                startpoints.append(i)
        
        if len(startpoints) == 0:
            return -1
        
        for i in startpoints:
            if self.circuit(gas, cost, i, n):
                return i
        
        return -1
        
            
class Solution:
    """
    O(n) solution that I did not come up with
    """
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        if (sum(gas) - sum(cost) < 0):
            return -1
        
        tank, start_index = 0, 0
        
        for i in range(len(gas)):
            tank += gas[i] - cost[i]
            
            if tank < 0:
                start_index = i + 1
                tank = 0
            
        return start_index    