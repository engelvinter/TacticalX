

import pandas as pd

from Portfolio import Portfolio

from DateUtil import assign_date

class Simulate:
    def __init__(self, start_date, end_date):
        self._start_date = assign_date(start_date)
        self._end_date = assign_date(end_date)
        self._algorithms = {}

    def _add_reallocation(self, date, algorithm):
        self._algorithms[date] = algorithm

    # freq as in pandas.date_range i.e. 
    # yearly => BAS
    # monthly => BM
    # quarterly => BQ
    def setup_reallocations(self, algorithm, freq):
        # First get the periodical time series
        range = pd.date_range(start=self._start_date, end=self._end_date, freq=freq).tolist()
        # Insert end values
        range.insert(0, self._start_date)
        range.append(self._end_date)
        
        for date in range:
            self._add_reallocation(date, algorithm)

    def execute(self, market):
        range = pd.bdate_range(start=self._start_date, end=self._end_date).tolist()
        result = pd.Series(index=range)

        for date in range:
            try:
                result[date] = market.simulate_business_day(date)
            except Portfolio.CalcValueException:
                pass

            if date in self._algorithms:
                self._algorithms[date].execute(date, market)

        return result.dropna()