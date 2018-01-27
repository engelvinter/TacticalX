
import pandas as pd

import empyrical

class Evaluate:
    class Result:
        def __init__(self, total, yearly, monthly, drawdown):
            self.total = total
            self.yearly = yearly
            self.monthly = monthly
            self.drawdown = drawdown

    def __init__(self, timeseries):
        self._timeseries = timeseries
    
    def total_return(self, daily_change):
        perc = empyrical.cum_returns_final(daily_change) * 100
        return round(perc, 0)

    def return_each_month(self, daily_change):
        result = empyrical.aggregate_returns(daily_change, 'monthly') * 100
        return result

    def return_each_year(self, daily_change):
        result = empyrical.aggregate_returns(daily_change, 'yearly') * 100
        return result

    def worst_drawdown(self, daily_change):
        result = empyrical.max_drawdown(daily_change) * 100
        return result

    def execute(self):
        daily_change = self._timeseries.pct_change()

        total = self.total_return(daily_change)

        yearly = self.return_each_year(daily_change)
        monthly = self.return_each_month(daily_change)

        drawdown = self.worst_drawdown(daily_change)

        return Evaluate.Result(total, yearly, monthly, drawdown)

    

    