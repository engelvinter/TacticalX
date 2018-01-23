
from SebFundOperations import SebFundOperations

class RelativeMomentum:
    def __init__(self, default_allocation, average_strategy = False):
        self._default = default_allocation
        self._initial_investing_done = False
        self._fund_op = SebFundOperations()
        self.name = "Relative Momentum"
        self._lookback_days = 30
        self._best_funds = self.set_strategy(average_strategy)

    def set_strategy(self, average):
        if average:
            return self._get_best_funds_average
        
        return self._get_best_funds

    def set_logger(self, logger):
        self._logger = logger

    def _initial_investment(self, date, market):
        # Do inital investment
        market.update_portfolio(date, self._default)
        self._initial_investing_done = True

    def _get_best_funds(self, date, market):
        # Calc return of all available funds one month back
        avail_funds = market.get_available_funds(date)
        ret_funds = self._fund_op.current_return_funds(date, avail_funds, self._lookback_days)

        # Sort the return, best return first
        ret_sorted = sorted(ret_funds.items(), key=lambda x:x[1], reverse=True)

        return ret_sorted

    def _calc_average(self, fund_name, fund_returns):
        sum = 0
        for fund_return in fund_returns:
            sum += fund_return[fund_name]

        avg_return = sum / len(fund_returns)
        return avg_return

    def _get_best_funds_average(self, date, market):
        avail_funds = market.get_available_funds(date)

        ret_funds1 = self._fund_op.current_return_funds(date, avail_funds, 30)
        ret_funds3 = self._fund_op.current_return_funds(date, avail_funds, 90)
        ret_funds6 = self._fund_op.current_return_funds(date, avail_funds, 180)
        ret_funds12 = self._fund_op.current_return_funds(date, avail_funds, 360)

        fund_returns = [ret_funds1, ret_funds3, ret_funds6, ret_funds12]

        fund_averages = {}
        for name in avail_funds:
            try:
                avg = self._calc_average(name, fund_returns)
                fund_averages[name] = avg
            except KeyError:
                pass

         # Sort the return, best return first
        avg_sorted = sorted(fund_averages.items(), key=lambda x:x[1], reverse=True)

        return avg_sorted

    def execute(self, date, market):
        if self._initial_investing_done is False:
            self._initial_investment(date, market)
            return

        self._logger.debug("**** Rel Mom ****")

        best_funds = self._best_funds(date, market)

        new_alloc = {}        
        for fund_name, _ in best_funds[0:4]:
            new_alloc[fund_name] = 0.20
        
        self._logger.debug("{0} {1}".format(date, new_alloc))

        market.update_portfolio(date, new_alloc)



        
