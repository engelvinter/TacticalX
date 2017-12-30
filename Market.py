
from ProcessReallocations import ProcessReallocations

from SebFundOperations import SebFundOperations

class Market:
    
    def __init__(self, funds, portfolio, logger = None):
        self._funds = funds
        self._portfolio = portfolio
        self._process_reallocations = ProcessReallocations(funds, portfolio, logger)
        self._logger = None

    def add_reallocation(self, fund_name, target_percentage_portfolio):
        self._process_reallocations.add_reallocation(fund_name, target_percentage_portfolio)
    
    def forced_sell_funds(self, date):
        s = SebFundOperations()
        fund_names = list(self._portfolio.get_all_fund_names())
        for fund_name in fund_names:
            (_, end) = s.get_interval(self._funds[fund_name])
            delta = end - date
            # Check if fund is closing
            if delta.days is 0:
                # Force selling of fund at last day
                order = self.add_reallocation(fund_name, 0.0)
                self._process_reallocations.execute(date)

    def simulate_business_day(self, date):
        self._process_reallocations.execute(date)
        
        portfolio_value = sum(self.calc_portfolio_value(date).values())

        self.forced_sell_funds(date)
        
        return portfolio_value

    #reallocate or rebalance portfolio
    def update_portfolio(self, date, new_allocation):
        # Sell all funds not in new allocation to get cash
        fund_shares_portfolio = self._portfolio.get_all_fund_shares()

        for fund_name, shares in fund_shares_portfolio:
            if fund_name not in new_allocation:
                self.add_reallocation(fund_name, 0.0)

        # Adjust the funds that we decide to keep
        for fund_name in new_allocation:
            self.add_reallocation(fund_name, new_allocation[fund_name])

    def calc_portfolio_value(self, date):
        return self._portfolio.calc_value(date, self._funds)
    
    