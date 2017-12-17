

class BuyAndHold :
    def __init__(self, default_allocation):
        self._default = default_allocation
        self._initial_investing_done = False

    def execute(self, date, market):
        if self._initial_investing_done is True:
            return

        market.update_portfolio(date, self._default)
        self._initial_investing_done = True