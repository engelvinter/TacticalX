
import Factory

import pandas as pd

class SebRebalance:
    # where fixed alloc is a dictionary
    # name - percentage
    def __init__(self, funds, allocation, start_date, end_date, next):
        f = Factory.Factory()
        self._funds = funds
        self._allocation = allocation
        self._start_date = start_date
        self._end_date = end_date
        self._fund_ops = f.create_fund_operations()
        self._next = next

    def _calc_start_quote(self, fund, fund_interval, start_date):
        start_quote = fund_interval.quote[0]

        if start_date != fund_interval.index[0]:
            start = fund_interval.index[0]
            pos = fund.index.get_loc(start)
            start_quote = fund.iloc[pos - 1].quote

        return start_quote

    def _calc_change_interval(self, fund, start_date, end_date):
        fund_interval = fund[start_date:end_date]
        
        start_quote = self._calc_start_quote(fund, fund_interval, start_date)

        change = fund_interval.quote / start_quote
        return change

    def _get_available_funds(self):
        funds = self._fund_ops.filter_interval(self._funds, 
                                               self._start_date, 
                                               self._end_date)
        return funds
    
    def _rebalance(self, portfolio, allocation):
        rebalanced = {}
        tot_sum = sum(portfolio.values())
        for name in self._allocation:
            rebalanced[name] = allocation[name] * portfolio[name]
        return rebalanced

    def _precheck(self, allocation, funds_in_interval):
        for name in allocation:
            if name not in funds_in_interval:
                raise Exception("Fund not found in i interval")

    def _calc_return(self, portfolio):
        updated_portfolio = {}
        for name in portfolio:
            change_interval = self._calc_change_interval(self._funds[name], 
                                                         self._start_date, 
                                                         self._end_date)
            change_portfolio = portfolio[name] * change_interval
            updated_portfolio[name] = change_portfolio[-1]
        
        return updated_portfolio

    def execute(self, portfolio):
        
        funds_in_interval = self._get_available_funds()
        self._precheck(self._allocation, funds_in_interval)
        
        #rebalanced = self._rebalance(portfolio, self._allocation)
        
        rebalanced = portfolio
        
        new_portfolio = self._calc_return(rebalanced)

        if self._next:
            new_portfolio = self._next.execute(new_portfolio)

        return new_portfolio