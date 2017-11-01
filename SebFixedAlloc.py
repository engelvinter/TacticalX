
import Factory

class SebFixedAlloc:
    # where fixed alloc is a dictionary
    # name - percentage
    def __init__(self, funds, fixed_alloc, start_date, end_date):
        f = Factory.Factory()
        self._funds = funds
        self._fixed_alloc = fixed_alloc
        self._start_date = start_date
        self._end_date = end_date
        self._fund_ops = f.create_fund_operations()

    def current_portfolio_value(self, sum):
        self._sum = sum

    def execute(self):
        self._new_sum = 0
        funds_in_interval = self._fund_ops.filter_interval(self._funds, 
                                                           self._start_date, 
                                                           self._end_date)

        for name in self._fixed_alloc:
            if name not in funds_in_interval:
                raise Exception("Fund not found in i interval")
            alloc = self._fixed_alloc[name] * self._sum
            fund = self._funds[name]
            start_quote = fund.loc[self._start_date].quote
            end_quote = fund.loc[self._end_date].quote
            self._new_sum += alloc * end_quote / start_quote

        print(self._new_sum)
