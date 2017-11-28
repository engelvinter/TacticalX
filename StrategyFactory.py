from datetime import date, datetime, timedelta

import pandas as pd

import SebRebalance

class StrategyFactory:
    def __init__(self, funds, start_date, end_date):
        self._funds = funds
        self._start_date = start_date
        self._end_date = end_date

    def create_buy_and_hold(self, allocation):
        return SebRebalance.SebRebalance(self._funds, 
                                         allocation, 
                                         self._start_date, 
                                         self._end_date, 
                                         None)

    def create_rebalanced(self, allocation):
        # First get the periodical time series
        range = pd.date_range(start=self._start_date, end=self._end_date, freq='BAS').tolist()
        # Insert end values
        range.insert(0, self._start_date)
        range.append(self._end_date)

        # Make a shorter periodical series
        short_range = range[:-1]

        # First reverse the two time series - they begin at different dates 
        # since we removed the last date in short_range
        # Then zip the two series making tuples containing start and end value of a period
        periodIter = zip(reversed(range), reversed(short_range))
    
        next = None
        # Make a linked list of Rebalance objects, returning the last
        for end, start in periodIter:
            next = SebRebalance.SebRebalance(self._funds, allocation, start, end, next)
        
        return next