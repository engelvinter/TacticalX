
import pandas as pd

from dateutil import parser as date_parser

class Simulate:
    def __init__(self, start_date, end_date):
        try:
            self._start_date = date_parser.parse(start_date)
            self._end_date = date_parser.parse(end_date)
        except TypeError:
            self._start_date = start_date
            self._end_date = end_date

        self._reallocations = {}

    def _add_reallocation(self, date, reallocation):
        self._reallocations[date] = reallocation

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
        range = pd.date_range(start=self._start_date, end=self._end_date, freq="B").tolist()
        result = pd.Series(index=range)

        for date in range:
            try:
                if market.order_depth() > 0:
                    market.process_orders(date)

                if date in self._reallocations:
                    self._reallocations[date].execute(date, market)

                result[date] = sum(market.calc_portfolio_value(date).values())

            except Exception:
                pass

        return result.dropna()