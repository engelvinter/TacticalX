
import Factory

import pandas as pd

class SebRebalance:
    # where fixed alloc is a dictionary
    # name - percentage
    def __init__(self, funds, fixed_alloc, start_date, end_date, next):
        f = Factory.Factory()
        self._funds = funds
        self._fixed_alloc = fixed_alloc
        self._start_date = start_date
        self._end_date = end_date
        self._fund_ops = f.create_fund_operations()
        self._next = next

    def _realloc(self, fixed_alloc):
        return fixed_alloc

    def _calc_new_result(self, fund, alloc):
        fund_interval = fund.loc[self._start_date:self._end_date]
        percent = fund_interval.quote / fund.quote[0]
        return percent * alloc

    def _get_available_funds(self):
        funds = self._fund_ops.filter_interval(self._funds, 
                                               self._start_date, 
                                               self._end_date)
        return funds
        
    def execute(self):
        percent = 0
        funds_in_interval = self._get_available_funds()

        for name in self._fixed_alloc:
            if name not in funds_in_interval:
                raise Exception("Fund not found in i interval")
            percent += self._calc_new_result(self._funds[name], 
                                             self._fixed_alloc[name])
        
        if self._next:
            next_percent = self._next.execute()
            sum = percent.add(next_percent, fill_value=0)
            return sum
        else:
            return percent