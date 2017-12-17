

class Rebalance :
    def __init__(self, default_allocation):
        self._default = default_allocation
    
    def execute(self, date, market):        
        tot_sum = sum(market.portfolio.values())
        
        rebalanced = {}
        for name in self._default:
            rebalanced[name] = self._default[name] * tot_sum

        return rebalanced