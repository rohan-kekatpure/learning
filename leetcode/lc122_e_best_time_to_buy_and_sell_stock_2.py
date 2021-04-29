class Solution: 
    def maxProfit(self, prices: List[int]) -> int:
    """
    On each day you have the choice to buy, sell, or do nothing. The DP state is captured in 
    two arrays, `buy` and `sell` which indicate the best total balance after having reached day `i`
    with the last transaction of 'buy' and 'sell' respectively. 
    
    In other words `buy[i]` is the best balance you can achieve on day `i` where your last 
    action is 'buy' (and thus you have option to sell next). Similarly `sell[i]` indicates the 
    best balance you can achieve on day `i` where your last action was 'sell' (and thus
    you have option to buy next). 
    
    `buy[i]` is the maximum out of (1) retain previous buy and do nothing today, (2) first buy action
    after having not done anything till now and (3) buy after a previous sell
    
    `sell[i] is maximum out of (1) retain previous sell and do nothing today and (2) sell today
    
    The answer is max(buy[n - 1], sell[n - 1])
    
    Ashamed of my solution after seeing the posted solutions :(
    """
        n = len(prices)
        if n == 0: return 0
        buy = [0] * n
        sell = [0] * n        
        buy[0] = -prices[0]
        for i in range(1, n):
            p = prices[i]
            buy[i] = max(buy[i - 1], -p, sell[i - 1] - p)
            sell[i] = max(sell[i - 1], buy[i - 1] + p)
        return max(buy[-1], sell[-1])