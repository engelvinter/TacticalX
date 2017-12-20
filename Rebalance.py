

class Rebalance :
    def __init__(self, default_allocation):
        self._default = default_allocation

    def execute(self, date, market):
        market.update_portfolio(date, self._default)