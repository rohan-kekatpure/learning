class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        high = float('-inf')
        maxprofit = 0
        for i in range(n - 2, -1, -1):
            high = max(high, prices[i + 1])
            maxprofit = max(maxprofit, high - prices[i])
        return maxprofit
