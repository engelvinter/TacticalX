
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

    def _realloc(self, fixed_alloc, sum):
        return fixed_alloc * sum

    def _calc_new_result(self, fund, realloc_sum):        
        start_quote = fund.loc[self._start_date].quote
        end_quote = fund.loc[self._end_date].quote
        return realloc_sum * end_quote / start_quote

    def _get_available_funds(self):
        funds = self._fund_ops.filter_interval(self._funds, 
                                               self._start_date, 
                                               self._end_date)
        return funds
        
    def execute(self):
        new_sum = 0
        funds_in_interval = self._get_available_funds()

        for name in self._fixed_alloc:
            if name not in funds_in_interval:
                raise Exception("Fund not found in i interval")
            realloc_sum = self._realloc(self._fixed_alloc[name], self._sum)
            new_sum += self._calc_new_result(self._funds[name], realloc_sum)

        print(new_sum)
