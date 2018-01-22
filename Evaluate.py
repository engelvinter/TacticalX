
import pandas as pd

class Evaluate:
    class Result:
        def __init__(self, total, yearly, quarterly, monthly):
            self.total = total
            self.yearly = yearly
            self.quarterly = quarterly
            self.monthly = monthly

    def __init__(self, timeseries):
        self._timeseries = timeseries
    
    def total_return(self, ts):
        ret = ts[-1] / ts[0]
        if ret > 1.0:
            perc = (ret - 1.0) * 100
        else:
            perc = -(1.0 - ret) * 100
        
        return perc

    def return_each_month(self, ts, freq):
        range = pd.date_range(start=ts.index[0], end=ts.index[-1], freq=freq).tolist()

        if range[0] != ts[0]:
            range.insert(0, ts.index[0])

        if range[-1] != ts[-1]:
            range.append(ts.index[-1])

        range1 = range[:-1]  # remove last date
        range2 = range[1:]   # remove first date

        result = {}
        for start, end in zip(range1, range2):
            start_idx = ts.index.get_loc(start, method = 'bfill')
            end_idx = ts.index.get_loc(end, method = 'ffill')
            month_ts = ts.iloc[start_idx:end_idx]
            result[end] = self.total_return(month_ts)

        return result

    def execute(self):
        total = self.total_return(self._timeseries)
        yearly = self.return_each_month(self._timeseries, "AS")
        quarterly = self.return_each_month(self._timeseries, "QS")
        monthly = self.return_each_month(self._timeseries, "MS")

        return Evaluate.Result(total, yearly, quarterly, monthly)

    

    