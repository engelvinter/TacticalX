import numpy

from SebFundOperations import SebFundOperations

class SMA10:
    def __init__(self, default_allocation):
        self._default = default_allocation
        self._initial_investing_done = False
        self.name = "SMA10"
    
    def set_logger(self, logger):
        pass
        
    def execute(self, date, market):
        if self._initial_investing_done is False:
            # Do inital investment
            market.update_portfolio(date, self._default)
            self._initial_investing_done = True
            return
        
        # Get available funds at this date
        funds = market.get_available_funds(date)

        new_alloc = {}
        # Iterate through funds in default allocation
        # Only allocate those that are above sma10 (moving average 200 days)
        for name in self._default:
            try:
                fund = funds[name]
                idx = fund.index.get_loc(date, method='ffill')
                sma10 = fund.iloc[idx].sma10
                quote = fund.iloc[idx].quote
                if not numpy.isnan(sma10):
                    if quote > sma10:
                        new_alloc[name] = self._default[name]
            except KeyError:
                pass

        market.update_portfolio(date, new_alloc)