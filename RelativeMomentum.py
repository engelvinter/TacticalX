
from SebFundOperations import SebFundOperations

import numpy

class RelativeMomentum:
    def __init__(self, default_allocation):
        self._default = default_allocation
        self._initial_investing_done = False
        self._fund_op = SebFundOperations()
        self.name = "Relative Momentum"
        self._lookback_days = 30
        self._nbr_funds = 4
        self._use_sma10 = True

    def set_nbr_funds_in_selection(self, nbr_funds):
        self._nbr_funds = nbr_funds

    def set_sma10(self, sma10):
        self._use_sma10 = sma10

    def set_logger(self, logger):
        self._logger = logger

    def _initial_investment(self, date, market):
        # Do inital investment
        market.update_portfolio(date, self._default)
        self._initial_investing_done = True

    def _calc_average(self, fund_name, fund_returns):
        sum = 0
        for fund_return in fund_returns:
            sum += fund_return[fund_name]

        avg_return = sum / len(fund_returns)
        return avg_return

    def _get_best_funds_average(self, date, avail_funds):
        
        self._logger.debug("avail_funds: {}".format(len(avail_funds)))

        ret_funds1 = self._fund_op.current_return_funds(date, avail_funds, 30)
        ret_funds3 = self._fund_op.current_return_funds(date, avail_funds, 90)
        ret_funds6 = self._fund_op.current_return_funds(date, avail_funds, 180)
        ret_funds12 = self._fund_op.current_return_funds(date, avail_funds, 360)

        self._logger.debug("ret_funds {} {} {} {}".format(len(ret_funds1.keys()), 
                                                         len(ret_funds3.keys()),
                                                         len(ret_funds6.keys()),
                                                         len(ret_funds12.keys())))

        fund_returns = [ret_funds1, ret_funds3, ret_funds6, ret_funds12]

        fund_averages = {}

        for name in avail_funds:
            try:
                avg = self._calc_average(name, fund_returns)
                fund_averages[name] = avg
            except KeyError:
                pass

        return fund_averages

    def _pos_sma10_trend(self, fund, date):
        try:
            idx = fund.index.get_loc(date, method='ffill')
            sma10 = fund.iloc[idx].sma10
            quote = fund.iloc[idx].quote
            if not numpy.isnan(sma10):
                if quote > sma10:
                    return True
        except KeyError:
            pass
        
        return False

    def execute(self, date, market):
        avail_funds = market.get_available_funds(date)

        if self._initial_investing_done is False:
            self._initial_investment(date, market)
            return

        self._logger.debug("**** Rel Mom ****")

        best_funds = self._get_best_funds_average(date, avail_funds)

        if self._use_sma10:
            sma10 = lambda n : self._pos_sma10_trend(avail_funds[n], date)
            tmp = { name : best_funds[name] for name in best_funds if sma10(name) }
            best_funds = tmp

        new_alloc = {}
        # Sort the return, best return first
        sorted_funds = sorted(best_funds.items(), key=lambda x:x[1], reverse=True)
        self._logger.debug("len: {}".format(len(best_funds.keys())))

        for fund_name, _ in sorted_funds[0:self._nbr_funds]:
            new_alloc[fund_name] = 0.20
        
        self._logger.info("{0} {1}".format(date, new_alloc))

        market.update_portfolio(date, new_alloc)



        
